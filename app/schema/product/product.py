from datetime import datetime, date
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from model.user.user import UserRole

from pydantic import BaseModel, Field, condecimal

class ProductCreate(BaseModel):
   
    name: str  = Field(
        title= "Nombre del producto",
        max_lenght= 250
    )
    description: str  = Field(
        title= "Descripción del producto",
        max_lenght= 520
    )
    price: condecimal(decimal_places= 2)
    is_active: boolean = Field(
        title = "Activo"
    )
    created_at:Optional[datetime] = Field(
        default=datetime.now()
    )


class ProductModify(BaseModel):
    
    name: str  = Field(
        title= "Nombre del producto",
        max_lenght= 250
    )
    description: str  = Field(
        title= "Descripción del producto",
        max_lenght= 520
    )
    price: condecimal(decimal_places= 2)
    owner_id: int = Field(
        title="Seller del producto"
    )
    is_active: boolean = Field(
        title = "Activo"
    )
    updated_at:Optional[datetime] = Field(
        default=datetime.now()
    )
