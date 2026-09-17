export interface Rate {
  currency: string
  network: string
  rate: number
  fee_type: string
  fee_value: number
  min_amount: number
  max_amount: number
  active: boolean
  updated_at?: string
}

export interface Quote {
  quote_id: string
  currency: string
  network: string
  input_amount: number
  rate: number
  fee: number
  output_amount: number
  expires_at: string
  remaining_seconds: number
}

export interface Order {
  id: number
  order_number: string
  input_currency: string
  input_amount: number
  output_currency: string
  output_amount: number
  network: string
  exchange_rate: number
  fee: number
  wallet_address?: string
  status: string
  created_at?: string
  completed_at?: string
}

export interface Wallet {
  id: number
  currency: string
  network: string
  address: string
  label?: string
  is_default: boolean
}

export interface User {
  id: number
  telegram_id: number
  username?: string
}

export interface Stats {
  total_users: number
  total_orders: number
  pending_orders: number
  completed_orders: number
  total_volume: number
}

export type Page = 'home' | 'exchange' | 'orders' | 'wallet' | 'profile' | 'admin'
