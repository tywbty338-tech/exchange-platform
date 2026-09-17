import { motion } from 'framer-motion'
import { useStore } from '../../store'
import { formatRate, timeAgo } from '../../utils/format'

export function RateCard() {
  const { rates } = useStore()
  const usdt = rates.find(r => r.currency === 'USDT' && r.network === 'TRC20')
  const ton = rates.find(r => r.currency === 'TON' && r.network === 'TON')

  return (
    <div className="space-y-3">
      {usdt && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-5 glow-usdt"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-2xl">💵</span>
              <span className="text-lg font-semibold">USDT</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 bg-success rounded-full animate-pulse-live" />
              <span className="text-xs text-text-muted">متاح</span>
            </div>
          </div>
          <div className="text-center py-4">
            <div className="text-sm text-text-muted mb-1">1 USDT</div>
            <div className="text-3xl font-bold text-usdt font-mono">
              {formatRate(1 / usdt.rate)} <span className="text-lg text-text-muted">د.ع</span>
            </div>
          </div>
          <div className="flex items-center justify-between text-xs text-text-muted pt-2 border-t border-border">
            <span>آخر تحديث: {usdt.updated_at ? timeAgo(usdt.updated_at) : 'الآن'}</span>
            <span>الحد: {formatRate(usdt.min_amount)} - {formatRate(usdt.max_amount)}</span>
          </div>
        </motion.div>
      )}

      {ton && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card p-5 glow-ton"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="text-2xl">💎</span>
              <span className="text-lg font-semibold">TON</span>
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 bg-success rounded-full animate-pulse-live" />
              <span className="text-xs text-text-muted">متاح</span>
            </div>
          </div>
          <div className="text-center py-4">
            <div className="text-sm text-text-muted mb-1">1 TON</div>
            <div className="text-3xl font-bold text-ton font-mono">
              {formatRate(1 / ton.rate)} <span className="text-lg text-text-muted">د.ع</span>
            </div>
          </div>
          <div className="flex items-center justify-between text-xs text-text-muted pt-2 border-t border-border">
            <span>آخر تحديث: {ton.updated_at ? timeAgo(ton.updated_at) : 'الآن'}</span>
            <span>الحد: {formatRate(ton.min_amount)} - {formatRate(ton.max_amount)}</span>
          </div>
        </motion.div>
      )}

      {!usdt && !ton && (
        <div className="glass-card p-8 text-center">
          <div className="text-text-muted">جاري تحميل الأسعار...</div>
        </div>
      )}
    </div>
  )
}
