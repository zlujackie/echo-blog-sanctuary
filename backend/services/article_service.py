
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from ..models import Article
from ..schemas import (
    ArticleCreate, 
    ArticleUpdate, 
    ArticleResponse, 
    ArticleListResponse
)

class ArticleService:
    def get_published_articles(
        self, 
        db: Session, 
        skip: int, 
        limit: int, 
        category: Optional[str] = None, 
        search: Optional[str] = None
    ) -> List[ArticleListResponse]:
        """获取已发布的文章列表"""
        query = db.query(Article).filter(Article.status == "已发布")
        
        if category:
            query = query.filter(Article.category == category)
        
        if search:
            query = query.filter(Article.title.contains(search))
        
        articles = query.order_by(desc(Article.published_at)).offset(skip).limit(limit).all()
        return articles
    
    def get_article_by_id(self, article_id: int, db: Session) -> ArticleResponse:
        """根据ID获取文章详情"""
        article = db.query(Article).filter(
            Article.id == article_id,
            Article.status == "已发布"
        ).first()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        # 增加浏览量
        article.views += 1
        db.commit()
        
        return article
    
    def get_admin_articles(
        self, 
        db: Session, 
        skip: int, 
        limit: int, 
        status_filter: Optional[str] = None, 
        category: Optional[str] = None
    ) -> List[ArticleResponse]:
        """获取管理员文章列表"""
        query = db.query(Article)
        
        if status_filter:
            query = query.filter(Article.status == status_filter)
        
        if category:
            query = query.filter(Article.category == category)
        
        articles = query.order_by(desc(Article.created_at)).offset(skip).limit(limit).all()
        return articles
    
    def create_article(self, article: ArticleCreate, author_id: int, db: Session) -> ArticleResponse:
        """创建新文章"""
        db_article = Article(
            **article.dict(),
            author_id=author_id
        )
        
        # 如果是发布状态，设置发布时间
        if article.status == "已发布":
            db_article.published_at = datetime.utcnow()
        
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        
        return db_article
    
    def update_article(self, article_id: int, article_update: ArticleUpdate, db: Session) -> ArticleResponse:
        """更新文章"""
        db_article = db.query(Article).filter(Article.id == article_id).first()
        
        if not db_article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        # 更新文章字段
        update_data = article_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_article, field, value)
        
        # 如果状态改为发布且之前未发布，设置发布时间
        if (article_update.status == "已发布" and 
            db_article.status != "已发布" and 
            not db_article.published_at):
            db_article.published_at = datetime.utcnow()
        
        db_article.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_article)
        
        return db_article
    
    def delete_article(self, article_id: int, db: Session) -> dict:
        """删除文章"""
        db_article = db.query(Article).filter(Article.id == article_id).first()
        
        if not db_article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        db.delete(db_article)
        db.commit()
        
        return {"message": "文章删除成功"}
    
    def like_article(self, article_id: int, db: Session) -> dict:
        """文章点赞"""
        article = db.query(Article).filter(Article.id == article_id).first()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在"
            )
        
        article.likes += 1
        db.commit()
        
        return {"message": "点赞成功", "likes": article.likes}
