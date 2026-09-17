import { ReactNode } from 'react'
import { BottomNav } from './BottomNav'

interface Props {
  children: ReactNode
}

export function AppShell({ children }: Props) {
  return (
    <div className="min-h-[100dvh] flex flex-col bg-bg">
      <div className="flex-1 overflow-y-auto no-scrollbar pb-24">
        {children}
      </div>
      <BottomNav />
    </div>
  )
}
