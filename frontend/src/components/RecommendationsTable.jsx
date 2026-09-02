export default function RecommendationsTable({ dishes }) {
  if (!dishes || dishes.length === 0) return null

  return (
    <div className="w-full max-w-2xl animate-rise-in">
      <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-saffron-500 mb-3">
        Your options
      </p>
      <div className="border border-char-700 rounded-lg overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="bg-char-800 text-cream-400 font-mono text-[11px] uppercase tracking-wider">
              <th className="px-4 py-3 font-medium">Dish</th>
              <th className="px-4 py-3 font-medium hidden sm:table-cell">Restaurant</th>
              <th className="px-4 py-3 font-medium">Spice</th>
              <th className="px-4 py-3 font-medium">Price</th>
            </tr>
          </thead>
          <tbody>
            {dishes.map((dish, i) => (
              <tr key={i} className="border-t border-char-700/60 text-cream-100 font-body text-sm">
                <td className="px-4 py-3">
                  {dish.dish_name}
                  <span className="block sm:hidden text-cream-400 text-xs mt-0.5">{dish.restaurant_name}</span>
                </td>
                <td className="px-4 py-3 hidden sm:table-cell text-cream-400">{dish.restaurant_name}</td>
                <td className="px-4 py-3">
                  <SpiceLevel level={dish.spice_level} />
                </td>
                <td className="px-4 py-3 font-mono text-saffron-400">Rs. {dish.dish_price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function SpiceLevel({ level = 0 }) {
  return (
    <span className="font-mono text-xs text-chili-500">
      {'●'.repeat(level)}
      <span className="text-char-700">{'●'.repeat(Math.max(0, 5 - level))}</span>
    </span>
  )
}
