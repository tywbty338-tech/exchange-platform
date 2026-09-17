import { useStore } from '../../store'
import type { Page } from '../../types'

const tabs: { id: Page; icon: string; label: string }[] = [
  { id: 'home', icon: '🏠', label: 'الرئيسية' },
  { id: 'exchange', icon: '💱', label: 'تحويل' },
  { id: 'orders', icon: '📋', label: 'طلباتي' },
  { id: 'wallet', icon: '💼', label: 'محفظتي' },
  { id: 'profile', icon: '👤', label: 'حسابي' },
]

export function BottomNav() {
  const { page, setPage } = useStore()

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50">
      <div className="glass border-t border-border">
        <div className="flex items-center justify-around max-w-lg mx-auto h-16">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setPage(tab.id)}
              className={`flex flex-col items-center gap-0.5 px-3 py-1 transition-all duration-200 ${
                page === tab.id
                  ? 'text-primary scale-105'
                  : 'text-text-muted active:scale-95'
              }`}
            >
              <span className="text-xl">{tab.icon}</span>
              <span className="text-[10px] font-medium">{tab.label}</span>
              {page === tab.id && (
                <div className="w-4 h-0.5 bg-primary rounded-full mt-0.5" />
              )}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
