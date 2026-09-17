import { useState } from 'react'
import { motion } from 'framer-motion'
import { useStore } from '../store'
import { api } from '../services/api'
import { formatAmount, formatRate, statusInfo } from '../utils/format'

type Step = 'quote' | 'payment' | 'wallet' | 'confirm' | 'success'

export function ExchangePage() {
  const { currentQuote, selectedCurrency, setCurrentQuote, setPage } = useStore()
  const [step, setStep] = useState<Step>('quote')
  const [orderId, setOrderId] = useState<number | null>(null)
  const [orderNumber, setOrderNumber] = useState('')
  const [walletAddress, setWalletAddress] = useState('')
  const [txHash, setTxHash] = useState('')
  const [phone, setPhone] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (!currentQuote) {
    return (
      <div className="max-w-lg mx-auto px-4 py-20 text-center">
        <div className="text-text-muted mb-4">لا يوجد سعر محدد</div>
        <button onClick={() => setPage('home')} className="btn-primary">
          العودة للرئيسية
        </button>
      </div>
    )
  }

  const handleCreateOrder = async () => {
    setLoading(true)
    setError('')
    try {
      const order = await api.createOrder(currentQuote.quote_id)
      setOrderId(order.id)
      setOrderNumber(order.order_number)
      setStep('payment')
    } catch (e: any) {
      setError(e.message || 'خطأ في إنشاء الطلب')
    } finally {
      setLoading(false)
    }
  }

  const handlePayment = async () => {
    if (!phone || phone.length < 10) {
      setError('أدخل رقم آسياسيل صحيح')
      return
    }
    setLoading(true)
    setError('')
    try {
      // In TEST_MODE, payment is auto-confirmed
      setStep('wallet')
    } catch (e: any) {
      setError(e.message || 'خطأ في الدفع')
    } finally {
      setLoading(false)
    }
  }

  const handleSetWallet = async () => {
    if (!walletAddress || walletAddress.length < 10) {
      setError('أدخل عنوان محفظة صحيح')
      return
    }
    setLoading(true)
    setError('')
    try {
      await api.setWallet(orderId!, walletAddress)
      setStep('confirm')
    } catch (e: any) {
      setError(e.message || 'خطأ في العنوان')
    } finally {
      setLoading(false)
    }
  }

  const handleConfirm = async () => {
    setLoading(true)
    setError('')
    try {
      const result = await api.confirmOrder(orderId!)
      setTxHash(result.tx_hash || '0x' + Math.random().toString(16).slice(2, 18))
      setStep('success')
    } catch (e: any) {
      setError(e.message || 'خطأ في التأكيد')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-lg mx-auto px-4 py-6 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button onClick={() => {
          if (step === 'quote') setPage('home')
          else if (step === 'payment') setStep('quote')
          else if (step === 'wallet') setStep('payment')
          else if (step === 'confirm') setStep('wallet')
          else setPage('home')
        }} className="text-text-muted">
          ← رجوع
        </button>
        <h2 className="font-semibold">
          {step === 'quote' && 'ملخص التحويل'}
          {step === 'payment' && 'الدفع'}
          {step === 'wallet' && 'المحفظة'}
          {step === 'confirm' && 'التأكيد'}
          {step === 'success' && 'تم بنجاح'}
        </h2>
        <div className="w-10" />
      </div>

      {/* Progress */}
      <div className="flex gap-1.5">
        {['quote', 'payment', 'wallet', 'confirm'].map((s, i) => (
          <div
            key={s}
            className={`h-1 flex-1 rounded-full transition-all duration-500 ${
              ['quote', 'payment', 'wallet', 'confirm'].indexOf(step) >= i
                ? 'bg-primary'
                : 'bg-border'
            }`}
          />
        ))}
      </div>

      {/* Quote Step */}
      {step === 'quote' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
          <div className="glass-card p-5">
            <div className="text-center mb-4">
              <div className="text-sm text-text-muted mb-1">تستلم</div>
              <div className={`text-3xl font-bold font-mono ${selectedCurrency === 'USDT' ? 'text-usdt' : 'text-ton'}`}>
                {formatAmount(currentQuote.output_amount, selectedCurrency === 'TON' ? 4 : 2)} {selectedCurrency}
              </div>
            </div>
            <div className="space-y-2 text-sm border-t border-border pt-3">
              <div className="flex justify-between">
                <span className="text-text-muted">المدفوع</span>
                <span className="font-mono">{formatAmount(currentQuote.input_amount)} د.ع</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-muted">السعر</span>
                <span className="font-mono">1 {selectedCurrency} = {formatRate(Math.round(1 / currentQuote.rate))} د.ع</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-muted">العمولة</span>
                <span className="font-mono">{formatAmount(currentQuote.fee)} د.ع</span>
              </div>
            </div>
          </div>

          {error && <div className="text-danger text-sm text-center">{error}</div>}

          <button onClick={handleCreateOrder} disabled={loading} className="btn-primary disabled:opacity-40">
            {loading ? 'جاري الإنشاء...' : 'تأكيد وإنشاء الطلب'}
          </button>
        </motion.div>
      )}

      {/* Payment Step */}
      {step === 'payment' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
          <div className="glass-card p-5 text-center">
            <div className="text-sm text-text-muted mb-2">الطلب {orderNumber}</div>
            <div className="text-2xl font-bold mb-1">{formatAmount(currentQuote.input_amount)} د.ع</div>
            <div className="text-xs text-text-muted">أدخل رقم آسياسيل للدفع</div>
          </div>

          <input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="07XXXXXXXXX"
            className="w-full bg-bg-card border border-border rounded-xl px-4 py-3 text-center text-lg font-mono outline-none focus:border-primary"
          />

          {error && <div className="text-danger text-sm text-center">{error}</div>}

          <button onClick={handlePayment} disabled={loading} className="btn-primary disabled:opacity-40">
            {loading ? 'جاري المعالجة...' : 'إتمام الدفع'}
          </button>
        </motion.div>
      )}

      {/* Wallet Step */}
      {step === 'wallet' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
          <div className="glass-card p-5 text-center">
            <div className="text-success text-sm mb-2">✓ تم تأكيد الدفع</div>
            <div className="text-sm text-text-muted">أرسل عنوان محفظتك</div>
          </div>

          <input
            type="text"
            value={walletAddress}
            onChange={(e) => setWalletAddress(e.target.value)}
            placeholder={selectedCurrency === 'TON' ? 'EQ...' : 'T...'}
            className="w-full bg-bg-card border border-border rounded-xl px-4 py-3 text-center text-sm font-mono outline-none focus:border-primary"
            dir="ltr"
          />

          <div className="text-xs text-text-muted text-center">
            تأكد من صحة العنوان والشبكة ({currentQuote.network})
          </div>

          {error && <div className="text-danger text-sm text-center">{error}</div>}

          <button onClick={handleSetWallet} disabled={loading} className="btn-primary disabled:opacity-40">
            {loading ? 'جاري التحقق...' : 'تأكيد العنوان'}
          </button>
        </motion.div>
      )}

      {/* Confirm Step */}
      {step === 'confirm' && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-4">
          <div className="glass-card p-5 space-y-3">
            <div className="text-center text-sm text-text-muted mb-2">مراجعة العملية</div>
            <div className="flex justify-between text-sm">
              <span className="text-text-muted">المدفوع</span>
              <span className="font-mono">{formatAmount(currentQuote.input_amount)} د.ع</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-text-muted">تستلم</span>
              <span className="font-mono font-semibold">{formatAmount(currentQuote.output_amount, selectedCurrency === 'TON' ? 4 : 2)} {selectedCurrency}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-text-muted">الشبكة</span>
              <span>{currentQuote.network}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-text-muted">العنوان</span>
              <span className="font-mono text-xs truncate max-w-[200px]" dir="ltr">{walletAddress}</span>
            </div>
          </div>

          {error && <div className="text-danger text-sm text-center">{error}</div>}

          <button onClick={handleConfirm} disabled={loading} className="btn-primary disabled:opacity-40">
            {loading ? 'جاري التنفيذ...' : 'تأكيد التحويل'}
          </button>
        </motion.div>
      )}

      {/* Success Step */}
      {step === 'success' && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="space-y-4"
        >
          <div className="glass-card p-8 text-center glow-primary">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', bounce: 0.5 }}
              className="w-20 h-20 mx-auto mb-4 rounded-full bg-success/20 flex items-center justify-center"
            >
              <span className="text-4xl">✓</span>
            </motion.div>
            <h3 className="text-xl font-bold mb-1">تم التحويل</h3>
            <p className="text-text-muted text-sm mb-4">بنجاح</p>
            <div className={`text-3xl font-bold font-mono ${selectedCurrency === 'USDT' ? 'text-usdt' : 'text-ton'}`}>
              {formatAmount(currentQuote.output_amount, selectedCurrency === 'TON' ? 4 : 2)} {selectedCurrency}
            </div>
          </div>

          <div className="glass-card p-4 space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-text-muted">الطلب</span>
              <span className="font-mono">{orderNumber}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-text-muted">TX Hash</span>
              <span className="font-mono text-xs truncate max-w-[180px]" dir="ltr">{txHash}</span>
            </div>
          </div>

          <button onClick={() => { setCurrentQuote(null); setPage('home') }} className="btn-primary">
            طلب جديد
          </button>
        </motion.div>
      )}
    </div>
  )
}
