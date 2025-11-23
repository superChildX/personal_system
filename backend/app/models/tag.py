"""
标签和附件模型：tags, attachments
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from ..database import Base


class Tag(Base):
    """标签表"""
    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='unique_user_tag'),
    )
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    color = Column(String(20))
    usage_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


class Attachment(Base):
    """附件表"""
    __tablename__ = "attachments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    entity_type = Column(String(50), nullable=False, index=True)  # projects/notes/experiences等
    entity_id = Column(Integer, nullable=False, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)  # 字节
    file_type = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
