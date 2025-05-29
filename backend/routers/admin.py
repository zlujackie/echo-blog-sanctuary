
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import StatsResponse
from ..auth import get_current_admin_user
from ..controllers.admin_controller import admin_controller

router = APIRouter(prefix="/api/admin", tags=["管理后台"])

@router.get("/stats", response_model=StatsResponse)
def get_dashboard_stats(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取仪表板统计数据"""
    return admin_controller.get_dashboard_stats(current_user, db)

@router.get("/users")
def get_users(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """获取用户列表"""
    return admin_controller.get_users(current_user, db)
