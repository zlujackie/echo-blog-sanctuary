
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    articles = relationship("Article", back_populates="author")

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True, nullable=False)
    content = Column(Text, nullable=False)
    excerpt = Column(Text)
    category = Column(String(50))
    status = Column(String(20), default="草稿")  # 草稿, 已发布, 已下线
    image = Column(String(500))  # 封面图片 URL
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime)
    
    # 关系
    author = relationship("User", back_populates="articles")
    tags = relationship("ArticleTag", back_populates="article")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    articles = relationship("ArticleTag", back_populates="tag")

class ArticleTag(Base):
    __tablename__ = "article_tags"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    
    # 关系
    article = relationship("Article", back_populates="tags")
    tag = relationship("Tag", back_populates="articles")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author_name = Column(String(50), nullable=False)
    author_email = Column(String(100), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"))
    parent_id = Column(Integer, ForeignKey("comments.id"))  # 用于回复评论
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    article = relationship("Article")
    parent = relationship("Comment", remote_side=[id])
