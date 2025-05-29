
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserLogin, Token, UserResponse
from ..services.auth_service import AuthService

class AuthController:
    def __init__(self):
        self.auth_service = AuthService()
    
    def register(self, user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
        """用户注册控制器"""
        return self.auth_service.register_user(user, db)
    
    def login(self, user: UserLogin, db: Session = Depends(get_db)) -> Token:
        """用户登录控制器"""
        return self.auth_service.login_user(user, db)

# 创建控制器实例
auth_controller = AuthController()
