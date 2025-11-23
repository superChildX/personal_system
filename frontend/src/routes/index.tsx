/**
 * 路由配置
 */
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import { useAuthStore } from '@/store/authStore'
import MainLayout from '@/components/layout/MainLayout'

// 页面组件（延迟加载）
import Login from '@/features/auth/Login'
import Register from '@/features/auth/Register'
import Dashboard from '@/features/dashboard/Dashboard'

// 私有路由组件
const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

// 路由器组件
const AppRouter = () => {
  const { fetchCurrentUser, isAuthenticated } = useAuthStore()

  useEffect(() => {
    if (isAuthenticated) {
      fetchCurrentUser()
    }
  }, [isAuthenticated, fetchCurrentUser])

  return (
    <BrowserRouter>
      <Routes>
        {/* 公开路由 */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* 私有路由 */}
        <Route
          path="/*"
          element={
            <PrivateRoute>
              <MainLayout>
                <Routes>
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  {/* 其他路由将在后续添加 */}
                  <Route path="*" element={<div className="text-center py-12">页面开发中...</div>} />
                </Routes>
              </MainLayout>
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRouter
