/**
 * 顶部导航栏组件
 */
import { Link } from 'react-router-dom'
import { User, LogOut } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import Button from '../common/Button'

const Header = () => {
  const { user, logout } = useAuthStore()

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-6">
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-xl font-bold">个人成长系统</span>
          </Link>
          
          <nav className="hidden md:flex gap-6">
            <Link to="/dashboard" className="text-sm font-medium hover:text-primary">
              数据看板
            </Link>
            <Link to="/projects" className="text-sm font-medium hover:text-primary">
              项目管理
            </Link>
            <Link to="/notes" className="text-sm font-medium hover:text-primary">
              学习笔记
            </Link>
            <Link to="/time" className="text-sm font-medium hover:text-primary">
              时间管理
            </Link>
          </nav>
        </div>

        <div className="flex items-center gap-4">
          {user ? (
            <>
              <Link to="/profile" className="flex items-center gap-2 text-sm hover:text-primary">
                <User className="h-4 w-4" />
                <span>{user.full_name || user.username}</span>
              </Link>
              <Button variant="ghost" size="sm" onClick={logout}>
                <LogOut className="h-4 w-4 mr-2" />
                退出
              </Button>
            </>
          ) : (
            <Link to="/login">
              <Button>登录</Button>
            </Link>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header
