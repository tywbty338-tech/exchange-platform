import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useStore } from '../store'
import { api } from '../services/api'
import type { Wallet } from '../types'

export function WalletPage() {
  const { wallets, setWallets } = useStore()
  const [loading, setLoading] = useState(true)
  const [showAdd, setShowAdd] = useState(false)
  const [currency, setCurrency] = useState('USDT')
  const [network, setNetwork] = useState('TRC20')
  const [address, setAddress] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getWallets()
        setWallets(data)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [setWallets])

  const handleAdd = async () => {
    if (!address || address.length < 10) return
    setSaving(true)
    try {
      await api.createWallet({ currency, network, address })
      const data = await api.getWallets()
      setWallets(data)
      setShowAdd(false)
      setAddress('')
    } catch (e: any) {
      alert(e.message || 'خطأ')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('هل أنت متأكد من حذف المحفظة؟')) return
    try {
      await api.deleteWallet(id)
      setWallets(wallets.filter(w => w.id !== id))
    } catch (e: any) {
      alert(e.message || 'خطأ')
    }
  }

  if (loading) {
    return (
      <div className="max-w-lg mx-auto px-4 py-6 space-y-4">
        <h2 className="text-xl font-bold">محفظتي</h2>
        {[1, 2].map((i) => (
          <div key={i} className="glass-card p-4 space-y-3">
            <div className="skeleton h-4 w-20" />
            <div className="skeleton h-3 w-full" />
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="max-w-lg mx-auto px-4 py-6 space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold">محفظتي</h2>
        <button
          onClick={() => setShowAdd(!showAdd)}
          className="text-sm text-primary font-medium"
        >
          + إضافة
        </button>
      </div>

      {showAdd && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="glass-card p-5 space-y-3"
        >
          <div className="flex gap-2">
            {['USDT', 'TON'].map((c) => (
              <button
                key={c}
                onClick={() => { setCurrency(c); setNetwork(c === 'USDT' ? 'TRC20' : 'TON') }}
                className={`flex-1 py-2 rounded-xl text-sm font-medium transition-all ${
                  currency === c ? 'bg-primary/20 text-primary border border-primary/30' : 'bg-bg-card text-text-muted border border-border'
                }`}
              >
                {c === 'USDT' ? '💵' : '💎'} {c}
              </button>
            ))}
          </div>
          <input
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            placeholder={currency === 'TON' ? 'EQ...' : 'T...'}
            className="w-full bg-bg-card border border-border rounded-xl px-4 py-3 text-sm font-mono outline-none focus:border-primary"
            dir="ltr"
          />
          <button onClick={handleAdd} disabled={saving} className="btn-primary text-sm py-3">
            {saving ? 'جاري الحفظ...' : 'حفظ المحفظة'}
          </button>
        </motion.div>
      )}

      {wallets.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="text-4xl mb-3">💼</div>
          <div className="text-text-muted mb-1">لم تتم إضافة محفظة بعد</div>
          <button onClick={() => setShowAdd(true)} className="text-primary text-sm mt-2">
            إضافة محفظة
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          {wallets.map((wallet, i) => (
            <motion.div
              key={wallet.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="glass-card p-4"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span>{wallet.currency === 'USDT' ? '💵' : '💎'}</span>
                  <span className="font-medium">{wallet.currency}</span>
                  <span className="text-xs text-text-muted">{wallet.network}</span>
                </div>
                <button onClick={() => handleDelete(wallet.id)} className="text-danger text-xs">
                  حذف
                </button>
              </div>
              <div className="text-sm font-mono text-text-secondary truncate" dir="ltr">
                {wallet.address}
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}
