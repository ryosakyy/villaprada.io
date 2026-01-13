from sqlalchemy import Column, Integer, String, Date, Time, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    fecha_evento = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    paquete = Column(String(100), nullable=False)
    monto_total = Column(Float, nullable=False)
    adelanto = Column(Float, default=0)
    saldo = Column(Float, default=0)

    estado = Column(String(20), default="activo")
    fecha_creacion = Column(DateTime, default=datetime.now)

    cliente = relationship("Cliente")