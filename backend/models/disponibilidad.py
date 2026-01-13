from sqlalchemy import Column, Integer, Date, String, Boolean, Time
from core.database import Base

class Disponibilidad(Base):
    __tablename__ = "disponibilidad"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, unique=True, nullable=False)
    estado = Column(String(20), default="ocupado")  # ocupado | libre | bloqueado
    motivo = Column(String(255), nullable=True)  # mantenimiento, evento, contrato, etc.
