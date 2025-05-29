
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import Article, User, Comment
from ..schemas import StatsResponse
from ..auth import get_current_admin_user

router = APIRouter(prefix="/api/admin", tags=["管理后台"])

@router.get("/stats", response_model=StatsResponse)
def get_dashboard_stats(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取仪表板统计数据"""
    
    # 文章统计
    total_articles = db.query(Article).count()
    published_articles = db.query(Article).filter(Article.status == "已发布").count()
    draft_articles = db.query(Article).filter(Article.status == "草稿").count()
    
    # 浏览量统计
    total_views = db.query(func.sum(Article.views)).scalar() or 0
    
    # 点赞统计
    total_likes = db.query(func.sum(Article.likes)).scalar() or 0
    
    # 评论统计
    total_comments = db.query(Comment).count()
    
    return {
        "total_articles": total_articles,
        "published_articles": published_articles,
        "draft_articles": draft_articles,
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments
    }

@router.get("/users")
def get_users(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    users = db.query(User).all()
    return users
