export default function UserIdBadge({ userId }) {
  if (userId === null || userId === undefined) return null

  return (
    <div className="flex items-center gap-2 px-4 py-2 rounded-full border border-saffron-500/30 bg-char-800 animate-rise-in">
      <span className="font-mono text-[11px] uppercase tracking-[0.15em] text-cream-400">Your ID</span>
      <span className="font-mono text-sm text-saffron-400 font-medium">{userId}</span>
    </div>
  )
}
