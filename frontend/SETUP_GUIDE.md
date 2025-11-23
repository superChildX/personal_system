# 🚀 前端项目配置指南

## ⚠️ 手动配置步骤

由于某些配置文件已存在，请按照以下步骤手动完成配置。

---

## 第1步：更新 `tsconfig.json`

打开 `/home/amazing/projects/personal_system/frontend/tsconfig.json`

找到 `"references"` 部分，在整个配置文件中添加或确保包含以下内容：

```json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

---

## 第2步：更新 `tsconfig.app.json`

打开 `/home/amazing/projects/personal_system/frontend/tsconfig.app.json`

确保包含以下配置：

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedSideEffectImports": true,

    /* Path alias */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"]
}
```

---

## 第3步：删除不需要的文件

```bash
cd /home/amazing/projects/personal_system/frontend
rm -f src/App.css src/assets/react.svg
```

---

## 第4步：安装依赖

```bash
cd /home/amazing/projects/personal_system/frontend
npm install
```

这将安装 `package.json` 中已经配置好的所有依赖：
- ✅ react-router-dom (路由)
- ✅ zustand (状态管理)
- ✅ axios (HTTP客户端)
- ✅ lucide-react (图标)
- ✅ antd (UI组件库)
- ✅ recharts (图表)
- ✅ tailwindcss (样式)
- ✅ 以及其他工具库

---

## 第5步：验证配置

安装完成后，所有的 lint 错误应该消失。

### 验证路径别名

在任意 TypeScript 文件中测试导入：
```typescript
import { cn } from '@/utils/cn'  // 应该不报错
```

### 验证Tailwind CSS

查看 `src/index.css`，应该看到：
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## 第6步：启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173 应该可以看到登录页面。

---

## 🎯 已完成的功能

### ✅ 前端基础架构
- Vite + React 18 + TypeScript
- TailwindCSS 样式系统
- 路径别名配置 (@/ 指向 src/)
- API代理配置 (代理到 http://localhost:8000)

### ✅ 核心服务层
- **API服务** (`src/services/api.ts`)
  - Axios 配置
  - 请求/响应拦截器
  - 自动添加 JWT Token
  - 401 自动跳转登录

- **认证服务** (`src/services/auth.service.ts`)
  - 用户注册
  - 用户登录
  - 获取当前用户
  - Token 管理

### ✅ 状态管理 (Zustand)
- **Auth Store** (`src/store/authStore.ts`)
  - 用户状态管理
  - 登录状态管理
  - 自动获取用户信息

### ✅ 类型定义
- **API类型** (`src/types/api.types.ts`)
- **用户类型** (`src/types/user.types.ts`)

### ✅ 基础UI组件
- **Button** (`src/components/common/Button.tsx`)
  - 多种变体 (default, destructive, outline等)
  - 多种尺寸
  - 支持 icon

- **Card** (`src/components/common/Card.tsx`)
  - CardHeader, CardTitle, CardDescription
  - CardContent, CardFooter
  - 完整的卡片组件系统

### ✅ 布局组件
- **Header** (`src/components/layout/Header.tsx`)
  - 顶部导航栏
  - 用户信息显示
  - 登录/退出功能

- **Sidebar** (`src/components/layout/Sidebar.tsx`)
  - 侧边栏导航
  - 14个功能模块入口
  - 路由高亮显示

- **MainLayout** (`src/components/layout/MainLayout.tsx`)
  - 主布局容器
  - Header + Sidebar + Content

### ✅ 路由配置
- **AppRouter** (`src/routes/index.tsx`)
  - React Router v6
  - 公开路由 (登录/注册)
  - 私有路由保护
  - 自动重定向

### ✅ 功能页面
- **登录页** (`src/features/auth/Login.tsx`)
  - 表单验证
  - 错误处理
  - 自动跳转

- **注册页** (`src/features/auth/Register.tsx`)
  - 完整注册流程
  - 密码确认
  - 注册后自动登录

- **Dashboard** (`src/features/dashboard/Dashboard.tsx`)
  - 数据统计卡片
  - 欢迎信息
  - 占位内容

---

## 📁 项目结构

```
frontend/
├── src/
│   ├── assets/              # 静态资源
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   ├── components/          # 通用组件
│   │   ├── common/          # Button, Card, Input等
│   │   ├── layout/          # Header, Sidebar, MainLayout
│   │   └── widgets/         # 业务组件（待开发）
│   ├── features/            # 功能模块页面
│   │   ├── auth/            # ✅ 登录/注册
│   │   ├── dashboard/       # ✅ 数据看板
│   │   ├── profile/         # 个人档案（待开发）
│   │   ├── projects/        # 项目管理（待开发）
│   │   ├── notes/           # 学习笔记（待开发）
│   │   ├── time/            # 时间管理（待开发）
│   │   ├── daily/           # 每日记录（待开发）
│   │   ├── goals/           # 目标复盘（待开发）
│   │   ├── knowledge/       # 知识库（待开发）
│   │   ├── experience/      # 经历记录（待开发）
│   │   ├── network/         # 社交网络（待开发）
│   │   ├── ideas/           # 灵感捕捉（待开发）
│   │   ├── resources/       # 资源管理（待开发）
│   │   └── tools/           # 创意工具（待开发）
│   ├── hooks/               # 自定义Hooks（待开发）
│   ├── services/            # ✅ API服务层
│   │   ├── api.ts
│   │   └── auth.service.ts
│   ├── store/               # ✅ Zustand状态管理
│   │   └── authStore.ts
│   ├── types/               # ✅ TypeScript类型
│   │   ├── api.types.ts
│   │   └── user.types.ts
│   ├── utils/               # ✅ 工具函数
│   │   └── cn.ts
│   ├── routes/              # ✅ 路由配置
│   │   └── index.tsx
│   ├── App.tsx              # ✅ 根组件
│   ├── main.tsx             # ✅ 入口文件
│   └── index.css            # ✅ TailwindCSS样式
├── public/                  # 公共资源
├── .gitignore
├── package.json             # ✅ 依赖配置
├── tsconfig.json            # ⚠️ 需要手动更新
├── tsconfig.app.json        # ⚠️ 需要手动更新
├── vite.config.ts           # ✅ Vite配置
├── tailwind.config.js       # ✅ Tailwind配置
├── postcss.config.js        # ✅ PostCSS配置
└── README.md
```

---

## 🎨 设计系统

### 颜色主题
- 支持亮色/暗色模式切换
- CSS变量驱动
- 使用HSL颜色空间

### 组件风格
- 基于 shadcn/ui 设计
- TailwindCSS 实现
- 完全可定制

---

## 🔧 常见问题

### Q1: npm install 失败？
**A**: 确保 Node.js 版本为 18+ 或 20+
```bash
node -v  # 应该显示 v18.x.x 或 v20.x.x 或更高
```

### Q2: 路径别名 @ 不工作？
**A**: 确保已按照第1步和第2步更新了 `tsconfig.json` 和 `tsconfig.app.json`

### Q3: Tailwind 样式不生效？
**A**: 检查 `postcss.config.js` 和 `tailwind.config.js` 是否正确配置

### Q4: API 请求 404？
**A**: 确保后端服务已启动在 http://localhost:8000

---

## 🚀 下一步

配置完成后，你可以：

1. **启动前端开发服务器**
   ```bash
   npm run dev
   ```

2. **启动后端服务器**
   ```bash
   cd ../backend
   conda activate personal-system
   uvicorn app.main:app --reload
   ```

3. **测试完整流程**
   - 访问 http://localhost:5173
   - 注册新用户
   - 登录系统
   - 查看Dashboard

4. **开始开发新功能**
   - 按照设计文档继续开发其他模块
   - 复用现有的组件和服务

---

**配置完成后，前端基础架构和基础UI组件库任务即可标记为完成！** ✅
