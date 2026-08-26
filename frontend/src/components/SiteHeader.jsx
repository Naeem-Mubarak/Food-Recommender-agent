export default function SiteHeader() {
  return (
    <header className="w-full px-6 md:px-10 py-6 flex items-center justify-between border-b border-char-700/60">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-saffron-500 flex items-center justify-center">
          <span className="font-display text-char-900 text-sm font-semibold">V</span>
        </div>
        <span className="font-display text-cream-100 text-lg tracking-wide">Voice-Driven Ordering</span>
      </div>
      <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-cream-400">
        Mood-Based Agent
      </span>
    </header>
  )
}
