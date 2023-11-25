import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from utils.db import Base

#Clase para definir los roles
class UserRole(str, Enum):
    anonymous = "Anonymous"
    seller = "Seller"
    admin_plat_us = "Admin Platform User Roles"
    admin =  "Admin"
    financial = "Financial"
    logistics = "Logistics"

#Modelo para el usuario
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True,)
    email = Column(String(80), unique=True)
    hashed_pass = Column(String(200))
    role = Column(String, default=UserRole.anonymous.value)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self):
        return f"{self.id} - {self.email} - {self.hashed_pass} - {self.role_id} - {self.is_coordinator} - {self.is_admin} - {self.is_employee} - {self.is_superuser} - {self.is_active} - {self.created_at} - {self.updated_at}"
