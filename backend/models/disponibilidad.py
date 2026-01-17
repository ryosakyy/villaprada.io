from sqlalchemy import Column, Integer, Date, String, Boolean, Time
from core.database import Base

class Disponibilidad(Base):
    __tablename__ = "disponibilidad"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False) # Eliminamos unique=True
    hora_inicio = Column(Time, nullable=True)
    hora_fin = Column(Time, nullable=True)
    estado = Column(String(20), default="ocupado")  # ocupado | libre | bloqueado
    motivo = Column(String(255), nullable=True)  # mantenimiento, evento, contrato, etc.
