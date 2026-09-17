import { motion } from 'framer-motion'
import { useStore } from '../store'

export function ProfilePage() {
  const { orders, user } = useStore()

  const completed = orders.filter(o => o.status === 'COMPLETED').length
  const totalVolume = orders.reduce((sum, o) => sum + o.input_amount, 0)

  return (
    <div className="max-w-lg mx-auto px-4 py-6 space-y-4">
      <h2 className="text-xl font-bold">حسابي</h2>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6 text-center"
      >
        <div className="w-16 h-16 mx-auto mb-3 rounded-full bg-primary/20 flex items-center justify-center">
          <span className="text-2xl">👤</span>
        </div>
        <div className="font-semibold mb-0.5">{user?.username || 'مستخدم'}</div>
        <div className="text-sm text-text-muted">ID: {user?.telegram_id || '—'}</div>
      </motion.div>

      <div className="grid grid-cols-2 gap-3">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card p-4 text-center"
        >
          <div className="text-2xl font-bold text-primary">{orders.length}</div>
          <div className="text-xs text-text-muted mt-1">عدد الطلبات</div>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="glass-card p-4 text-center"
        >
          <div className="text-2xl font-bold text-success">{completed}</div>
          <div className="text-xs text-text-muted mt-1">مكتملة</div>
        </motion.div>
      </div>

      <div className="glass-card p-5 space-y-3">
        <h3 className="font-semibold text-sm mb-2">الإعدادات</h3>
        <div className="flex items-center justify-between py-2 border-b border-border">
          <span className="text-sm text-text-secondary">الإشعارات</span>
          <span className="text-success text-sm">مفعلة</span>
        </div>
        <div className="flex items-center justify-between py-2 border-b border-border">
          <span className="text-sm text-text-secondary">اللغة</span>
          <span className="text-sm">العربية</span>
        </div>
        <div className="flex items-center justify-between py-2">
          <span className="text-sm text-text-secondary">الوضع</span>
          <span className="text-sm">اختبار</span>
        </div>
      </div>

      <div className="glass-card p-5 space-y-3">
        <h3 className="font-semibold text-sm mb-2">الدعم</h3>
        <div className="text-sm text-text-secondary">
          للدعم الفني: @support
        </div>
      </div>
    </div>
  )
}
