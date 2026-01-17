from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# -------------------------
# Schema Base (solo lectura)
# -------------------------
class UsuarioBase(BaseModel):
    nombres: str = Field(..., example="Juan Pérez")
    email: EmailStr = Field(..., example="admin@villa.com")
    rol: Optional[str] = "admin"
    estado: Optional[bool] = True


# -------------------------
# Crear usuario
# -------------------------
class UsuarioCreate(BaseModel):
    nombres: str = Field(..., example="Juan Pérez")
    email: EmailStr = Field(..., example="admin@villa.com")
    password: str = Field(..., min_length=6)
    rol: Optional[str] = "admin"


# -------------------------
# Actualizar usuario (parcial)
# -------------------------
class UsuarioUpdate(BaseModel):
    nombres: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    rol: Optional[str]
    estado: Optional[bool]


# -------------------------
# Login Request
# -------------------------
class LoginRequest(BaseModel):
    email: str
    password: str

# -------------------------
# Respuesta final
# -------------------------
class UsuarioResponse(UsuarioBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True
