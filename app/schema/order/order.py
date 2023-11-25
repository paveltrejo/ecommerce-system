from datetime import datetime, date
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from model.user.user import UserRole

from pydantic import BaseModel, Field, condecimal

class OrderCreate(BaseModel):
   
    buyer_id: int = Field(
        title="Comprador"
    )
    eta: datetime = Field(
        title="Fecha de entrega aproximada"        
    ) 
    is_active: boolean = Field(
        title = "Activo"
    )
    created_at:Optional[datetime] = Field(
        default=datetime.now()
    )


class OrderModify(BaseModel):
    
    buyer_id: int = Field(
        title="Comprador"
    )
    total_amount: condecimal(decimal_places= 2)
    eta: datetime = Field(
        title="Fecha de entrega aproximada"        
    ) 
    is_active: boolean = Field(
        title = "Activo"
    )
    updated_at:Optional[datetime] = Field(
        default=datetime.now()
    )

class OrderProductCreate(BaseModel):

    order: OrderCreate
    products_id: Optional[list[int]]