
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserCreate, UserLogin, Token, UserResponse
from ..controllers.auth_controller import auth_controller

router = APIRouter(prefix="/api/auth", tags=["认证"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    return auth_controller.register(user, db)

@router.post("/login", response_model=Token)
def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    return auth_controller.login(user, db)
