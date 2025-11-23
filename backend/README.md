# 个人成长管理系统 - 后端

FastAPI + MySQL 后端服务

## 🛠️ 技术栈

- **FastAPI** - 现代化Web框架
- **SQLAlchemy** - ORM
- **MySQL 8.0+** - 数据库
- **JWT** - 身份验证
- **Pydantic** - 数据验证

## 📦 环境准备

### 1. 激活Conda虚拟环境
```bash
conda activate personal-system
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
复制 `.env.example` 为 `.env` 并修改配置：
```bash
cp .env.example .env
# 然后编辑 .env 文件，修改数据库密码等敏感信息
```

## 🗄️ 数据库初始化

### 1. 创建数据库
```sql
mysql -u root -p
CREATE DATABASE personal_growth_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 初始化表结构
```bash
python init_db.py
```

### 3. 删除所有表（慎用！）
```bash
python init_db.py --drop
```

## 🚀 启动服务

### 开发模式（热重载）
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 生产模式
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📖 API文档

启动服务后访问：
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 📁 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── database.py          # 数据库连接
│   ├── models/              # SQLAlchemy模型（27张表）
│   ├── schemas/             # Pydantic验证模型
│   ├── api/v1/              # API路由
│   ├── crud/                # 数据库操作
│   ├── core/                # 核心功能（配置、安全）
│   └── utils/               # 工具函数
├── tests/                   # 测试代码
├── requirements.txt         # Python依赖
├── .env.example             # 环境变量模板
└── init_db.py               # 数据库初始化脚本
```

## 🗂️ 数据库表（27张）

### 用户相关 (4张)
- `users` - 用户表
- `profiles` - 个人档案
- `education` - 教育背景
- `skills` - 技能表

### 项目管理 (2张)
- `projects` - 项目表
- `project_images` - 项目截图

### 学习笔记 (2张)
- `notes` - 学习笔记
- `code_snippets` - 代码片段

### 经历记录 (1张)
- `experiences` - 经历记录

### 时间管理 (3张)
- `tasks` - Todo任务
- `pomodoro_sessions` - 番茄钟记录
- `schedules` - 日程安排

### 知识库 (3张)
- `interview_questions` - 面试题
- `leetcode_problems` - LeetCode刷题
- `resources` - 技术资源收藏

### 每日记录 (2张)
- `daily_records` - 每日记录
- `daily_tasks` - 每日任务明细

### 灵感捕捉 (2张)
- `ideas` - 灵感笔记
- `media_records` - 读书/电影记录

### 目标与复盘 (4张)
- `goals` - OKR目标
- `key_results` - 关键结果
- `habit_logs` - 习惯打卡
- `monthly_reviews` - 月度复盘

### 社交网络 (2张)
- `contacts` - 联系人
- `meetings` - 会议记录

### 其他 (2张)
- `tags` - 标签
- `attachments` - 附件

## 🔐 安全注意事项

- ✅ 密码使用bcrypt哈希存储
- ✅ JWT令牌过期时间7天
- ✅ 所有敏感信息存放在 `.env` 文件中
- ✅ `.env` 文件已加入 `.gitignore`
- ✅ 外键设置级联删除/SET NULL
- ✅ SQL注入防护（ORM参数化查询）

## 📝 开发规范

- 遵循 PEP 8 代码规范
- 使用类型注解（Type Hints）
- 数据库表名使用小写+下划线
- Python变量/函数使用snake_case
- 所有表必须包含 `created_at` 字段
- 更新类表必须包含 `updated_at` 字段
