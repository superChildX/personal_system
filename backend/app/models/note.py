"""
学习笔记模型：notes, code_snippets
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Note(Base):
    """学习笔记表"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    category = Column(String(50))  # 课程笔记/技术博客/代码片段
    tags = Column(JSON)  # 标签数组
    is_public = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class CodeSnippet(Base):
    """代码片段表"""
    __tablename__ = "code_snippets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(50))  # JavaScript/Python/Java等
    description = Column(Text)
    tags = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
