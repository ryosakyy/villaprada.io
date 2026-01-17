from pydantic import BaseModel
from datetime import date, time

# Base compartida
class DisponibilidadBase(BaseModel):
    fecha: date
    hora_inicio: time | None = None
    hora_fin: time | None = None
    estado: str = "bloqueado"
    motivo: str | None = None


# Crear
class DisponibilidadCreate(DisponibilidadBase):
    pass


# Actualizar (idéntico al create)
class DisponibilidadUpdate(DisponibilidadBase):
    pass


# Output
class DisponibilidadOut(BaseModel):
    id: int
    fecha: date
    hora_inicio: time | None
    hora_fin: time | None
    estado: str
    motivo: str | None

    # Pydantic v2
    class Config:
        from_attributes = True
