"""
用户管理API路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...schemas.user import User, UserUpdate, Profile, ProfileUpdate
from ...models.user import User as UserModel
from ...crud import user as crud_user
from ...api.deps import get_db, get_current_active_user


router = APIRouter()


@router.get("/me", response_model=User)
def get_my_info(
    current_user: UserModel = Depends(get_current_active_user),
) -> User:
    """获取当前用户信息"""
    return current_user


@router.put("/me", response_model=User)
def update_my_info(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
) -> User:
    """更新当前用户信息"""
    user = crud_user.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me/profile", response_model=Profile)
def get_my_profile(
    *,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_user),
) -> Profile:
    """获取当前用户的个人档案"""
    profile = crud_user.profile.get_by_user_id(db, user_id=current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="个人档案不存在"
        )
    return profile


@router.put("/me/profile", response_model=Profile)
def update_my_profile(
    *,
    db: Session = Depends(get_db),
    profile_in: ProfileUpdate,
    current_user: UserModel = Depends(get_current_active_user),
) -> Profile:
    """更新当前用户的个人档案"""
    profile = crud_user.profile.get_by_user_id(db, user_id=current_user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="个人档案不存在"
        )
    
    profile = crud_user.profile.update(db, db_obj=profile, obj_in=profile_in)
    return profile


@router.get("/{user_id}", response_model=User)
def get_user_by_id(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: UserModel = Depends(get_current_active_user),
) -> User:
    """根据ID获取用户信息"""
    user = crud_user.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user
