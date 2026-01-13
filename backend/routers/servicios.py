from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# --- IMPORTACIONES CORREGIDAS (Rutas Absolutas) ---
from core.database import get_db 
from models.servicios import Servicio
from schemas.servicios import ServicioCreate, ServicioResponse

router = APIRouter(
    prefix="/servicios",
    tags=["Servicios"]
)

# 1. Obtener todos los servicios
@router.get("/", response_model=List[ServicioResponse])
def listar_servicios(db: Session = Depends(get_db)):
    return db.query(Servicio).all()

# 2. Crear un nuevo servicio
@router.post("/", response_model=ServicioResponse)
def crear_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    nuevo_servicio = Servicio(**servicio.dict())
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio

# 3. Eliminar servicio
@router.delete("/{id}")
def eliminar_servicio(id: int, db: Session = Depends(get_db)):
    servicio = db.query(Servicio).filter(Servicio.id == id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    db.delete(servicio)
    db.commit()
    return {"message": "Servicio eliminado correctamente"}