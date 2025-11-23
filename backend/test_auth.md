# 用户认证系统测试指南

## 🚀 启动服务

```bash
# 确保在backend目录下，并激活conda环境
cd /home/amazing/projects/personal_system/backend
conda activate personal-system

# 启动FastAPI服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📖 访问API文档

启动成功后访问：
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

## 🧪 测试认证API

### 1. 用户注册

**接口**: `POST /api/v1/auth/register`

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "123456",
    "full_name": "测试用户"
  }'
```

**预期响应**（201 Created）：
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "测试用户",
  "avatar_url": null,
  "github_username": null,
  "linkedin_url": null,
  "created_at": "2025-11-23T19:40:00",
  "updated_at": "2025-11-23T19:40:00"
}
```

---

### 2. 用户登录（OAuth2密码流）

**接口**: `POST /api/v1/auth/login`

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=123456"
```

**预期响应**（200 OK）：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### 3. 用户登录（JSON格式）

**接口**: `POST /api/v1/auth/login/json`

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login/json" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "123456"
  }'
```

---

### 4. 获取当前用户信息

**接口**: `GET /api/v1/auth/me`

```bash
# 先登录获取token
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=123456" | jq -r '.access_token')

# 使用token获取用户信息
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

**预期响应**（200 OK）：
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "测试用户",
  "avatar_url": null,
  "github_username": null,
  "linkedin_url": null,
  "created_at": "2025-11-23T19:40:00",
  "updated_at": "2025-11-23T19:40:00"
}
```

---

### 5. 测试JWT令牌

**接口**: `POST /api/v1/auth/test-token`

```bash
curl -X POST "http://localhost:8000/api/v1/auth/test-token" \
  -H "Authorization: Bearer $TOKEN"
```

---

### 6. 更新用户信息

**接口**: `PUT /api/v1/users/me`

```bash
curl -X PUT "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "新名字",
    "github_username": "testuser",
    "linkedin_url": "https://linkedin.com/in/testuser"
  }'
```

---

### 7. 获取个人档案

**接口**: `GET /api/v1/users/me/profile`

```bash
curl -X GET "http://localhost:8000/api/v1/users/me/profile" \
  -H "Authorization: Bearer $TOKEN"
```

---

### 8. 更新个人档案

**接口**: `PUT /api/v1/users/me/profile`

```bash
curl -X PUT "http://localhost:8000/api/v1/users/me/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "13800138000",
    "bio": "这是我的个人简介",
    "current_position": "软件工程师",
    "location": "北京",
    "website": "https://example.com"
  }'
```

---

## 🔍 在Swagger UI中测试

1. 访问 http://localhost:8000/api/v1/docs

2. **注册用户**：
   - 展开 `POST /api/v1/auth/register`
   - 点击 "Try it out"
   - 填写JSON数据
   - 点击 "Execute"

3. **登录获取Token**：
   - 展开 `POST /api/v1/auth/login`
   - 点击 "Try it out"
   - 填写username和password
   - 点击 "Execute"
   - 复制返回的 `access_token`

4. **设置认证Token**：
   - 点击页面右上角的 "Authorize" 按钮
   - 在弹窗中输入：`Bearer <你的token>`
   - 点击 "Authorize"

5. **测试需要认证的接口**：
   - 现在可以测试所有需要认证的接口了
   - 例如：`GET /api/v1/auth/me`

---

## ⚠️ 常见错误

### 1. 401 Unauthorized
- 检查JWT令牌是否正确
- 检查令牌是否已过期（默认7天）
- 确保请求头格式：`Authorization: Bearer <token>`

### 2. 400 Bad Request - "用户名已存在"
- 尝试使用不同的用户名

### 3. 400 Bad Request - "邮箱已被注册"
- 尝试使用不同的邮箱

### 4. 401 Unauthorized - "用户名或密码错误"
- 检查用户名和密码是否正确
- 用户名可以是username或email

---

## ✅ 功能清单

- [x] 用户注册（密码bcrypt加密）
- [x] 用户登录（OAuth2密码流）
- [x] 用户登录（JSON格式）
- [x] JWT令牌生成（7天过期）
- [x] JWT令牌验证
- [x] 获取当前用户信息
- [x] 更新用户信息
- [x] 自动创建个人档案
- [x] 获取个人档案
- [x] 更新个人档案
- [x] 认证依赖项（Bearer Token）
- [x] 支持用户名或邮箱登录

---

## 📊 数据库表状态

注册用户后，数据库会自动创建：
- `users` 表：用户基本信息（密码已哈希）
- `profiles` 表：用户个人档案（自动创建）
