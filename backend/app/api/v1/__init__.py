"""
API v1路由汇总
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router


api_router = APIRouter()

# 认证路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])

# 用户管理路由
api_router.include_router(users_router, prefix="/users", tags=["用户管理"])
