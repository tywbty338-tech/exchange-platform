const API_BASE = '/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = localStorage.getItem('token')
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...((options?.headers as Record<string, string>) || {}),
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(error.detail || `HTTP ${res.status}`)
  }

  return res.json()
}

export const api = {
  getRates: () => request<any[]>('/rates'),

  createQuote: (data: { currency: string; network: string; input_amount: number }) =>
    request<any>('/quotes', { method: 'POST', body: JSON.stringify(data) }),

  getQuote: (quoteId: string) => request<any>(`/quotes/${quoteId}`),

  createOrder: (quoteId: string) =>
    request<any>('/orders', { method: 'POST', body: JSON.stringify({ quote_id: quoteId }) }),

  getOrders: () => request<any[]>('/orders'),

  getOrder: (id: number) => request<any>(`/orders/${id}`),

  setWallet: (orderId: number, address: string) =>
    request<any>(`/orders/${orderId}/wallet`, { method: 'POST', body: JSON.stringify({ wallet_address: address }) }),

  confirmOrder: (orderId: number) =>
    request<any>(`/orders/${orderId}/confirm`, { method: 'POST' }),

  getWallets: () => request<any[]>('/wallets'),

  createWallet: (data: any) =>
    request<any>('/wallets', { method: 'POST', body: JSON.stringify(data) }),

  deleteWallet: (id: number) =>
    request<any>(`/wallets/${id}`, { method: 'DELETE' }),

  getAdminStats: () => request<any>('/admin/stats'),

  getAdminRates: () => request<any[]>('/admin/rates'),

  updateAdminRate: (currency: string, network: string, data: any) =>
    request<any>(`/admin/rates/${currency}/${network}`, { method: 'PUT', body: JSON.stringify(data) }),

  authTelegram: (initData: string) =>
    request<any>('/auth/telegram', { method: 'POST', body: JSON.stringify({ init_data: initData }) }),
}
