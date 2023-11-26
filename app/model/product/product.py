import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
from utils.db import Base


class ProductStatus(str, Enum):
    exist = "Existencia"
    out_of_stock = "Agotado"
    cancel = "Cancelado"


class ProductLog(Base):
    __tablename__ = "product_log"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(ForeignKey("product.id"), nullable=False)
    name = Column(String(280))
    description = Column(String(520))
    price = Column(Float(20))
    status = Column(String)
    owner_id = Column(ForeignKey("user.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True,)
    name = Column(String(280), unique=True)
    description = Column(String(520))
    price = Column(Float(20))
    status = Column(String, default=ProductStatus.exist.value)
    owner_id = Column(ForeignKey("user.id"), nullable=True,
                      doc='Seller propietario')

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
