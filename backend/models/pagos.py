from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=False)

    fecha_pago = Column(Date, nullable=False)
    monto = Column(Float, nullable=False)
    metodo = Column(String(50), nullable=False)   # efectivo, yape, transferencia, etc.
    observacion = Column(String(255), nullable=True)
    
    # --- NUEVO CAMPO ---
    comprobante_url = Column(String(500), nullable=True)
    # -------------------

    fecha_creacion = Column(DateTime, default=datetime.now)

    contrato = relationship("Contrato")