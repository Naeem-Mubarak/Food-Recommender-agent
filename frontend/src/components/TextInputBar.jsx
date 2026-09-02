import { useState } from 'react'

export default function TextInputBar({ status, onSend }) {
  const [value, setValue] = useState('')
  const canSend = status === 'waiting_for_user'

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!canSend || !value.trim()) return
    onSend(value)
    setValue('')
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md flex gap-2">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        disabled={!canSend}
        placeholder={canSend ? 'Type your reply...' : 'Waiting for the agent...'}
        className="flex-1 px-4 py-2.5 rounded-full bg-char-800 border border-char-700
                   text-cream-100 text-sm placeholder-cream-400/50 font-body
                   focus:outline-none focus:border-saffron-500/60 transition-colors
                   disabled:opacity-50 disabled:cursor-not-allowed"
      />
      <button
        type="submit"
        disabled={!canSend || !value.trim()}
        className="px-5 py-2.5 rounded-full bg-saffron-500 text-char-900 font-body font-semibold text-sm
                   hover:bg-saffron-400 transition-colors duration-200
                   disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-saffron-500"
      >
        Send
      </button>
    </form>
  )
}
