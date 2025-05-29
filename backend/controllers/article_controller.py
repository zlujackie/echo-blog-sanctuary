
from typing import List, Optional
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import (
    ArticleCreate, 
    ArticleUpdate, 
    ArticleResponse, 
    ArticleListResponse
)
from ..services.article_service import ArticleService
from ..auth import get_current_admin_user

class ArticleController:
    def __init__(self):
        self.article_service = ArticleService()
    
    def get_articles(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        category: Optional[str] = None,
        search: Optional[str] = None,
        db: Session = Depends(get_db)
    ) -> List[ArticleListResponse]:
        """获取文章列表（前台）"""
        return self.article_service.get_published_articles(db, skip, limit, category, search)
    
    def get_article(self, article_id: int, db: Session = Depends(get_db)) -> ArticleResponse:
        """获取单篇文章详情"""
        return self.article_service.get_article_by_id(article_id, db)
    
    def get_admin_articles(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        status_filter: Optional[str] = Query(None, alias="status"),
        category: Optional[str] = None,
        current_user: User = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
    ) -> List[ArticleResponse]:
        """获取所有文章（后台管理）"""
        return self.article_service.get_admin_articles(db, skip, limit, status_filter, category)
    
    def create_article(
        self,
        article: ArticleCreate,
        current_user: User = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
    ) -> ArticleResponse:
        """创建文章"""
        return self.article_service.create_article(article, current_user.id, db)
    
    def update_article(
        self,
        article_id: int,
        article_update: ArticleUpdate,
        current_user: User = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
    ) -> ArticleResponse:
        """更新文章"""
        return self.article_service.update_article(article_id, article_update, db)
    
    def delete_article(
        self,
        article_id: int,
        current_user: User = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
    ) -> dict:
        """删除文章"""
        return self.article_service.delete_article(article_id, db)
    
    def like_article(self, article_id: int, db: Session = Depends(get_db)) -> dict:
        """点赞文章"""
        return self.article_service.like_article(article_id, db)

# 创建控制器实例
article_controller = ArticleController()
