import { motion } from 'framer-motion'
import { useStore } from '../../store'

export function CurrencySelector() {
  const { selectedCurrency, setSelectedCurrency } = useStore()

  return (
    <div className="glass-card p-1.5 flex gap-1">
      {(['USDT', 'TON'] as const).map((currency) => (
        <button
          key={currency}
          onClick={() => setSelectedCurrency(currency)}
          className={`flex-1 py-3 rounded-xl font-semibold text-sm transition-all duration-300 relative ${
            selectedCurrency === currency
              ? currency === 'USDT'
                ? 'text-white glow-usdt'
                : 'text-white glow-ton'
              : 'text-text-muted'
          }`}
        >
          {selectedCurrency === currency && (
            <motion.div
              layoutId="currency-bg"
              className={`absolute inset-0 rounded-xl ${
                currency === 'USDT' ? 'bg-usdt/20' : 'bg-ton/20'
              }`}
              transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
            />
          )}
          <span className="relative z-10 flex items-center justify-center gap-2">
            {currency === 'USDT' ? '💵' : '💎'} {currency}
          </span>
        </button>
      ))}
    </div>
  )
}
