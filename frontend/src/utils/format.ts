export function formatAmount(n: number, decimals = 0): string {
  if (decimals === 0) return Math.round(n).toLocaleString('en-US')
  return n.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals })
}

export function formatRate(rate: number): string {
  if (rate >= 1) return Math.round(rate).toLocaleString('en-US')
  return rate.toFixed(6)
}

export function timeAgo(date: string | Date): string {
  const now = new Date()
  const d = typeof date === 'string' ? new Date(date) : date
  const seconds = Math.floor((now.getTime() - d.getTime()) / 1000)
  if (seconds < 60) return `منذ ${seconds} ثانية`
  if (seconds < 3600) return `منذ ${Math.floor(seconds / 60)} دقيقة`
  if (seconds < 86400) return `منذ ${Math.floor(seconds / 3600)} ساعة`
  return `منذ ${Math.floor(seconds / 86400)} يوم`
}

export function statusInfo(status: string): { emoji: string; label: string; color: string } {
  const map: Record<string, { emoji: string; label: string; color: string }> = {
    CREATED: { emoji: '🆕', label: 'جديد', color: 'text-text-secondary' },
    QUOTE_CREATED: { emoji: '📋', label: 'تم إنشاء السعر', color: 'text-text-secondary' },
    WAITING_PAYMENT: { emoji: '💳', label: 'بانتظار الدفع', color: 'text-warning' },
    PAYMENT_PROCESSING: { emoji: '⏳', label: 'قيد المعالجة', color: 'text-warning' },
    PAYMENT_CONFIRMED: { emoji: '✅', label: 'تم التأكيد', color: 'text-success' },
    WAITING_WALLET: { emoji: '📥', label: 'بانتظار العنوان', color: 'text-ton' },
    WALLET_CONFIRMED: { emoji: '✔️', label: 'تم تأكيد العنوان', color: 'text-success' },
    PROCESSING: { emoji: '⏳', label: 'جاري التنفيذ', color: 'text-primary' },
    SENT: { emoji: '📤', label: 'تم الإرسال', color: 'text-primary' },
    COMPLETED: { emoji: '🎉', label: 'مكتملة', color: 'text-success' },
    REJECTED: { emoji: '❌', label: 'مرفوضة', color: 'text-danger' },
    CANCELLED: { emoji: '🚫', label: 'ملغاة', color: 'text-text-muted' },
    PAYMENT_FAILED: { emoji: '❌', label: 'فشل الدفع', color: 'text-danger' },
    TRANSFER_FAILED: { emoji: '❌', label: 'فشل التحويل', color: 'text-danger' },
  }
  return map[status] || { emoji: '❓', label: status, color: 'text-text-muted' }
}
