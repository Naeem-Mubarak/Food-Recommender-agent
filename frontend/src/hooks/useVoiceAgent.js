import { useCallback, useRef, useState } from 'react'

// ============================================================
// BACKEND CONTRACT:
//   ws://<VITE_WS_URL>/agent
//   - server speaks first on connect, no client message needed to start
//   - three interrupt types send a JSON frame before their audio:
//       'Select dish' -> array, 'confirmation' -> object,
//       'New_user' -> { user_id }
//   - agent's reply is ALWAYS audio (binary WAV, one clip per turn)
//   - the user's reply can be EITHER:
//       - binary audio bytes (voice mode) - server transcribes it
//       - a text frame (text mode) - server uses it directly
//     main.py branches on message type via a generic websocket.receive()
// ============================================================

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/agent'
const BAR_COUNT = 48
const MIN_RECORDING_MS = 600

export function useVoiceAgent() {
  // 'idle' | 'connecting' | 'agent_speaking' | 'listening' | 'processing' | 'waiting_for_user' | 'complete' | 'error'
  const [status, setStatus] = useState('idle')
  const [errorMessage, setErrorMessage] = useState(null)
  const [recommendations, setRecommendations] = useState(null)
  const [selectedItem, setSelectedItem] = useState(null)
  const [userId, setUserId] = useState(null)
  const [frequencyData, setFrequencyData] = useState(new Uint8Array(BAR_COUNT))

  const socketRef = useRef(null)
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const rafRef = useRef(null)

  const mediaRecorderRef = useRef(null)
  const chunksRef = useRef([])
  const micStreamRef = useRef(null)
  const recordingStartRef = useRef(0)

  const runVisualizerLoop = useCallback(() => {
    const analyser = analyserRef.current
    if (!analyser) return
    const bufferLength = analyser.frequencyBinCount
    const data = new Uint8Array(bufferLength)
    const tick = () => {
      analyser.getByteFrequencyData(data)
      const step = Math.floor(bufferLength / BAR_COUNT) || 1
      const bars = new Uint8Array(BAR_COUNT)
      for (let i = 0; i < BAR_COUNT; i++) bars[i] = data[i * step] || 0
      setFrequencyData(bars)
      rafRef.current = requestAnimationFrame(tick)
    }
    tick()
  }, [])

  const stopVisualizerLoop = useCallback(() => {
    if (rafRef.current) cancelAnimationFrame(rafRef.current)
    rafRef.current = null
    setFrequencyData(new Uint8Array(BAR_COUNT))
  }, [])

  // plays the agent's spoken reply - always runs, regardless of which
  // input mode the user is in, since output is voice-only either way
  const playAgentAudio = useCallback((arrayBuffer) => {
    return new Promise((resolve, reject) => {
      if (!audioContextRef.current) {
        audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
      }
      const ctx = audioContextRef.current
      ctx.decodeAudioData(
        arrayBuffer.slice(0),
        (decoded) => {
          const source = ctx.createBufferSource()
          source.buffer = decoded
          const analyser = ctx.createAnalyser()
          analyser.fftSize = 128
          analyserRef.current = analyser
          source.connect(analyser)
          analyser.connect(ctx.destination)
          setStatus('agent_speaking')
          runVisualizerLoop()
          source.onended = () => {
            stopVisualizerLoop()
            resolve()
          }
          source.start(0)
        },
        (err) => reject(err)
      )
    })
  }, [runVisualizerLoop, stopVisualizerLoop])

  const connect = useCallback(() => {
    setStatus('connecting')
    setErrorMessage(null)

    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
    }
    audioContextRef.current.resume()

    const socket = new WebSocket(WS_URL)
    socket.binaryType = 'arraybuffer'
    socketRef.current = socket

    socket.onopen = () => {}

    socket.onmessage = async (event) => {
      if (typeof event.data === 'string') {
        try {
          const parsed = JSON.parse(event.data)
          if (Array.isArray(parsed)) {
            setRecommendations(parsed)
            setSelectedItem(null)
          } else if (parsed.user_id !== undefined) {
            setUserId(parsed.user_id)
          } else {
            setSelectedItem(parsed)
          }
        } catch (e) {
          console.error('Failed to parse JSON frame:', e)
        }
        return
      }

      try {
        await playAgentAudio(event.data)
        setStatus('waiting_for_user')
      } catch (e) {
        console.error('Audio playback failed:', e)
        setStatus('error')
        setErrorMessage("Could not play the agent's response.")
      }
    }

    socket.onerror = () => {
      setStatus('error')
      setErrorMessage('Connection error - is the backend running?')
    }

    socket.onclose = () => {
      setStatus((prev) => (prev === 'error' ? prev : 'complete'))
      stopVisualizerLoop()
    }
  }, [playAgentAudio, stopVisualizerLoop])

  // ---------- voice input ----------
  const startListening = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      micStreamRef.current = stream

      if (!audioContextRef.current) {
        audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
      }
      const ctx = audioContextRef.current
      const micSource = ctx.createMediaStreamSource(stream)
      const analyser = ctx.createAnalyser()
      analyser.fftSize = 128
      micSource.connect(analyser)
      analyserRef.current = analyser
      runVisualizerLoop()

      const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' })
      chunksRef.current = []
      recorder.ondataavailable = (e) => chunksRef.current.push(e.data)
      recorder.start()

      mediaRecorderRef.current = recorder
      recordingStartRef.current = Date.now()
      setStatus('listening')
    } catch (e) {
      console.error('Microphone access failed:', e)
      setStatus('error')
      setErrorMessage('Microphone access was denied or is unavailable.')
    }
  }, [runVisualizerLoop])

  const stopListeningAndSend = useCallback(() => {
    const recorder = mediaRecorderRef.current
    if (!recorder) return

    const elapsed = Date.now() - recordingStartRef.current
    stopVisualizerLoop()

    recorder.onstop = async () => {
      micStreamRef.current?.getTracks().forEach((t) => t.stop())

      if (elapsed < MIN_RECORDING_MS) {
        setStatus('waiting_for_user')
        setErrorMessage('Hold the button a little longer while you speak.')
        return
      }
      setErrorMessage(null)

      const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
      const buffer = await blob.arrayBuffer()

      if (socketRef.current?.readyState === WebSocket.OPEN) {
        socketRef.current.send(buffer)
        setStatus('processing')
      } else {
        setStatus('error')
        setErrorMessage('Lost connection to the backend.')
      }
    }
    recorder.stop()
  }, [stopVisualizerLoop])

  const toggleMic = useCallback(() => {
    if (status === 'waiting_for_user') startListening()
    else if (status === 'listening') stopListeningAndSend()
  }, [status, startListening, stopListeningAndSend])

  // ---------- text input ----------
  // sends a TEXT frame instead of bytes - the backend uses it directly,
  // no transcription needed. Output still comes back as audio either way.
  const sendText = useCallback((text) => {
    const trimmed = text.trim()
    if (!trimmed) return
    if (socketRef.current?.readyState !== WebSocket.OPEN) {
      setStatus('error')
      setErrorMessage('Lost connection to the backend.')
      return
    }
    setErrorMessage(null)
    socketRef.current.send(trimmed)
    setStatus('processing')
  }, [])

  return {
    status,
    errorMessage,
    recommendations,
    selectedItem,
    userId,
    frequencyData,
    connect,
    toggleMic,
    sendText,
  }
}
