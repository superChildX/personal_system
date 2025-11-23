/**
 * 数据看板页面
 */
import { useAuthStore } from '@/store/authStore'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/common/Card'
import { LayoutDashboard, FolderKanban, BookOpen, Clock } from 'lucide-react'

const Dashboard = () => {
  const user = useAuthStore((state) => state.user)

  const stats = [
    { icon: FolderKanban, label: '项目数量', value: '0', color: 'text-blue-500' },
    { icon: BookOpen, label: '学习笔记', value: '0', color: 'text-green-500' },
    { icon: Clock, label: '学习时长', value: '0h', color: 'text-orange-500' },
    { icon: LayoutDashboard, label: '完成任务', value: '0', color: 'text-purple-500' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">欢迎回来，{user?.full_name || user?.username}!</h1>
        <p className="text-muted-foreground mt-2">这是你的个人成长数据看板</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <Card key={stat.label}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{stat.label}</CardTitle>
                <Icon className={`h-4 w-4 ${stat.color}`} />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>最近项目</CardTitle>
            <CardDescription>你最近的项目活动</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">暂无项目数据</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>学习进度</CardTitle>
            <CardDescription>本周学习统计</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">暂无学习数据</p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard
