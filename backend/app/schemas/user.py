"""
用户相关的Pydantic验证模型
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ========== 用户基础模型 ==========

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    full_name: Optional[str] = Field(None, max_length=100, description="姓名")


class UserCreate(UserBase):
    """用户注册模型"""
    password: str = Field(..., min_length=6, max_length=50, description="密码")


class UserUpdate(BaseModel):
    """用户更新模型"""
    full_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_url: Optional[str] = None


class UserInDB(UserBase):
    """数据库中的用户模型"""
    id: int
    avatar_url: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDB):
    """用户响应模型（返回给前端）"""
    pass


# ========== 认证相关模型 ==========

class Token(BaseModel):
    """JWT令牌响应模型"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """JWT令牌数据模型"""
    user_id: Optional[int] = None
    username: Optional[str] = None


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")


# ========== 个人档案模型 ==========

class ProfileBase(BaseModel):
    """个人档案基础模型"""
    phone: Optional[str] = None
    bio: Optional[str] = None
    current_position: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None


class ProfileCreate(ProfileBase):
    """创建个人档案"""
    pass


class ProfileUpdate(ProfileBase):
    """更新个人档案"""
    pass


class Profile(ProfileBase):
    """个人档案响应模型"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
