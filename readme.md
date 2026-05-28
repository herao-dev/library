# 图书管理系统 (Library Management System)

基于 Flask 框架的 Python Web 图书管理系统，支持图书的增删改查、借阅归还、用户管理等功能。

---

## 一、技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
| **后端框架** | Flask 3.x | 轻量级 Python Web 框架 |
| **模板引擎** | Jinja2 | Flask 内置，服务端渲染页面 |
| **ORM** | Flask-SQLAlchemy | 数据库对象关系映射 |
| **数据库** | SQLite（开发）/ MySQL（生产） | 关系型数据库 |
| **数据库迁移** | Flask-Migrate (Alembic) | 数据库版本管理 |
| **表单处理** | Flask-WTF | 表单验证与 CSRF 保护 |
| **用户认证** | Flask-Login | 会话管理与登录状态 |
| **密码加密** | Werkzeug Security | 密码哈希 |
| **前端框架** | Vue 3 + TypeScript | SPA 单页应用 |
| **前端构建** | Vite | 前端构建工具 |
| **前端路由** | Vue Router | 前端路由管理 |
| **前端状态** | Pinia | 状态管理 |
| **前端样式** | Bootstrap 5 | 响应式 UI 框架 |
| **前端图标** | Bootstrap Icons | 图标库 |
| **分页** | Flask-SQLAlchemy 内置分页 | 数据分页 |

项目包含两套前端界面：Jinja2 模板渲染页面（`templates/`）和 Vue 3 SPA 单页应用（`frontend/`）。

---

## 二、用户角色

| 角色 | 权限描述 |
|------|---------|
| **管理员 (Admin)** | 图书管理、用户管理、借阅管理、查看统计报表 |
| **普通用户 (User)** | 浏览图书、搜索图书、借阅/归还图书、查看个人借阅记录 |

---

## 三、页面规划

### 3.1 公共页面（无需登录）

| 页面名称 | 路由 | 模板文件 | 功能描述 |
|---------|------|---------|---------|
| 登录页 | `/auth/login` | `auth/login.html` | 用户名 + 密码登录表单 |
| 注册页 | `/auth/register` | `auth/register.html` | 新用户注册表单 |

### 3.2 管理员页面

<img width="1247" height="608" alt="58e48885ce436290778759a926a0c770" src="https://github.com/user-attachments/assets/b39adf8d-db26-4c57-b9eb-f2a82596dbd5" />


### 3.3 普通用户页面

<img width="1243" height="604" alt="32676e8ae09e37917f3ab3d019ced295" src="https://github.com/user-attachments/assets/24947afb-dc59-4ed8-bffa-a2a8f3ce46ae" />





---

## 四、启动方式

```bash
# 1. 克隆项目
git clone <repo-url>
cd finish

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Linux/Mac

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量（复制 .env.example 为 .env 并修改）
cp .env.example .env

# 5. 初始化数据库
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 6. 填充种子数据（可选）
flask seed

# 7. 启动开发服务器
flask run
# 或
python run.py
```

访问 `http://localhost:5000` 即可使用。

**默认管理员账号**（种子数据创建）：
- 用户名：`admin`
- 密码：`admin123`
<img width="1244" height="607" alt="b64edaf39b067b652d85ee364d7a1ac5" src="https://github.com/user-attachments/assets/2badf844-3274-4923-986d-e4c525cdac68" />

<img width="1246" height="605" alt="9b715f405db47d30dc88635034f5e7ae" src="https://github.com/user-attachments/assets/b9b18864-e873-424d-a461-93fc2bd17f92" />

<img width="1243" height="375" alt="0d3489ad7719ee97fa72e97e62cad29c" src="https://github.com/user-attachments/assets/0ce043b6-46e1-43cb-8bb6-255ec48832f9" />



