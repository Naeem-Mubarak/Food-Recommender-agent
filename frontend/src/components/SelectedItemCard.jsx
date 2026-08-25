export default function SelectedItemCard({ item }) {
  if (!item) return null

  return (
    <div className="w-full max-w-md animate-rise-in">
      <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-saffron-500 mb-3">
        Confirming
      </p>
      <div className="border border-saffron-500/40 rounded-lg p-5 bg-char-800">
        <h3 className="font-display text-xl text-cream-100">{item.dish_name}</h3>
        <p className="text-cream-400 text-sm mt-1">{item.restaurant_name} · {item.cuisine_type}</p>
        <div className="flex items-center gap-4 mt-4 font-mono text-xs text-cream-400">
          <span>Spice {item.spice_level}/5</span>
          <span className="text-saffron-400">Rs. {item.dish_price}</span>
          <span>{item.type_of_food}</span>
        </div>
      </div>
    </div>
  )
}
