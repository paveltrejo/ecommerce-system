from datetime import datetime, date
from typing import Optional
from uuid import UUID
from xmlrpc.client import boolean

from model.user.user import UserRole

from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
   
    email: EmailStr = Field(
        title= "Nombre del metodo de pago",
        max_lenght= 50
    )
    hashed_pass:str = Field (
        title = "Contraseña",
        max_lenght= 25
    )
    is_active: boolean = Field(
        title = "Activo"
    )
    created_at:Optional[datetime] = Field(
        default=datetime.now()
    )


class UserModify(BaseModel):
    
    email: EmailStr = Field(
        title= "Nombre del metodo de pago",
        max_lenght= 50
    )
    hashed_pass:str = Field (
        title = "Contraseña",
        max_lenght= 25
    )
    is_active: boolean = Field(
        title = "Activo"
    )
    updated_at:Optional[datetime] = Field(
        default=datetime.now()
    )
