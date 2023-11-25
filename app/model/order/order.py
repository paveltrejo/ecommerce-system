import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from utils.db import Base

# Clase para el status de un pedido
class OrderStatus(str, Enum):
    approval = "Aprobación"
    rejection = "Rechazo"
    scheduling_arrival = "En entrega"
    on_recovery =  "En recuperación"

#Modelo para el usuario
class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True,)
    owner_id = Column(ForeignKey("user.id"), nullable=True,  doc='Seller propietario')
    role = Column(String, default=OrderStatus.approval.value)
    eta = Column(DateTime(timezone=True), nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
