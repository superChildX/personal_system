"""
用户CRUD操作
"""
from typing import Optional
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..models.user import User, Profile
from ..schemas.user import UserCreate, UserUpdate, ProfileCreate, ProfileUpdate
from ..core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """用户CRUD操作类"""
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """创建用户（密码哈希）"""
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            full_name=obj_in.full_name,
            password_hash=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # 自动创建个人档案
        profile = Profile(user_id=db_obj.id)
        db.add(profile)
        db.commit()
        
        return db_obj
    
    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        """
        验证用户身份（用户名/邮箱 + 密码）
        
        Args:
            username: 用户名或邮箱
            password: 密码
        
        Returns:
            User对象或None
        """
        # 先尝试用户名查询
        user = self.get_by_username(db, username=username)
        
        # 如果找不到，尝试邮箱查询
        if not user:
            user = self.get_by_email(db, email=username)
        
        if not user:
            return None
        
        # 验证密码
        if not verify_password(password, user.password_hash):
            return None
        
        return user
    
    def is_active(self, user: User) -> bool:
        """检查用户是否激活（预留功能）"""
        return True
    
    def update_password(self, db: Session, *, user: User, new_password: str) -> User:
        """更新用户密码"""
        user.password_hash = get_password_hash(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


class CRUDProfile(CRUDBase[Profile, ProfileCreate, ProfileUpdate]):
    """个人档案CRUD操作类"""
    
    def get_by_user_id(self, db: Session, *, user_id: int) -> Optional[Profile]:
        """根据用户ID获取个人档案"""
        return db.query(Profile).filter(Profile.user_id == user_id).first()


# 创建CRUD实例
user = CRUDUser(User)
profile = CRUDProfile(Profile)
