import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint
from pydantic import BaseModel
from utils.db import Base


#Modelo para la relacion Orden de compra y productos
class OrderProduct(Base):
    __tablename__ = "order_product"
    __table_args__ = (UniqueConstraint("order_id", "product_id"),)

    id = Column(Integer, primary_key=True, index=True,)
    order_id = Column(ForeignKey("order.id"), nullable=True,  doc=' Orden de compra')
    product_id = Column(ForeignKey("product.id"), nullable=True,  doc='Producto')
    product_price= Column(Float(20))
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
