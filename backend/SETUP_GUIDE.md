# 🚀 后端环境配置指南

## 第1步：激活Conda环境并安装依赖

```bash
# 切换到backend目录
cd /home/amazing/projects/personal_system/backend

# 激活conda虚拟环境
conda activate personal-system

# 安装Python依赖
pip install -r requirements.txt
```

## 第2步：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件（如果需要修改数据库密码等配置）
# 默认配置已经符合你的环境（root/123456），可以直接使用
```

## 第3步：创建数据库

```bash
# 连接到MySQL
mysql -u root -p123456

# 在MySQL中执行
CREATE DATABASE personal_growth_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;
```

## 第4步：初始化数据库表

```bash
# 在backend目录下，确保conda环境已激活
python init_db.py
```

## 第5步：启动FastAPI服务

```bash
# 开发模式（热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 访问API文档

启动成功后，访问：
- 🌐 API文档: http://localhost:8000/api/v1/docs
- 📖 ReDoc: http://localhost:8000/api/v1/redoc
- ❤️ 健康检查: http://localhost:8000/health

---

## ⚠️ 常见问题

### Q1: pip命令找不到？
**A**: 确保已激活conda环境：`conda activate personal-system`

### Q2: MySQL连接失败？
**A**: 检查MySQL服务是否启动，以及 `.env` 中的数据库配置是否正确

### Q3: 模块导入错误？
**A**: 确保在backend目录下运行命令，且依赖已正确安装

---

## 📋 完成检查清单

- [ ] ✅ 激活conda环境
- [ ] ✅ 安装Python依赖
- [ ] ✅ 创建MySQL数据库
- [ ] ✅ 初始化数据库表（27张表）
- [ ] ✅ 启动FastAPI服务
- [ ] ✅ 访问API文档验证
