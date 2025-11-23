"""
API依赖项：认证、数据库会话等
"""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from ..core.config import settings
from ..core.security import decode_access_token
from ..database import SessionLocal
from ..models.user import User
from ..crud import user as crud_user


# OAuth2密码流（Bearer Token）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_db() -> Generator:
    """
    获取数据库会话
    
    Yields:
        数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    获取当前登录用户
    
    Args:
        db: 数据库会话
        token: JWT令牌
    
    Returns:
        User对象
    
    Raises:
        HTTPException: 认证失败
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 解码JWT令牌
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # 从数据库获取用户
    user = crud_user.user.get(db, id=int(user_id))
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前激活的用户（预留功能）
    
    Args:
        current_user: 当前用户
    
    Returns:
        User对象
    
    Raises:
        HTTPException: 用户未激活
    """
    if not crud_user.user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未激活"
        )
    return current_user
