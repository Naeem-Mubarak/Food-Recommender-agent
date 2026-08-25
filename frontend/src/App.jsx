import { useVoiceAgent } from './hooks/useVoiceAgent'
import SiteHeader from './components/SiteHeader'
import VoiceOrb from './components/VoiceOrb'
import RecommendationsTable from './components/RecommendationsTable'
import SelectedItemCard from './components/SelectedItemCard'

export default function App() {
  const {
    status,
    errorMessage,
    recommendations,
    selectedItem,
    frequencyData,
    connect,
    toggleMic,
  } = useVoiceAgent()

  const notStarted = status === 'idle'

  return (
    <div className="min-h-screen flex flex-col bg-char-900">
      <SiteHeader />

      <main className="flex-1 flex flex-col items-center justify-center px-6 py-16 gap-12">
        {notStarted && (
          <div className="text-center max-w-lg animate-rise-in">
            <h1 className="font-display text-4xl md:text-5xl text-cream-100 leading-tight">
              Tell us what you're craving.
            </h1>
            <p className="font-body text-cream-400 mt-4 text-base">
              Speak naturally — spicy, sweet, on a budget, whatever's on your mind.
              We'll take it from there.
            </p>
            {/* ============================================================
                BACKEND CONNECTION POINT: opening the conversation.
                connect() opens the websocket. The AudioContext is created
                lazily on this same click too, satisfying browser autoplay
                policy - this is why the orb doesn't appear until the user
                takes this first action.
                ============================================================ */}
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
            <VoiceOrb
              status={status}
              frequencyData={frequencyData}
              onTap={toggleMic}
              disabled={status === 'error' || status === 'complete'}
            />

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
          Dastarkhwan · Mood-based ordering
        </p>
      </footer>
    </div>
  )
}
