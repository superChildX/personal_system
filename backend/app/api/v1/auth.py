"""
认证API路由：注册、登录
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ...core.config import settings
from ...core.security import create_access_token
from ...schemas.user import User, UserCreate, UserLogin, Token
from ...crud import user as crud_user
from ...api.deps import get_db, get_current_active_user


router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> User:
    """
    用户注册
    
    - **username**: 用户名（3-50字符）
    - **email**: 邮箱
    - **password**: 密码（至少6字符）
    - **full_name**: 姓名（可选）
    """
    # 检查用户名是否已存在
    user = crud_user.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )
    
    # 检查邮箱是否已存在
    user = crud_user.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册",
        )
    
    # 创建用户
    user = crud_user.user.create(db, obj_in=user_in)
    return user


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    用户登录（OAuth2密码流）
    
    - **username**: 用户名或邮箱
    - **password**: 密码
    
    返回JWT访问令牌
    """
    # 验证用户身份
    user = crud_user.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否激活
    if not crud_user.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未激活"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login/json", response_model=Token)
def login_json(
    *,
    db: Session = Depends(get_db),
    user_in: UserLogin,
) -> Token:
    """
    用户登录（JSON格式）
    
    - **username**: 用户名或邮箱
    - **password**: 密码
    
    返回JWT访问令牌
    """
    # 验证用户身份
    user = crud_user.user.authenticate(
        db, username=user_in.username, password=user_in.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否激活
    if not crud_user.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未激活"
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=User)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    获取当前登录用户信息
    
    需要在请求头中携带JWT令牌：
    Authorization: Bearer <token>
    """
    return current_user


@router.post("/test-token", response_model=User)
def test_token(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    测试JWT令牌是否有效
    """
    return current_user
