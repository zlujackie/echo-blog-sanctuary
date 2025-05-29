
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from ..database import get_db
from ..models import Article, User
from ..schemas import (
    ArticleCreate, 
    ArticleUpdate, 
    ArticleResponse, 
    ArticleListResponse
)
from ..auth import get_current_user, get_current_admin_user

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
    query = db.query(Article).filter(Article.status == "已发布")
    
    if category:
        query = query.filter(Article.category == category)
    
    if search:
        query = query.filter(Article.title.contains(search))
    
    articles = query.order_by(desc(Article.published_at)).offset(skip).limit(limit).all()
    return articles

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """获取单篇文章详情"""
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
    query = db.query(Article)
    
    if status_filter:
        query = query.filter(Article.status == status_filter)
    
    if category:
        query = query.filter(Article.category == category)
    
    articles = query.order_by(desc(Article.created_at)).offset(skip).limit(limit).all()
    return articles

@router.post("/", response_model=ArticleResponse)
def create_article(
    article: ArticleCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """创建文章"""
    db_article = Article(
        **article.dict(),
        author_id=current_user.id
    )
    
    # 如果是发布状态，设置发布时间
    if article.status == "已发布":
        db_article.published_at = datetime.utcnow()
    
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    
    return db_article

@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
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

@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
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

@router.post("/{article_id}/like")
def like_article(article_id: int, db: Session = Depends(get_db)):
    """点赞文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )
    
    article.likes += 1
    db.commit()
    
    return {"message": "点赞成功", "likes": article.likes}
