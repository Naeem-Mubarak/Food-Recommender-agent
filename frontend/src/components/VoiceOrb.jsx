const BAR_COUNT = 48

const STATUS_COPY = {
  idle: 'Tap to begin',
  connecting: 'Connecting…',
  agent_speaking: 'Speaking',
  listening: 'Listening',
  processing: 'Thinking',
  waiting_for_user: 'Your turn',
  complete: 'Order placed',
  error: 'Something went wrong',
}

const STATUS_COLOR = {
  agent_speaking: '#E8A33D', // saffron
  listening: '#C1442B',      // chili
}

export default function VoiceOrb({ status, frequencyData, onTap, disabled }) {
  const isActive = status === 'agent_speaking' || status === 'listening'
  const barColor = STATUS_COLOR[status] || '#E8A33D'
  const canTap = status === 'waiting_for_user' || status === 'listening'

  const radius = 78
  const center = 100

  return (
    <div className="flex flex-col items-center gap-6">
      <button
        onClick={onTap}
        disabled={disabled || !canTap}
        aria-label={canTap ? (status === 'listening' ? 'Stop and send' : 'Start speaking') : 'Voice agent'}
        className="relative w-[200px] h-[200px] rounded-full flex items-center justify-center
                   disabled:cursor-not-allowed transition-transform duration-200
                   enabled:hover:scale-[1.03] enabled:active:scale-[0.97]"
      >
        {/* frequency ring - reacts to real playing/captured audio */}
        <svg viewBox="0 0 200 200" className="absolute inset-0 w-full h-full">
          {Array.from({ length: BAR_COUNT }).map((_, i) => {
            const angle = (i / BAR_COUNT) * Math.PI * 2
            const magnitude = isActive ? (frequencyData[i] || 0) / 255 : 0.06
            const barLength = 10 + magnitude * 26
            const x1 = center + Math.cos(angle) * radius
            const y1 = center + Math.sin(angle) * radius
            const x2 = center + Math.cos(angle) * (radius + barLength)
            const y2 = center + Math.sin(angle) * (radius + barLength)
            return (
              <line
                key={i}
                x1={x1} y1={y1} x2={x2} y2={y2}
                stroke={barColor}
                strokeWidth="2.5"
                strokeLinecap="round"
                opacity={isActive ? 0.55 + magnitude * 0.45 : 0.35}
                style={{ transition: isActive ? 'none' : 'opacity 0.4s ease' }}
              />
            )
          })}
        </svg>

        {/* core disc */}
        <div
          className={`relative w-[136px] h-[136px] rounded-full border flex items-center justify-center
                      transition-colors duration-300
                      ${status === 'listening' ? 'bg-chili-500/10 border-chili-500/50' : 'bg-char-800 border-saffron-500/30'}`}
        >
          <MicIcon active={status === 'listening'} />
        </div>
      </button>

      <div className="text-center">
        <p className="font-mono text-xs uppercase tracking-[0.2em] text-cream-400">
          {STATUS_COPY[status] || ''}
        </p>
      </div>
    </div>
  )
}

function MicIcon({ active }) {
  return (
    <svg viewBox="0 0 24 24" className={`w-7 h-7 ${active ? 'fill-chili-500' : 'fill-saffron-500'}`}>
      <path d="M12 14a3 3 0 0 0 3-3V5a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3zm5-3a5 5 0 0 1-10 0H5a7 7 0 0 0 6 6.92V21h2v-3.08A7 7 0 0 0 19 11h-2z"/>
    </svg>
  )
}
