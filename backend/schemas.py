
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# 用户相关 Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# 文章相关 Schema
class ArticleBase(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None

class ArticleCreate(ArticleBase):
    status: str = "草稿"

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    image: Optional[str] = None

class ArticleResponse(ArticleBase):
    id: int
    status: str
    views: int
    likes: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ArticleListResponse(BaseModel):
    id: int
    title: str
    excerpt: Optional[str]
    category: Optional[str]
    status: str
    image: Optional[str]
    views: int
    likes: int
    author_id: int
    created_at: datetime
    published_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# 标签相关 Schema
class TagBase(BaseModel):
    name: str
    description: Optional[str] = None

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 评论相关 Schema
class CommentBase(BaseModel):
    content: str
    author_name: str
    author_email: EmailStr

class CommentCreate(CommentBase):
    article_id: int
    parent_id: Optional[int] = None

class CommentResponse(CommentBase):
    id: int
    article_id: int
    parent_id: Optional[int]
    is_approved: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# 统计相关 Schema
class StatsResponse(BaseModel):
    total_articles: int
    published_articles: int
    draft_articles: int
    total_views: int
    total_likes: int
    total_comments: int

# Token 相关 Schema
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None
