
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
import jwt
import bcrypt
from pydantic import BaseModel
from typing import List, Optional

# 数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT 配置
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 初始化 FastAPI 应用
app = FastAPI(title="个人博客 API", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    excerpt = Column(Text)
    category = Column(String)
    status = Column(String, default="草稿")  # 草稿 或 已发布
    image = Column(String, nullable=True)
    views = Column(Integer, default=0)
    author_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# Pydantic 模型
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ArticleCreate(BaseModel):
    title: str
    content: str
    excerpt: str
    category: str
    status: str = "草稿"
    image: Optional[str] = None

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    image: Optional[str] = None

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    excerpt: str
    category: str
    status: str
    image: Optional[str]
    views: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT 工具函数
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效的认证凭据")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="无效的认证凭据")

def get_current_user(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

# 密码工具函数
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# API 路由
@app.post("/api/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 检查用户是否已存在
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 创建新用户
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "用户注册成功"}

@app.post("/api/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    # 验证用户
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": db_user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "is_admin": db_user.is_admin
        }
    }

@app.get("/api/articles", response_model=List[ArticleResponse])
def get_articles(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Article)
    
    # 只显示已发布的文章（前台）
    if status is None:
        query = query.filter(Article.status == "已发布")
    elif status:
        query = query.filter(Article.status == status)
    
    if category:
        query = query.filter(Article.category == category)
    
    articles = query.offset(skip).limit(limit).all()
    return articles

@app.get("/api/articles/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 增加浏览量
    article.views += 1
    db.commit()
    
    return article

@app.post("/api/admin/articles", response_model=ArticleResponse)
def create_article(
    article: ArticleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 检查管理员权限
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    db_article = Article(
        **article.dict(),
        author_id=current_user.id
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    return db_article

@app.put("/api/admin/articles/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 检查管理员权限
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    # 更新文章
    for field, value in article_update.dict(exclude_unset=True).items():
        setattr(db_article, field, value)
    
    db_article.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_article)
    
    return db_article

@app.delete("/api/admin/articles/{article_id}")
def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 检查管理员权限
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="文章不存在")
    
    db.delete(db_article)
    db.commit()
    
    return {"message": "文章删除成功"}

@app.get("/api/admin/articles", response_model=List[ArticleResponse])
def get_admin_articles(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 检查管理员权限
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    articles = db.query(Article).offset(skip).limit(limit).all()
    return articles

@app.get("/api/stats")
def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 检查管理员权限
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    total_articles = db.query(Article).count()
    published_articles = db.query(Article).filter(Article.status == "已发布").count()
    draft_articles = db.query(Article).filter(Article.status == "草稿").count()
    total_views = db.query(Article).with_entities(Article.views).all()
    total_views_sum = sum([views[0] for views in total_views])
    
    return {
        "total_articles": total_articles,
        "published_articles": published_articles,
        "draft_articles": draft_articles,
        "total_views": total_views_sum
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
