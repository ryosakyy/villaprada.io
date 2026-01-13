from pydantic import BaseModel
from datetime import date
from typing import Optional

class PagoBase(BaseModel):
    contrato_id: int
    fecha_pago: date
    monto: float
    metodo: str
    observacion: Optional[str] = None
    # Agregamos esto aquí para que sea parte base
    comprobante_url: Optional[str] = None 

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel):
    fecha_pago: Optional[date] = None
    monto: Optional[float] = None
    metodo: Optional[str] = None
    observacion: Optional[str] = None
    # También permitimos actualizar la foto si quisieras a futuro
    comprobante_url: Optional[str] = None

class PagoResponse(PagoBase):
    id: int

    class Config:
        from_attributes = True

class PagoResumen(BaseModel):
    contrato_id: int
    monto_total: float
    adelanto: float
    total_pagos: float
    total_pagado: float
    saldo: float
    estado: str