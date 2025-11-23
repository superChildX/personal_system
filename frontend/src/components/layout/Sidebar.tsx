/**
 * 侧边栏导航组件
 */
import { Link, useLocation } from 'react-router-dom'
import {
  LayoutDashboard,
  FolderKanban,
  BookOpen,
  Clock,
  Calendar,
  Target,
  Brain,
  Award,
  Users,
  Lightbulb,
  Box,
} from 'lucide-react'
import { cn } from '@/utils/cn'

const menuItems = [
  { icon: LayoutDashboard, label: '数据看板', path: '/dashboard' },
  { icon: FolderKanban, label: '项目管理', path: '/projects' },
  { icon: BookOpen, label: '学习笔记', path: '/notes' },
  { icon: Clock, label: '时间管理', path: '/time' },
  { icon: Calendar, label: '每日记录', path: '/daily' },
  { icon: Target, label: '目标复盘', path: '/goals' },
  { icon: Brain, label: '知识库', path: '/knowledge' },
  { icon: Award, label: '经历记录', path: '/experience' },
  { icon: Users, label: '社交网络', path: '/network' },
  { icon: Lightbulb, label: '灵感捕捉', path: '/ideas' },
  { icon: Box, label: '资源管理', path: '/resources' },
]

const Sidebar = () => {
  const location = useLocation()

  return (
    <aside className="fixed left-0 top-16 z-40 h-[calc(100vh-4rem)] w-64 border-r bg-background">
      <div className="flex flex-col gap-1 p-4">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path

          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-all hover:bg-accent',
                isActive
                  ? 'bg-accent text-accent-foreground font-medium'
                  : 'text-muted-foreground'
              )}
            >
              <Icon className="h-4 w-4" />
              <span>{item.label}</span>
            </Link>
          )
        })}
      </div>
    </aside>
  )
}

export default Sidebar
