/**
 * 主布局组件
 */
import { ReactNode } from 'react'
import Header from './Header'
import Sidebar from './Sidebar'

interface MainLayoutProps {
  children: ReactNode
}

const MainLayout = ({ children }: MainLayoutProps) => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 ml-64 p-6">
          <div className="container mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default MainLayout
