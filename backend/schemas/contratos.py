from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class ContratoBase(BaseModel):
    cliente_id: int
    fecha_evento: date
    hora_inicio: time
    hora_fin: time
    paquete: str
    monto_total: float
    adelanto: Optional[float] = 0
    saldo: Optional[float] = 0
    estado: Optional[str] = "activo"

class ContratoCreate(ContratoBase):
    pass

class ContratoUpdate(BaseModel):
    fecha_evento: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    paquete: Optional[str] = None
    monto_total: Optional[float] = None
    adelanto: Optional[float] = None
    saldo: Optional[float] = None
    estado: Optional[str] = None

class ContratoResponse(ContratoBase):
    id: int

    class Config:
        from_attributes = True  # Esto arregla el Warning amarillo