from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    age = Column(Integer)
    bio = Column(Text)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    swipe_actions = relationship("SwipeAction", back_populates="user")


class Mug(Base):
    __tablename__ = "mugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    swipe_actions = relationship("SwipeAction", back_populates="mug")


class SwipeAction(Base):
    __tablename__ = "swipe_actions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mug_id = Column(Integer, ForeignKey("mugs.id"))
    is_like = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="swipe_actions")
    mug = relationship("Mug", back_populates="swipe_actions")


# Pydantic models for API
class UserCreate(BaseModel):
    email: str
    name: str
    age: int
    bio: Optional[str] = ""
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class MugResponse(BaseModel):
    id: int
    name: str
    description: str
    image_url: str

    class Config:
        from_attributes = True
