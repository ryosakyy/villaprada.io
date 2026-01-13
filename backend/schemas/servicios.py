from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base para compartir campos
class ServicioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    estado: Optional[str] = "activo"

# Para crear (lo que manda el frontend)
class ServicioCreate(ServicioBase):
    pass

# Para leer (lo que responde el backend, incluye ID y fechas)
class ServicioResponse(ServicioBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True # <--- CORREGIDO: "orm_mode" ahora es "from_attributes"