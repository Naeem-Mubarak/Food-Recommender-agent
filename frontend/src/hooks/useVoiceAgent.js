import { useCallback, useRef, useState } from 'react'

// ============================================================
// BACKEND CONTRACT (confirmed against backend/app/main.py):
//
//   ws://<VITE_WS_URL>/agent
//
//   - The socket speaks first. The moment it opens, the server
//     is already running the graph and will push messages with
//     no message required from the client first.
//   - For three interrupt types, a JSON text frame arrives BEFORE
//     the audio for that turn:
//       'Select dish'   -> JSON array of recommended dishes
//       'confirmation'  -> JSON object of the selected dish
//       'New_user'      -> JSON object { user_id: <int> }
//     Every other interrupt type sends audio only, no JSON.
//   - Audio always follows (binary frame, a WAV clip - one
//     complete file per turn, not a live stream of samples).
//   - The client responds by sending ONE binary audio blob
//     (the user's recorded turn) as an ArrayBuffer.
//   - This repeats until the graph finishes. There is currently
//     no explicit "conversation complete" signal from the server -
//     the socket just stops sending further turns. This hook
//     treats a clean socket close with no pending turn as "done".
// ============================================================

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/agent'

// how many bars the visualizer renders around the orb
const BAR_COUNT = 48

// Whisper hallucinates ("please like and subscribe"-style phrases) on
// very short/near-silent clips. Requiring a minimum press duration
// filters out accidental taps and cuts down on this significantly.
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

  // pulls frequency bins out of the analyser every animation frame,
  // feeding the visualizer around the orb - this only runs while
  // audio is actually playing or the mic is actively capturing
  const runVisualizerLoop = useCallback(() => {
    const analyser = analyserRef.current
    if (!analyser) return

    const bufferLength = analyser.frequencyBinCount
    const data = new Uint8Array(bufferLength)

    const tick = () => {
      analyser.getByteFrequencyData(data)
      // downsample to BAR_COUNT bars for the visual
      const step = Math.floor(bufferLength / BAR_COUNT) || 1
      const bars = new Uint8Array(BAR_COUNT)
      for (let i = 0; i < BAR_COUNT; i++) {
        bars[i] = data[i * step] || 0
      }
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

  // ------------------------------------------------------------
  // BACKEND CONNECTION POINT 1 - play the agent's spoken reply
  // Decodes the WAV bytes, connects them through an AnalyserNode
  // (so the visualization reflects the real playing audio, not a
  // random animation), and plays them.
  // ------------------------------------------------------------
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

  // ------------------------------------------------------------
  // BACKEND CONNECTION POINT 2 - open the socket and listen
  // ------------------------------------------------------------
  const connect = useCallback(() => {
    setStatus('connecting')
    setErrorMessage(null)

    // Create + resume the AudioContext HERE, synchronously, inside the
    // click handler - this satisfies the browser's autoplay policy.
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
    }
    audioContextRef.current.resume()

    const socket = new WebSocket(WS_URL)
    socket.binaryType = 'arraybuffer'
    socketRef.current = socket

    socket.onopen = () => {
      // nothing to send here - the backend speaks first
    }

    socket.onmessage = async (event) => {
      if (typeof event.data === 'string') {
        // JSON frame: recommendations (array), selected item (object),
        // or a new user's id (object with a user_id key)
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

      // binary frame: the agent's spoken audio for this turn
      try {
        await playAgentAudio(event.data)
        setStatus('waiting_for_user')
      } catch (e) {
        console.error('Audio playback failed:', e)
        setStatus('error')
        setErrorMessage('Could not play the agent\'s response.')
      }
    }

    socket.onerror = () => {
      setStatus('error')
      setErrorMessage('Connection error - is the backend running?')
    }

    socket.onclose = () => {
      // if we were mid-conversation and not already handling an
      // error, treat a closed socket as the conversation finishing
      setStatus((prev) => (prev === 'error' ? prev : 'complete'))
      stopVisualizerLoop()
    }
  }, [playAgentAudio, stopVisualizerLoop])

  // ------------------------------------------------------------
  // BACKEND CONNECTION POINT 3 - capture and send the user's turn
  // Press once to start, press again to stop - no fixed duration.
  // (Note: the backend transcribes one complete clip per turn via
  // Groq Whisper, not a live streaming transcript, so a full
  // press/stop cycle per turn is the correct shape here - true
  // continuous streaming ASR isn't something the backend supports.)
  // ------------------------------------------------------------
  const startListening = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      micStreamRef.current = stream

      // live-visualize the mic input too, so "listening" feels responsive
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

      const recorder = new MediaRecorder(stream)
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

      // guard against near-instant taps - these produce near-silent
      // clips that Whisper is prone to hallucinating text from
      if (elapsed < MIN_RECORDING_MS) {
        setStatus('waiting_for_user')
        setErrorMessage('Hold the button a little longer while you speak.')
        return
      }
      setErrorMessage(null)

      const blob = new Blob(chunksRef.current, { type: 'audio/wav' })
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
    if (status === 'waiting_for_user') {
      startListening()
    } else if (status === 'listening') {
      stopListeningAndSend()
    }
  }, [status, startListening, stopListeningAndSend])

  return {
    status,
    errorMessage,
    recommendations,
    selectedItem,
    userId,
    frequencyData,
    connect,
    toggleMic,
  }
}
