
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Article, User, Comment
from ..schemas import StatsResponse

class AdminService:
    def get_dashboard_stats(self, db: Session) -> StatsResponse:
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
    
    def get_all_users(self, db: Session) -> list:
        """获取所有用户"""
        users = db.query(User).all()
        return users
