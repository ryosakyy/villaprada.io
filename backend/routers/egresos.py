import shutil
import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from core.database import get_db
from core.security import get_current_user
from models.egresos import Egreso
from schemas.egresos import EgresoResponse, EgresoUpdate
from services.egresos_service import EgresoService

router = APIRouter(prefix="/egresos", tags=["Egresos"])

# Carpeta donde se guardan las fotos
UPLOAD_DIR = "static/comprobantes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- CREAR EGRESO CON IMAGEN ---
@router.post("/", response_model=EgresoResponse, dependencies=[Depends(get_current_user)])
def crear(
    descripcion: str = Form(...),
    monto: float = Form(...),
    categoria: str = Form(...),
    fecha: date = Form(...),
    observacion: Optional[str] = Form(None),
    contrato_id: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None), # Archivo opcional
    db: Session = Depends(get_db)
):
    ruta_imagen = None

    # 1. Si hay archivo, lo guardamos
    if file:
        extension = file.filename.split(".")[-1]
        nombre_unico = f"{uuid.uuid4()}.{extension}"
        ruta_archivo = os.path.join(UPLOAD_DIR, nombre_unico)
        
        with open(ruta_archivo, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Guardamos la ruta relativa (ej: static/comprobantes/abc.jpg)
        ruta_imagen = f"{UPLOAD_DIR}/{nombre_unico}"

    # 2. Creamos el objeto manualmente (ya que no viene como JSON Pydantic)
    nuevo_egreso = Egreso(
        descripcion=descripcion,
        monto=monto,
        categoria=categoria,
        fecha=fecha,
        observacion=observacion,
        contrato_id=contrato_id,
        comprobante_url=ruta_imagen
    )

    # 3. Guardar en BD
    db.add(nuevo_egreso)
    db.commit()
    db.refresh(nuevo_egreso)
    
    return nuevo_egreso

# --- RESTO DE ENDPOINTS (Iguales que antes) ---

@router.get("/", response_model=List[EgresoResponse], dependencies=[Depends(get_current_user)])
def listar(db: Session = Depends(get_db)):
    return EgresoService.listar(db)

@router.delete("/{id}", dependencies=[Depends(get_current_user)])
def eliminar(id: int, db: Session = Depends(get_db)):
    EgresoService.eliminar(id, db)
    return {"mensaje": "Eliminado"}

# (Agrega aquí tus endpoints de resumen y utilidad que ya tenías)