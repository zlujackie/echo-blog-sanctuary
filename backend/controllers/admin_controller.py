
from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import StatsResponse
from ..services.admin_service import AdminService
from ..auth import get_current_admin_user

class AdminController:
    def __init__(self):
        self.admin_service = AdminService()
    
    def get_dashboard_stats(
        self,
        current_user: User = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
    ) -> StatsResponse:
        """获取仪表板统计数据"""
        return self.admin_service.get_dashboard_stats(db)
    
    def get_users(
        self,
        current_user: User = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
    ) -> list:
        """获取用户列表"""
        return self.admin_service.get_all_users(db)

# 创建控制器实例
admin_controller = AdminController()
