# 个人成长管理系统 - 前端

React + TypeScript + Vite + TailwindCSS 前端应用

## 🛠️ 技术栈

- **React 19** - UI框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具
- **TailwindCSS** - 样式系统
- **React Router v6** - 路由管理
- **Zustand** - 状态管理
- **Axios** - HTTP客户端
- **Lucide React** - 图标库
- **Ant Design** - UI组件库
- **Recharts** - 图表库

## 🚀 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 3. 构建生产版本

```bash
npm run build
```

### 4. 预览生产构建

```bash
npm run preview
```

## 📁 项目结构

```
src/
├── assets/          # 静态资源
├── components/      # 通用组件
│   ├── common/      # Button, Card, Input等
│   ├── layout/      # Header, Sidebar, MainLayout
│   └── widgets/     # 业务组件
├── features/        # 功能模块页面
│   ├── auth/        # 登录/注册
│   ├── dashboard/   # 数据看板
│   ├── projects/    # 项目管理
│   └── ...
├── hooks/           # 自定义Hooks
├── services/        # API服务层
├── store/           # Zustand状态管理
├── types/           # TypeScript类型
├── utils/           # 工具函数
└── routes/          # 路由配置
```

## ✨ 已实现的功能

- ✅ 用户认证（登录/注册）
- ✅ JWT Token管理
- ✅ 私有路由保护
- ✅ 响应式布局
- ✅ 暗色/亮色主题支持
- ✅ API请求拦截器
- ✅ 基础UI组件库

## 📖 详细文档

查看 [SETUP_GUIDE.md](./SETUP_GUIDE.md) 了解：
- 完整的配置步骤
- 项目架构说明
- 组件使用指南
- 常见问题解答

## 🔗 API代理

开发模式下，所有 `/api` 请求会自动代理到后端服务：
- 前端: http://localhost:5173
- 后端: http://localhost:8000

## 🎨 样式系统

使用 TailwindCSS + CSS Variables 实现：
- 支持暗色模式
- 完全可定制的颜色主题
- Utility-first CSS

## 📦 主要依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| react | ^19.2.0 | UI框架 |
| react-router-dom | ^6.22.0 | 路由管理 |
| zustand | ^4.5.0 | 状态管理 |
| axios | ^1.6.7 | HTTP客户端 |
| tailwindcss | ^3.4.1 | 样式系统 |
| lucide-react | ^0.323.0 | 图标 |
| antd | ^5.13.3 | UI组件 |

## 🔧 开发指南

### 路径别名

使用 `@/` 作为 `src/` 的别名：

```typescript
import { cn } from '@/utils/cn'
import { useAuthStore } from '@/store/authStore'
```

### 组件开发

基于 shadcn/ui 风格的组件：

```typescript
import Button from '@/components/common/Button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/common/Card'

<Button variant="default" size="lg">点击我</Button>
<Card>
  <CardHeader>
    <CardTitle>标题</CardTitle>
  </CardHeader>
  <CardContent>内容</CardContent>
</Card>
```

### 状态管理

使用 Zustand 管理全局状态：

```typescript
import { useAuthStore } from '@/store/authStore'

const MyComponent = () => {
  const { user, logout } = useAuthStore()
  
  return <div>{user?.username}</div>
}
```

## 📝 可用脚本

```bash
npm run dev      # 启动开发服务器
npm run build    # 构建生产版本
npm run preview  # 预览生产构建
npm run lint     # 运行ESLint检查
```

## 🤝 贡献

这是个人项目，仅供学习使用。

## 📄 License

MIT
