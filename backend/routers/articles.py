
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import (
    ArticleCreate, 
    ArticleUpdate, 
    ArticleResponse, 
    ArticleListResponse
)
from ..auth import get_current_admin_user
from ..controllers.article_controller import article_controller

router = APIRouter(prefix="/api/articles", tags=["文章"])

@router.get("/", response_model=List[ArticleListResponse])
def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取文章列表（前台）"""
    return article_controller.get_articles(skip, limit, category, search, db)

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """获取单篇文章详情"""
    return article_controller.get_article(article_id, db)

@router.get("/admin/all", response_model=List[ArticleResponse])
def get_admin_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    category: Optional[str] = None,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取所有文章（后台管理）"""
    return article_controller.get_admin_articles(skip, limit, status_filter, category, current_user, db)

@router.post("/", response_model=ArticleResponse)
def create_article(
    article: ArticleCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """创建文章"""
    return article_controller.create_article(article, current_user, db)

@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """更新文章"""
    return article_controller.update_article(article_id, article_update, current_user, db)

@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """删除文章"""
    return article_controller.delete_article(article_id, current_user, db)

@router.post("/{article_id}/like")
def like_article(article_id: int, db: Session = Depends(get_db)):
    """点赞文章"""
    return article_controller.like_article(article_id, db)
