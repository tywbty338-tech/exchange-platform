import { useEffect } from 'react'
import { useStore } from './store'
import { api } from './services/api'
import { AppShell } from './components/layout/AppShell'
import { HomePage } from './pages/HomePage'
import { ExchangePage } from './pages/ExchangePage'
import { OrdersPage } from './pages/OrdersPage'
import { WalletPage } from './pages/WalletPage'
import { ProfilePage } from './pages/ProfilePage'

export default function App() {
  const { page, setRates } = useStore()

  useEffect(() => {
    const loadRates = async () => {
      try {
        const rates = await api.getRates()
        setRates(rates)
      } catch (e) {
        console.error('Failed to load rates:', e)
      }
    }
    loadRates()
    const interval = setInterval(loadRates, 30000)
    return () => clearInterval(interval)
  }, [setRates])

  const renderPage = () => {
    switch (page) {
      case 'home': return <HomePage />
      case 'exchange': return <ExchangePage />
      case 'orders': return <OrdersPage />
      case 'wallet': return <WalletPage />
      case 'profile': return <ProfilePage />
      default: return <HomePage />
    }
  }

  return (
    <AppShell>
      {renderPage()}
    </AppShell>
  )
}
