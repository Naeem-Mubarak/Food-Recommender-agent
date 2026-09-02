import { useState } from 'react'
import { useVoiceAgent } from './hooks/useVoiceAgent'
import SiteHeader from './components/SiteHeader'
import VoiceOrb from './components/VoiceOrb'
import TextInputBar from './components/TextInputBar'
import RecommendationsTable from './components/RecommendationsTable'
import SelectedItemCard from './components/SelectedItemCard'
import UserIdBadge from './components/UserIdBadge'

export default function App() {
  const {
    status,
    errorMessage,
    recommendations,
    selectedItem,
    userId,
    frequencyData,
    connect,
    toggleMic,
    sendText,
  } = useVoiceAgent()

  // 'voice' | 'text' - only controls how the USER replies.
  // The agent's spoken reply (and the orb's visualization while it
  // speaks) is identical in either mode - output is always voice.
  const [inputMode, setInputMode] = useState('voice')

  const notStarted = status === 'idle'

  return (
    <div className="min-h-screen flex flex-col bg-char-900">
      <SiteHeader />

      <main className="flex-1 flex flex-col items-center justify-center px-6 py-16 gap-8">
        {notStarted && (
          <div className="text-center max-w-lg animate-rise-in">
            <h1 className="font-display text-4xl md:text-5xl text-cream-100 leading-tight">
              Tell us what you're craving.
            </h1>
            <p className="font-body text-cream-400 mt-4 text-base">
              Speak or type — spicy, sweet, on a budget, whatever's on your mind.
              We'll take it from there.
            </p>
            <button
              onClick={connect}
              className="mt-8 px-8 py-3 rounded-full bg-saffron-500 text-char-900 font-body font-semibold
                         hover:bg-saffron-400 transition-colors duration-200"
            >
              Start ordering
            </button>
          </div>
        )}

        {!notStarted && (
          <>
            <UserIdBadge userId={userId} />

            {/* Orb + visualization is always shown - it's how the
                agent's spoken reply is represented, regardless of
                which input mode is active. */}
            <VoiceOrb
              status={inputMode === 'voice' ? status : (status === 'agent_speaking' ? status : 'waiting_for_user')}
              frequencyData={frequencyData}
              onTap={inputMode === 'voice' ? toggleMic : undefined}
              disabled={inputMode !== 'voice' || status === 'error' || status === 'complete'}
            />

            {/* Mode toggle - switch anytime except mid-recording */}
            <div className="flex gap-1 p-1 rounded-full bg-char-800 border border-char-700">
              <button
                onClick={() => setInputMode('voice')}
                disabled={status === 'listening'}
                className={`px-4 py-1.5 rounded-full text-xs font-mono uppercase tracking-wider transition-colors
                           ${inputMode === 'voice' ? 'bg-saffron-500 text-char-900' : 'text-cream-400'}`}
              >
                Voice
              </button>
              <button
                onClick={() => setInputMode('text')}
                disabled={status === 'listening'}
                className={`px-4 py-1.5 rounded-full text-xs font-mono uppercase tracking-wider transition-colors
                           ${inputMode === 'text' ? 'bg-saffron-500 text-char-900' : 'text-cream-400'}`}
              >
                Text
              </button>
            </div>

            {inputMode === 'text' && (
              <TextInputBar status={status} onSend={sendText} />
            )}

            {errorMessage && (
              <p className="font-mono text-xs text-chili-500 max-w-sm text-center">
                {errorMessage}
              </p>
            )}

            {status === 'complete' && (
              <p className="font-display text-2xl text-saffron-400 animate-rise-in">
                Your order's on its way.
              </p>
            )}

            <RecommendationsTable dishes={recommendations} />
            <SelectedItemCard item={selectedItem} />
          </>
        )}
      </main>

      <footer className="px-6 md:px-10 py-6 text-center">
        <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-cream-400/50">
          Voice-Driven Mood-Based Ordering Agent
        </p>
      </footer>
    </div>
  )
}
