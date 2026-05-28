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
| **前端样式** | Bootstrap 5 | 响应式 UI 框架 |
| **前端图标** | Bootstrap Icons | 图标库 |
| **分页** | Flask-SQLAlchemy 内置分页 | 数据分页 |

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

| 页面名称 | 路由 | 模板文件 | 功能描述 |
|---------|------|---------|---------|
| **管理后台首页** | `/admin/dashboard` | `admin/dashboard.html` | 统计概览：图书/用户/在借/逾期/预约/评论/罚金统计 + 最新动态 |
| **图书列表** | `/admin/books` | `admin/book_list.html` | 图书表格展示，支持搜索、分类筛选、分页 |
| **添加图书** | `/admin/books/add` | `admin/book_form.html` | 图书信息录入表单（书名、作者、ISBN、分类、库存等） |
| **编辑图书** | `/admin/books/<id>/edit` | `admin/book_form.html` | 复用添加表单，预填已有数据 |
| **图书详情** | `/admin/books/<id>` | `admin/book_detail.html` | 图书完整信息 + 借阅记录 |
| **分类管理** | `/admin/categories` | `admin/category_list.html` | 图书分类的增删改 |
| **用户列表** | `/admin/users` | `admin/user_list.html` | 用户表格展示，支持搜索、分页 |
| **添加用户** | `/admin/users/add` | `admin/user_form.html` | 管理员手动添加用户 |
| **编辑用户** | `/admin/users/<id>/edit` | `admin/user_form.html` | 编辑用户信息、重置密码 |
| **借阅管理** | `/admin/borrows` | `admin/borrow_list.html` | 所有借阅记录，支持按状态筛选（借出/已还/逾期），显示罚金 |
| **借书操作** | `/admin/borrows/add` | `admin/borrow_form.html` | 选择用户 + 选择图书，创建借阅记录 |
| **还书操作** | `/admin/borrows/<id>/return` | — | 确认归还，自动计算逾期罚金，更新库存 |
| **预约管理** | `/admin/reservations` | `admin/reservation_list.html` | 查看所有预约记录，支持按状态筛选、取消预约 |
| **评论管理** | `/admin/reviews` | `admin/review_list.html` | 查看所有评论，支持显示/隐藏、删除评论 |
| **公告管理** | `/admin/announcements` | `admin/announcement_list.html` | 公告列表，支持发布/编辑/上下架/删除 |
| **发布公告** | `/admin/announcements/add` | `admin/announcement_form.html` | 公告发布表单（标题、内容、优先级） |
| **编辑公告** | `/admin/announcements/<id>/edit` | `admin/announcement_form.html` | 编辑已有公告 |

### 3.3 普通用户页面

| 页面名称 | 路由 | 模板文件 | 功能描述 |
|---------|------|---------|---------|
| **用户首页** | `/user/dashboard` | `user/dashboard.html` | 个人借阅概览、推荐图书、最新公告 |
| **图书浏览** | `/user/books` | `user/book_list.html` | 图书卡片展示，支持搜索、分类筛选、分页 |
| **图书详情** | `/user/books/<id>` | `user/book_detail.html` | 图书详细信息 + 借阅/预约按钮 + 读者评论与评分 |
| **我的借阅** | `/user/borrows` | `user/borrow_list.html` | 个人借阅历史记录，显示逾期罚金 |
| **我的预约** | `/user/reservations` | `user/reservation_list.html` | 个人预约记录，支持取消预约 |
| **个人中心** | `/user/profile` | `user/profile.html` | 查看/编辑个人信息 |
| **修改密码** | `/user/change-password` | `user/change_password.html` | 修改登录密码 |

---

## 四、组件规划

### 4.1 布局组件

| 组件名称 | 模板文件 | 说明 |
|---------|---------|------|
| **基础布局** | `layouts/base.html` | 全局 HTML 骨架，引入 CSS/JS，定义 block 区域 |
| **管理端布局** | `layouts/admin.html` | 继承 base，包含侧边栏 + 顶栏 |
| **用户端布局** | `layouts/user.html` | 继承 base，包含导航栏 + 页脚 |
| **导航栏** | `components/navbar.html` | 顶部导航，含 Logo、菜单、用户下拉 |
| **侧边栏** | `components/sidebar.html` | 管理后台左侧菜单导航 |
| **页脚** | `components/footer.html` | 版权信息、链接 |

### 4.2 通用组件

| 组件名称 | 模板文件 | 说明 |
|---------|---------|------|
| **分页器** | `components/pagination.html` | 可复用的分页导航组件 |
| **搜索框** | `components/search_bar.html` | 带搜索按钮的输入框 |
| **图书卡片** | `components/book_card.html` | 封面图 + 书名 + 作者 + 状态标签 |
| **图书表格行** | `components/book_table_row.html` | 表格中的图书行 |
| **状态标签** | `components/status_badge.html` | 借阅状态标签（在借/已还/逾期） |
| **确认弹窗** | `components/confirm_modal.html` | 删除/归还等操作的确认对话框 |
| **消息提示** | `components/flash_messages.html` | Flask flash 消息的 Bootstrap Alert 渲染 |
| **空状态** | `components/empty_state.html` | 列表为空时的占位提示 |
| **加载动画** | `components/spinner.html` | 数据加载中的旋转动画 |

### 4.3 表单组件

| 组件名称 | 模板文件 | 说明 |
|---------|---------|------|
| **表单字段宏** | `macros/form_field.html` | Jinja2 宏，渲染 Bootstrap 风格的表单字段 + 错误提示 |
| **图书表单** | `components/book_form_fields.html` | 图书录入/编辑的字段集合 |
| **用户表单** | `components/user_form_fields.html` | 用户录入/编辑的字段集合 |

---

## 五、数据模型设计

### 5.1 ER 关系图

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────┐
│   Category  │       │      Book        │       │    User     │
├─────────────┤       ├──────────────────┤       ├─────────────┤
│ id (PK)     │──1:N──│ id (PK)          │       │ id (PK)     │
│ name        │       │ title            │       │ username    │
│ description │       │ author           │       │ email       │
│ created_at  │       │ isbn             │       │ password    │
└─────────────┘       │ publisher        │       │ role        │
                      │ publish_date     │       │ phone       │
                      │ category_id (FK) │       │ avatar      │
                      │ total_copies     │       │ is_active   │
                      │ available_copies │       │ created_at  │
                      │ cover_image      │       │ updated_at  │
                      │ description      │       └──────┬──────┘
                      │ location         │              │
                      │ created_at       │              │
                      │ updated_at       │              │
                      └────────┬─────────┘              │
                               │                        │
                               │         ┌──────────────┴──────┐
                               │         │    BorrowRecord     │
                               │         ├─────────────────────┤
                               └──1:N────│ id (PK)             │
                                         │ user_id (FK)        │
                                         │ book_id (FK)        │
                                         │ borrow_date         │
                                         │ due_date            │
                                         │ return_date         │
                                         │ status              │
                                         │ fine                │
                                         │ created_at          │
                                         │ updated_at          │
                                         └─────────────────────┘

┌──────────────────┐       ┌──────────────────┐
│   Reservation    │       │     Review       │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ user_id (FK)     │       │ user_id (FK)     │
│ book_id (FK)     │       │ book_id (FK)     │
│ reserve_date     │       │ rating           │
│ status           │       │ content          │
│ notify_date      │       │ is_visible       │
│ expire_date      │       │ created_at       │
│ created_at       │       └──────────────────┘
└──────────────────┘

┌──────────────────┐
│  Announcement    │
├──────────────────┤
│ id (PK)          │
│ title            │
│ content          │
│ priority         │
│ is_published     │
│ publisher_id(FK) │
│ created_at       │
│ updated_at       │
└──────────────────┘
```

### 5.2 模型详细字段

#### User（用户表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, Auto | 主键 |
| username | String(64) | Unique, NotNull | 用户名 |
| email | String(128) | Unique, NotNull | 邮箱 |
| password_hash | String(256) | NotNull | 密码哈希 |
| role | String(16) | Default='user' | 角色：admin / user |
| phone | String(20) | Nullable | 手机号 |
| avatar | String(256) | Nullable | 头像路径 |
| is_active | Boolean | Default=True | 是否启用 |
| created_at | DateTime | Default=now | 创建时间 |
| updated_at | DateTime | Default=now | 更新时间 |

#### Category（分类表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, Auto | 主键 |
| name | String(64) | Unique, NotNull | 分类名称 |
| description | Text | Nullable | 分类描述 |
| created_at | DateTime | Default=now | 创建时间 |

#### Book（图书表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, Auto | 主键 |
| title | String(256) | NotNull | 书名 |
| author | String(128) | NotNull | 作者 |
| isbn | String(20) | Unique, Nullable | ISBN 号 |
| publisher | String(128) | Nullable | 出版社 |
| publish_date | Date | Nullable | 出版日期 |
| category_id | Integer | FK → Category.id | 分类 |
| total_copies | Integer | Default=1 | 总库存 |
| available_copies | Integer | Default=1 | 可借数量 |
| cover_image | String(256) | Nullable | 封面图片路径 |
| description | Text | Nullable | 图书简介 |
| location | String(64) | Nullable | 馆藏位置 |
| created_at | DateTime | Default=now | 创建时间 |
| updated_at | DateTime | Default=now | 更新时间 |

#### BorrowRecord（借阅记录表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, Auto | 主键 |
| user_id | Integer | FK → User.id | 借阅用户 |
| book_id | Integer | FK → Book.id | 借阅图书 |
| borrow_date | DateTime | Default=now | 借阅日期 |
| due_date | DateTime | NotNull | 应还日期 |
| return_date | DateTime | Nullable | 实际归还日期 |
| status | String(16) | Default='borrowed' | 状态：borrowed / returned / overdue |
| fine | Numeric(10,2) | Default=0.00 | 逾期罚金（每日 ¥0.50） |
| created_at | DateTime | Default=now | 创建时间 |
| updated_at | DateTime | Default=now | 更新时间 |

#### Reservation（预约表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, Auto | 主键 |
| user_id | Integer | FK → User.id | 预约用户 |
| book_id | Integer | FK → Book.id | 预约图书 |
| reserve_date | DateTime | Default=now | 预约日期 |
| status | String(16) | Default='pending' | 状态：pending / fulfilled / cancelled / expired |
| notify_date | DateTime | Nullable | 通知日期 |
| expire_date | DateTime | Nullable | 过期日期 |
| created_at | DateTime | Default=now | 创建时间 |

#### Review（评论表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, Auto | 主键 |
| user_id | Integer | FK → User.id | 评论用户 |
| book_id | Integer | FK → Book.id | 评论图书 |
| rating | Integer | Default=5 | 评分（1-5星） |
| content | Text | Nullable | 评论内容 |
| is_visible | Boolean | Default=True | 是否可见 |
| created_at | DateTime | Default=now | 创建时间 |

#### Announcement（公告表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | Integer | PK, Auto | 主键 |
| title | String(256) | NotNull | 公告标题 |
| content | Text | NotNull | 公告内容 |
| priority | String(16) | Default='normal' | 优先级：normal / important / urgent |
| is_published | Boolean | Default=True | 是否发布 |
| publisher_id | Integer | FK → User.id | 发布者 |
| created_at | DateTime | Default=now | 创建时间 |
| updated_at | DateTime | Default=now | 更新时间 |

---

## 六、项目目录结构

```
finish/
├── app/                          # Flask 应用主包
│   ├── __init__.py               # 应用工厂函数 create_app()
│   ├── config.py                 # 配置类（开发/生产/测试）
│   ├── extensions.py             # Flask 扩展初始化（db, login, migrate）
│   │
│   ├── models/                   # 数据模型层
│   │   ├── __init__.py
│   │   ├── user.py               # User 模型
│   │   ├── book.py               # Book 模型
│   │   ├── category.py           # Category 模型
│   │   ├── borrow.py             # BorrowRecord 模型
│   │   ├── reservation.py        # Reservation 模型
│   │   ├── review.py             # Review 模型
│   │   └── announcement.py       # Announcement 模型
│   │
│   ├── auth/                     # 认证蓝图
│   │   ├── __init__.py           # 蓝图注册
│   │   ├── routes.py             # 登录/注册/登出路由
│   │   └── forms.py              # 登录/注册表单类
│   │
│   ├── admin/                    # 管理端蓝图
│   │   ├── __init__.py
│   │   ├── routes.py             # 管理端所有路由
│   │   └── forms.py              # 管理端表单类
│   │
│   ├── user/                     # 用户端蓝图
│   │   ├── __init__.py
│   │   ├── routes.py             # 用户端所有路由
│   │   └── forms.py              # 用户端表单类
│   │
│   ├── api/                      # REST API 蓝图（可选，用于 AJAX 交互）
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── decorators.py             # 自定义装饰器（角色权限校验等）
│   ├── utils.py                  # 工具函数（图片上传、日期处理等）
│   └── seed.py                   # 数据库种子数据脚本
│
├── templates/                    # Jinja2 模板文件
│   ├── layouts/
│   │   ├── base.html             # 基础布局
│   │   ├── admin.html            # 管理端布局
│   │   └── user.html             # 用户端布局
│   │
│   ├── components/
│   │   ├── navbar.html
│   │   ├── sidebar.html
│   │   ├── footer.html
│   │   ├── pagination.html
│   │   ├── search_bar.html
│   │   ├── book_card.html
│   │   ├── status_badge.html
│   │   ├── confirm_modal.html
│   │   ├── flash_messages.html
│   │   ├── empty_state.html
│   │   └── spinner.html
│   │
│   ├── macros/
│   │   └── form_field.html       # 表单字段宏
│   │
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   │
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── book_list.html
│   │   ├── book_form.html
│   │   ├── book_detail.html
│   │   ├── category_list.html
│   │   ├── user_list.html
│   │   ├── user_form.html
│   │   ├── borrow_list.html
│   │   ├── borrow_form.html
│   │   ├── reservation_list.html
│   │   ├── review_list.html
│   │   ├── announcement_list.html
│   │   └── announcement_form.html
│   │
│   └── user/
│       ├── dashboard.html
│       ├── book_list.html
│       ├── book_detail.html
│       ├── borrow_list.html
│       ├── reservation_list.html
│       ├── profile.html
│       └── change_password.html
│
├── static/                       # 静态资源
│   ├── css/
│   │   └── style.css             # 自定义样式
│   ├── js/
│   │   └── main.js               # 自定义脚本
│   ├── images/
│   │   └── covers/               # 图书封面图片
│   └── uploads/                  # 用户上传文件
│
├── migrations/                   # Flask-Migrate 迁移文件（自动生成）
│
├── tests/                        # 测试目录
│   ├── __init__.py
│   ├── conftest.py               # pytest 配置与 fixtures
│   ├── test_auth.py
│   ├── test_admin.py
│   ├── test_user.py
│   └── test_models.py
│
├── requirements.txt              # Python 依赖
├── run.py                        # 应用启动入口
├── .env                          # 环境变量（SECRET_KEY 等）
├── .env.example                  # 环境变量示例
├── .gitignore
└── readme.md
```

---

## 七、路由与蓝图设计

### 7.1 蓝图划分

| 蓝图名称 | URL 前缀 | 说明 |
|---------|---------|------|
| `auth_bp` | `/auth` | 认证相关（登录、注册、登出） |
| `admin_bp` | `/admin` | 管理后台（需 admin 角色） |
| `user_bp` | `/user` | 用户前台（需登录） |
| `api_bp` | `/api` | REST API（AJAX 调用） |

### 7.2 完整路由表

```
# 认证模块 (auth_bp)
GET   /auth/login              → 登录页面
POST  /auth/login              → 处理登录
GET   /auth/register           → 注册页面
POST  /auth/register           → 处理注册
GET   /auth/logout             → 登出

# 管理后台 (admin_bp) — 需要 admin 角色
GET   /admin/dashboard         → 管理后台首页
GET   /admin/books             → 图书列表
GET   /admin/books/add         → 添加图书页面
POST  /admin/books/add         → 处理添加图书
GET   /admin/books/<id>        → 图书详情
GET   /admin/books/<id>/edit   → 编辑图书页面
POST  /admin/books/<id>/edit   → 处理编辑图书
POST  /admin/books/<id>/delete → 删除图书
GET   /admin/categories        → 分类列表
POST  /admin/categories/add    → 添加分类
POST  /admin/categories/<id>/edit   → 编辑分类
POST  /admin/categories/<id>/delete → 删除分类
GET   /admin/users             → 用户列表
GET   /admin/users/add         → 添加用户页面
POST  /admin/users/add         → 处理添加用户
GET   /admin/users/<id>/edit   → 编辑用户页面
POST  /admin/users/<id>/edit   → 处理编辑用户
POST  /admin/users/<id>/toggle → 启用/禁用用户
GET   /admin/borrows           → 借阅记录列表
GET   /admin/borrows/add       → 借书页面
POST  /admin/borrows/add       → 处理借书
POST  /admin/borrows/<id>/return → 处理还书（自动计算罚金）
GET   /admin/reservations        → 预约记录列表
POST  /admin/reservations/<id>/cancel → 取消预约
GET   /admin/reviews             → 评论列表
POST  /admin/reviews/<id>/toggle → 显示/隐藏评论
POST  /admin/reviews/<id>/delete → 删除评论
GET   /admin/announcements       → 公告列表
GET   /admin/announcements/add   → 发布公告页面
POST  /admin/announcements/add   → 处理发布公告
GET   /admin/announcements/<id>/edit  → 编辑公告页面
POST  /admin/announcements/<id>/edit  → 处理编辑公告
POST  /admin/announcements/<id>/toggle → 上架/下架公告
POST  /admin/announcements/<id>/delete → 删除公告

# 用户前台 (user_bp) — 需要登录
GET   /user/dashboard          → 用户首页
GET   /user/books              → 图书浏览
GET   /user/books/<id>         → 图书详情
POST  /user/books/<id>/borrow  → 借阅图书
POST  /user/books/<id>/reserve → 预约图书
POST  /user/books/<id>/review  → 发表/更新评论
GET   /user/borrows            → 我的借阅
POST  /user/borrows/<id>/return → 归还图书（自动计算罚金）
GET   /user/reservations       → 我的预约
POST  /user/reservations/<id>/cancel → 取消预约
GET   /user/profile            → 个人中心
POST  /user/profile            → 更新个人信息
GET   /user/change-password    → 修改密码页面
POST  /user/change-password    → 处理修改密码

# API (api_bp) — AJAX 接口
GET   /api/books/search?q=     → 图书搜索建议
GET   /api/users/search?q=     → 用户搜索建议
GET   /api/borrows/stats       → 借阅统计数据
```

---

## 八、核心业务流程

### 8.1 借书流程

```
用户/管理员选择图书
    │
    ├── 检查 available_copies > 0 ?
    │       │
    │       ├── 否 → 提示"库存不足"
    │       │
    │       └── 是 → 创建 BorrowRecord
    │                   │
    │                   ├── status = "borrowed"
    │                   ├── borrow_date = now
    │                   ├── due_date = now + 30天
    │                   │
    │                   └── Book.available_copies -= 1
    │
    └── 完成
```

### 8.2 还书流程

```
管理员/用户确认归还
    │
    ├── 更新 BorrowRecord
    │       ├── return_date = now
    │       ├── status = "returned"
    │       ├── fine = 逾期天数 × ¥0.50/天
    │       │   (若 return_date > due_date 则计算罚金)
    │
    ├── Book.available_copies += 1
    │
    ├── 检查是否有待处理的预约
    │       └── 若有，通知预约用户
    │
    └── 完成
```

### 8.3 逾期检测与罚金

```
定时任务 / 每次查询时检查:
    遍历 status = "borrowed" 的记录
        │
        └── 若 now > due_date
                │
                └── status 更新为 "overdue"

罚金规则:
    - 每日罚金: ¥0.50
    - 归还时自动计算: fine = overdue_days × 0.50
    - 按时归还不产生罚金
```

### 8.4 预约流程

```
用户发现图书库存为 0
    │
    ├── 点击"预约此书"
    │       │
    │       ├── 检查是否已有待处理预约 → 提示"已预约"
    │       └── 创建 Reservation (status=pending)
    │
    └── 当图书被归还时
            │
            ├── 系统查找最早的 pending 预约
            └── 通知预约用户（可借阅）
```

### 8.5 评论流程

```
用户归还图书后
    │
    ├── 在图书详情页点击"写评论"
    │       │
    │       ├── 验证：必须借阅过该图书
    │       ├── 选择评分（1-5星）
    │       ├── 填写评论内容
    │       └── 提交 Review
    │
    └── 管理员可审核评论（显示/隐藏/删除）
```

---

## 九、开发计划（建议迭代顺序）

| 阶段 | 内容 | 产出 |
|------|------|------|
| **Phase 1: 项目初始化** | 创建 Flask 项目骨架、配置、扩展、基础布局模板 | 可运行的空项目 |
| **Phase 2: 认证模块** | User 模型、登录/注册/登出、Flask-Login 集成 | 用户可注册登录 |
| **Phase 3: 管理端-图书管理** | Book/Category 模型、CRUD 页面、分类管理 | 管理员可管理图书 |
| **Phase 4: 管理端-用户管理** | 用户列表、添加/编辑用户、启用/禁用 | 管理员可管理用户 |
| **Phase 5: 借阅管理** | BorrowRecord 模型、借书/还书、库存联动 | 核心借阅功能 |
| **Phase 6: 用户前台** | 图书浏览、搜索、个人借阅、个人中心 | 用户可自助借阅 |
| **Phase 7: 管理后台首页** | 统计图表、数据概览 | 数据可视化 |
| **Phase 8: 优化与测试** | 权限完善、异常处理、单元测试、样式打磨 | 生产可用 |

---

## 十、启动方式

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

---

## 十一、扩展方向（后续可考虑）

- [x] 图书预约功能（库存为 0 时可预约排队）
- [x] 图书评论与评分
- [x] 公告系统（管理员发布通知公告）
- [x] 逾期罚金自动计算
- [ ] 邮件通知（逾期提醒、预约到书通知）
- [ ] 数据导出（Excel/CSV）
- [ ] 条形码/ISBN 扫码录入
- [ ] RESTful API 完整化（前后端分离）
- [ ] Docker 容器化部署
- [ ] 日志系统（操作审计日志）
- [ ] 图书导入/导出（批量操作）