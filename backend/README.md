
# 个人博客后端 API

基于 FastAPI 构建的个人博客后端系统，采用 MVC 架构模式，提供完整的文章管理、用户认证和管理后台功能。

## 技术栈

- **FastAPI**: 现代、快速的 Web 框架
- **SQLAlchemy**: ORM 数据库工具
- **Pydantic**: 数据验证和序列化
- **JWT**: 身份认证
- **BCrypt**: 密码加密
- **SQLite/PostgreSQL/MySQL**: 数据库支持

## 架构设计

本项目采用 **MVC (Model-View-Controller) 架构模式**：

- **Models** (`models.py`): 数据库模型定义
- **Views** (`routers/`): API 路由和请求处理
- **Controllers** (`controllers/`): 业务逻辑控制
- **Services** (`services/`): 具体业务实现

## 功能特性

### 前台功能
- 文章列表展示
- 文章详情查看
- 文章搜索和分类筛选
- 文章点赞功能
- 浏览量统计

### 后台管理
- 管理员登录认证
- 文章的增删改查
- 文章状态管理（草稿/已发布）
- 统计数据展示
- 用户管理

### API 功能
- RESTful API 设计
- JWT 身份认证
- 权限控制
- 数据验证
- 错误处理
- CORS 支持

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python init_db.py
```

这将创建：
- 默认管理员账号：用户名 `admin`，密码 `admin123`
- 示例文章数据

### 3. 启动服务

```bash
# 开发模式
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. 访问 API 文档

启动后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口

### 认证接口
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 文章接口
- `GET /api/articles/` - 获取文章列表
- `GET /api/articles/{id}` - 获取文章详情
- `POST /api/articles/{id}/like` - 文章点赞

### 管理员接口
- `GET /api/articles/admin/all` - 获取所有文章（管理员）
- `POST /api/articles/` - 创建文章
- `PUT /api/articles/{id}` - 更新文章
- `DELETE /api/articles/{id}` - 删除文章
- `GET /api/admin/stats` - 获取统计数据

## 项目结构

```
backend/
├── main.py                   # FastAPI 应用入口
├── database.py               # 数据库配置
├── models.py                 # 数据库模型
├── schemas.py                # Pydantic 数据模型
├── auth.py                   # JWT 认证相关
├── controllers/              # 控制器层
│   ├── __init__.py
│   ├── auth_controller.py    # 认证控制器
│   ├── article_controller.py # 文章控制器
│   └── admin_controller.py   # 管理控制器
├── services/                 # 服务层
│   ├── __init__.py
│   ├── auth_service.py       # 认证服务
│   ├── article_service.py    # 文章服务
│   └── admin_service.py      # 管理服务
├── routers/                  # 路由层
│   ├── __init__.py
│   ├── auth.py               # 认证路由
│   ├── articles.py           # 文章路由
│   └── admin.py              # 管理路由
├── init_db.py                # 数据库初始化
├── requirements.txt          # 依赖列表
└── README.md                 # 说明文档
```

## MVC 架构说明

### Controller 层
负责接收请求、调用相应的服务、返回响应：
- `AuthController`: 处理用户认证相关逻辑
- `ArticleController`: 处理文章相关业务逻辑
- `AdminController`: 处理管理后台逻辑

### Service 层
包含具体的业务实现逻辑：
- `AuthService`: 用户注册、登录、令牌验证等
- `ArticleService`: 文章的 CRUD 操作、搜索、点赞等
- `AdminService`: 管理后台统计、用户管理等

### Router 层 (View)
定义 API 路由和参数验证：
- `auth.py`: 认证相关 API 路由
- `articles.py`: 文章相关 API 路由
- `admin.py`: 管理后台 API 路由

## 数据库模型

### User (用户)
- id: 主键
- username: 用户名
- email: 邮箱
- hashed_password: 加密密码
- is_admin: 是否管理员
- created_at: 创建时间

### Article (文章)
- id: 主键
- title: 标题
- content: 内容
- excerpt: 摘要
- category: 分类
- status: 状态（草稿/已发布）
- image: 封面图片
- views: 浏览量
- likes: 点赞数
- author_id: 作者ID
- created_at: 创建时间
- updated_at: 更新时间
- published_at: 发布时间

## 环境配置

可以通过环境变量配置：

```bash
# 数据库 URL
DATABASE_URL=sqlite:///./blog.db

# JWT 密钥
SECRET_KEY=your-secret-key-here

# 其他配置...
```

## 部署说明

### Docker 部署

```dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境建议
- 使用 PostgreSQL 或 MySQL 数据库
- 配置 Nginx 反向代理
- 使用 HTTPS
- 设置环境变量
- 配置日志记录
- 实施备份策略

## 与前端集成

这个后端 API 设计为与任何前端框架兼容，包括：
- React
- Vue.js
- Angular
- 原生 JavaScript

前端需要：
1. 处理 JWT 认证
2. 调用相应的 API 接口
3. 处理错误响应
4. 实现用户界面

## 扩展功能
- 评论系统
- 标签管理
- 文件上传
- 邮件通知
- 社交媒体集成
- SEO 优化
- 搜索功能增强

## 许可证

MIT License
