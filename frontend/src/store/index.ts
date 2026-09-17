import { create } from 'zustand'
import type { Rate, Quote, Order, Wallet, User, Page } from '../types'

interface AppState {
  page: Page
  setPage: (page: Page) => void

  rates: Rate[]
  setRates: (rates: Rate[]) => void

  currentQuote: Quote | null
  setCurrentQuote: (quote: Quote | null) => void

  orders: Order[]
  setOrders: (orders: Order[]) => void

  wallets: Wallet[]
  setWallets: (wallets: Wallet[]) => void

  user: User | null
  setUser: (user: User | null) => void

  selectedCurrency: 'USDT' | 'TON'
  setSelectedCurrency: (c: 'USDT' | 'TON') => void

  inputAmount: string
  setInputAmount: (a: string) => void

  loading: boolean
  setLoading: (l: boolean) => void
}

export const useStore = create<AppState>((set) => ({
  page: 'home',
  setPage: (page) => set({ page }),

  rates: [],
  setRates: (rates) => set({ rates }),

  currentQuote: null,
  setCurrentQuote: (quote) => set({ currentQuote: quote }),

  orders: [],
  setOrders: (orders) => set({ orders }),

  wallets: [],
  setWallets: (wallets) => set({ wallets }),

  user: null,
  setUser: (user) => set({ user }),

  selectedCurrency: 'USDT',
  setSelectedCurrency: (selectedCurrency) => set({ selectedCurrency }),

  inputAmount: '',
  setInputAmount: (inputAmount) => set({ inputAmount }),

  loading: false,
  setLoading: (loading) => set({ loading }),
}))
