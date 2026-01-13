from sqlalchemy import Column, Integer, String, Float, Text, DateTime, func
from core.database import Base  # <--- CORREGIDO: Sin los dos puntos ".."

class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Float, nullable=False)
    estado = Column(String(20), default="activo")
    fecha_creacion = Column(DateTime, server_default=func.now())