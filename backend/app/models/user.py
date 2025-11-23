"""
用户相关模型：users, profiles, education, skills
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean, DECIMAL, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    avatar_url = Column(String(255))
    github_username = Column(String(100))
    linkedin_url = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 关系
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    education = relationship("Education", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    """个人档案表"""
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    phone = Column(String(20))
    bio = Column(Text)
    current_position = Column(String(100))
    location = Column(String(100))
    website = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 关系
    user = relationship("User", back_populates="profile")


class Education(Base):
    """教育背景表"""
    __tablename__ = "education"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    school_name = Column(String(200), nullable=False)
    major = Column(String(100))
    degree = Column(String(50))
    gpa = Column(DECIMAL(3, 2))
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # 关系
    user = relationship("User", back_populates="education")


class Skill(Base):
    """技能表"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50))  # 编程语言/框架/工具
    proficiency = Column(Integer, default=3)  # 1-5星评分
    years_of_experience = Column(DECIMAL(3, 1))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # 关系
    user = relationship("User", back_populates="skills")
