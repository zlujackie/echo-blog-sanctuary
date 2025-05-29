
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate, UserLogin, Token, UserResponse
from ..auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

class AuthService:
    def register_user(self, user: UserCreate, db: Session) -> UserResponse:
        """用户注册业务逻辑"""
        # 检查用户名是否已存在
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )
        
        # 创建新用户
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        
        # 如果是第一个用户，设为管理员
        if db.query(User).count() == 0:
            db_user.is_admin = True
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    def login_user(self, user: UserLogin, db: Session) -> Token:
        """用户登录业务逻辑"""
        user_obj = authenticate_user(db, user.username, user.password)
        if not user_obj:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_obj.username}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_obj
        }
