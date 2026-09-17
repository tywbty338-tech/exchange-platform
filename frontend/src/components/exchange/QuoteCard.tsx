import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useStore } from '../../store'
import { formatAmount, formatRate } from '../../utils/format'

export function QuoteCard() {
  const { currentQuote, inputAmount, selectedCurrency, rates } = useStore()
  const [timeLeft, setTimeLeft] = useState(0)

  useEffect(() => {
    if (!currentQuote) return
    setTimeLeft(currentQuote.remaining_seconds)
    const timer = setInterval(() => {
      setTimeLeft((t) => Math.max(0, t - 1))
    }, 1000)
    return () => clearInterval(timer)
  }, [currentQuote])

  if (!currentQuote || !inputAmount) return null

  const rate = rates.find(r => r.currency === selectedCurrency)
  const iqdRate = rate ? Math.round(1 / rate.rate) : 0

  const isExpired = timeLeft <= 0

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass-card p-5"
    >
      <div className="text-center mb-4">
        <div className="text-sm text-text-muted mb-2">ستحصل على</div>
        <div className={`text-4xl font-bold font-mono ${selectedCurrency === 'USDT' ? 'text-usdt' : 'text-ton'}`}>
          {formatAmount(currentQuote.output_amount, selectedCurrency === 'TON' ? 4 : 2)} {selectedCurrency}
        </div>
      </div>

      <div className="space-y-3 py-4 border-t border-b border-border">
        <div className="flex justify-between text-sm">
          <span className="text-text-muted">سعر الصرف</span>
          <span className="font-mono">1 {selectedCurrency} = {formatRate(iqdRate)} د.ع</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-text-muted">العمولة</span>
          <span className="font-mono">{formatAmount(currentQuote.fee)} د.ع</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-text-muted">الصافي</span>
          <span className="font-mono font-semibold">{formatAmount(currentQuote.output_amount, selectedCurrency === 'TON' ? 4 : 2)} {selectedCurrency}</span>
        </div>
      </div>

      <div className="flex items-center justify-between pt-3">
        <span className="text-xs text-text-muted">السعر مضمون لمدة</span>
        <div className={`font-mono text-sm font-medium ${isExpired ? 'text-danger' : 'text-primary'}`}>
          {isExpired ? 'انتهت الصلاحية' : `00:${timeLeft.toString().padStart(2, '0')}`}
        </div>
      </div>

      {isExpired && (
        <div className="mt-3 text-center text-xs text-warning">
          انتهت صلاحية السعر - اضغط متابعة للتحديث
        </div>
      )}
    </motion.div>
  )
}
