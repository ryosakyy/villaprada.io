from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    dni: str
    nombre: str
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    dni: Optional[str] = None
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True
