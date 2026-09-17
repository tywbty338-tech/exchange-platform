import { useStore } from '../../store'
import { formatAmount } from '../../utils/format'

const quickAmounts = [3000, 5000, 10000, 25000, 50000]

export function AmountInput() {
  const { inputAmount, setInputAmount } = useStore()

  return (
    <div className="glass-card p-5">
      <div className="text-sm text-text-muted mb-3">مبلغ رصيد آسياسيل</div>
      <div className="relative">
        <input
          type="text"
          inputMode="numeric"
          value={inputAmount ? formatAmount(Number(inputAmount)) : ''}
          onChange={(e) => setInputAmount(e.target.value.replace(/[^0-9]/g, ''))}
          placeholder="0"
          className="w-full bg-transparent text-4xl font-bold text-text text-center py-4 outline-none font-mono"
        />
        <div className="text-center text-text-muted text-sm">IQD</div>
      </div>
      <div className="flex flex-wrap gap-2 mt-4 justify-center">
        {quickAmounts.map((amount) => (
          <button
            key={amount}
            onClick={() => setInputAmount(String(amount))}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
              Number(inputAmount) === amount
                ? 'bg-primary/20 text-primary border border-primary/30'
                : 'bg-bg-card text-text-secondary border border-border hover:border-primary/30'
            }`}
          >
            {formatAmount(amount)}
          </button>
        ))}
      </div>
    </div>
  )
}
