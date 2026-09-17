import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useStore } from '../store'
import { api } from '../services/api'
import { formatAmount, statusInfo, timeAgo } from '../utils/format'
import type { Order } from '../types'

export function OrdersPage() {
  const { orders, setOrders } = useStore()
  const [filter, setFilter] = useState<string>('all')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getOrders()
        setOrders(data)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [setOrders])

  const filters = [
    { id: 'all', label: 'الكل' },
    { id: 'COMPLETED', label: 'مكتمل' },
    { id: 'active', label: 'قيد التنفيذ' },
    { id: 'CANCELLED', label: 'ملغي' },
  ]

  const filtered = orders.filter((o) => {
    if (filter === 'all') return true
    if (filter === 'active') return !['COMPLETED', 'CANCELLED', 'REJECTED'].includes(o.status)
    return o.status === filter
  })

  if (loading) {
    return (
      <div className="max-w-lg mx-auto px-4 py-6 space-y-4">
        <h2 className="text-xl font-bold">طلباتي</h2>
        {[1, 2, 3].map((i) => (
          <div key={i} className="glass-card p-4 space-y-3">
            <div className="skeleton h-4 w-20" />
            <div className="skeleton h-3 w-full" />
            <div className="skeleton h-3 w-2/3" />
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="max-w-lg mx-auto px-4 py-6 space-y-4">
      <h2 className="text-xl font-bold">طلباتي</h2>

      <div className="flex gap-2 overflow-x-auto no-scrollbar">
        {filters.map((f) => (
          <button
            key={f.id}
            onClick={() => setFilter(f.id)}
            className={`px-4 py-2 rounded-xl text-sm font-medium whitespace-nowrap transition-all ${
              filter === f.id
                ? 'bg-primary/20 text-primary border border-primary/30'
                : 'bg-bg-card text-text-muted border border-border'
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="text-4xl mb-3">📋</div>
          <div className="text-text-muted mb-1">لا توجد طلبات بعد</div>
          <div className="text-sm text-text-muted">ابدأ أول عملية تحويل لك</div>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((order, i) => {
            const status = statusInfo(order.status)
            const icon = order.output_currency === 'USDT' ? '💵' : '💎'
            return (
              <motion.div
                key={order.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="glass-card p-4"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{icon}</span>
                    <span className="font-mono font-medium">{order.order_number}</span>
                  </div>
                  <span className={`text-xs ${status.color}`}>{status.emoji} {status.label}</span>
                </div>
                <div className="text-sm text-text-secondary">
                  {formatAmount(order.input_amount)} د.ع → {formatAmount(order.output_amount, order.output_currency === 'TON' ? 4 : 2)} {order.output_currency}
                </div>
                <div className="text-xs text-text-muted mt-1">
                  {order.created_at ? timeAgo(order.created_at) : ''}
                </div>
              </motion.div>
            )
          })}
        </div>
      )}
    </div>
  )
}
