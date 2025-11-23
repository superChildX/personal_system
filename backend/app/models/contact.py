"""
社交网络模型：contacts, meetings
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Date, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from ..database import Base
import enum


class ContactCategory(str, enum.Enum):
    """联系人分类枚举"""
    MENTOR = "mentor"
    CLASSMATE = "classmate"
    COLLEAGUE = "colleague"
    FRIEND = "friend"


class Contact(Base):
    """联系人表"""
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(SQLEnum(ContactCategory))
    position = Column(String(100))
    company = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    wechat = Column(String(50))
    github = Column(String(100))
    linkedin = Column(String(255))
    notes = Column(Text)
    last_contact_date = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class Meeting(Base):
    """会议记录表"""
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    meeting_date = Column(DateTime)
    location = Column(String(200))
    attendees = Column(JSON)  # 参与人员数组
    agenda = Column(Text)  # 会议议程
    minutes = Column(Text)  # 会议纪要
    action_items = Column(Text)  # 行动项
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
