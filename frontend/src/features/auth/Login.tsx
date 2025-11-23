/**
 * 登录页面
 */
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authService } from '@/services/auth.service'
import { useAuthStore } from '@/store/authStore'
import Button from '@/components/common/Button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/common/Card'

const Login = () => {
  const navigate = useNavigate()
  const fetchCurrentUser = useAuthStore((state) => state.fetchCurrentUser)
  
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await authService.login(formData)
      await fetchCurrentUser()
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || '登录失败，请检查用户名和密码')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">欢迎回来</CardTitle>
          <CardDescription className="text-center">
            登录到个人成长管理系统
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-red-500 bg-red-50 border border-red-200 rounded-md">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <label htmlFor="username" className="text-sm font-medium">
                用户名或邮箱
              </label>
              <input
                id="username"
                type="text"
                required
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                placeholder="请输入用户名或邮箱"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">
                密码
              </label>
              <input
                id="password"
                type="password"
                required
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                placeholder="请输入密码"
              />
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? '登录中...' : '登录'}
            </Button>

            <div className="text-center text-sm text-muted-foreground">
              还没有账号？{' '}
              <Link to="/register" className="text-primary hover:underline">
                立即注册
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default Login
