from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Egreso(Base):
    __tablename__ = "egresos"

    id = Column(Integer, primary_key=True, index=True)
    
    descripcion = Column(String(255), nullable=False)
    monto = Column(Float, nullable=False)
    categoria = Column(String(100), nullable=False)
    
    fecha = Column(Date, nullable=False)
    observacion = Column(String(255), nullable=True)

    # --- NUEVO CAMPO ---
    comprobante_url = Column(String(500), nullable=True) 
    # -------------------

    contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.now)

    contrato = relationship("Contrato")