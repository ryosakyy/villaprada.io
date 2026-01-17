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

    # --- Campo para imagen de comprobante ---
    comprobante_url = Column(String(500), nullable=True) 

    # --- Campo para rastrear quién hizo el egreso ---
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.now)

    # Relaciones
    contrato = relationship("Contrato")
    usuario = relationship("Usuario")

    @property
    def usuario_nombre(self):
        return self.usuario.nombres if self.usuario else None

    @property
    def usuario_rol(self):
        return self.usuario.rol if self.usuario else "empleado" # Default if not found