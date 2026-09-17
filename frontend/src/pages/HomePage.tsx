import { motion } from 'framer-motion'
import { useStore } from '../store'
import { RateCard } from '../components/rates/RateCard'
import { CurrencySelector } from '../components/exchange/CurrencySelector'
import { AmountInput } from '../components/exchange/AmountInput'
import { QuoteCard } from '../components/exchange/QuoteCard'
import { api } from '../services/api'
import { useState } from 'react'

export function HomePage() {
  const { selectedCurrency, inputAmount, setCurrentQuote, setPage, rates } = useStore()
  const [loading, setLoading] = useState(false)

  const network = selectedCurrency === 'USDT' ? 'TRC20' : 'TON'

  const handleGetQuote = async () => {
    if (!inputAmount || Number(inputAmount) < 3000) return
    setLoading(true)
    try {
      const quote = await api.createQuote({
        currency: selectedCurrency,
        network,
        input_amount: Number(inputAmount),
      })
      setCurrentQuote(quote)
      setPage('exchange')
    } catch (e: any) {
      alert(e.message || 'خطأ في obtaining السعر')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-lg mx-auto px-4 py-6 space-y-5">
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-4"
      >
        <h1 className="text-2xl font-bold mb-1">EXCHANGE</h1>
        <p className="text-sm text-text-muted">Digital Exchange Platform</p>
      </motion.div>

      <RateCard />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="space-y-4"
      >
        <CurrencySelector />
        <AmountInput />
        <QuoteCard />

        <button
          onClick={handleGetQuote}
          disabled={!inputAmount || Number(inputAmount) < 3000 || loading}
          className="btn-primary disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              جاري الحساب...
            </span>
          ) : (
            'متابعة التحويل'
          )}
        </button>
      </motion.div>
    </div>
  )
}
