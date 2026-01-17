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
@router.post("/", response_model=EgresoResponse)
def crear(
    descripcion: str = Form(...),
    monto: float = Form(...),
    categoria: str = Form(...),
    fecha: date = Form(...),
    observacion: Optional[str] = Form(None),
    contrato_id: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None), # Archivo opcional
    current_user: dict = Depends(get_current_user),  # Obtener usuario actual
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

    # 2. Creamos el objeto manualmente, ahora incluyendo usuario_id
    sub = current_user.get("sub")
    u_id = None
    
    # Robustez: Si sub es email (token antiguo o inconsistente), buscamos el ID
    if isinstance(sub, str) and "@" in sub:
        from models.usuarios import Usuario
        user_obj = db.query(Usuario).filter(Usuario.email == sub).first()
        if user_obj:
            u_id = user_obj.id
    else:
        try:
            u_id = int(sub) if sub else None
        except (ValueError, TypeError):
            u_id = None

    print(f"DEBUG: Registrando egreso - sub: {sub}, final u_id: {u_id}, Cat: {categoria}")

    nuevo_egreso = Egreso(
        descripcion=descripcion,
        monto=monto,
        categoria=categoria,
        fecha=fecha,
        observacion=observacion,
        contrato_id=contrato_id,
        comprobante_url=ruta_imagen,
        usuario_id=u_id
    )

    # 3. Guardar en BD
    db.add(nuevo_egreso)
    db.commit()
    db.refresh(nuevo_egreso)
    
    # Asegurarnos de que cargue la relación para el retorno
    db.refresh(nuevo_egreso, ["usuario"])
    
    return {
        "id": nuevo_egreso.id,
        "descripcion": nuevo_egreso.descripcion,
        "monto": nuevo_egreso.monto,
        "categoria": nuevo_egreso.categoria,
        "fecha": nuevo_egreso.fecha,
        "observacion": nuevo_egreso.observacion,
        "contrato_id": nuevo_egreso.contrato_id,
        "comprobante_url": nuevo_egreso.comprobante_url,
        "usuario_id": nuevo_egreso.usuario_id,
        "usuario_nombre": nuevo_egreso.usuario.nombres if nuevo_egreso.usuario else "Sistema",
        "usuario_rol": nuevo_egreso.usuario.rol if nuevo_egreso.usuario else "admin"
    }

# --- RESTO DE ENDPOINTS (Iguales que antes) ---

@router.get("/", response_model=List[EgresoResponse])
def listar(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sub = current_user.get("sub")
    rol = current_user.get("rol")
    u_id = None

    # Robustez: Si sub es email (token antiguo), buscamos el ID
    if isinstance(sub, str) and "@" in sub:
        from models.usuarios import Usuario
        user_obj = db.query(Usuario).filter(Usuario.email == sub).first()
        if user_obj:
            u_id = user_obj.id
    else:
        try:
            u_id = int(sub) if sub else None
        except (ValueError, TypeError):
            u_id = None
    
    egresos = EgresoService.listar(db, user_id=u_id, rol=rol)
    
    resultado = []
    for egreso in egresos:
        # Usamos los datos del objeto, garantizando que el usuario esté cargado por joinedload
        nombre_u = egreso.usuario.nombres if egreso.usuario else "S/N"
        rol_u = egreso.usuario.rol if egreso.usuario else "admin"
        
        resultado.append({
            "id": egreso.id,
            "descripcion": egreso.descripcion,
            "monto": egreso.monto,
            "categoria": egreso.categoria,
            "fecha": egreso.fecha,
            "observacion": egreso.observacion,
            "contrato_id": egreso.contrato_id,
            "comprobante_url": egreso.comprobante_url,
            "usuario_id": egreso.usuario_id,
            "usuario_nombre": nombre_u,
            "usuario_rol": rol_u
        })
    
    return resultado

@router.delete("/{id}", dependencies=[Depends(get_current_user)])
def eliminar(id: int, db: Session = Depends(get_db)):
    EgresoService.eliminar(id, db)
    return {"mensaje": "Eliminado"}

# (Agrega aquí tus endpoints de resumen y utilidad que ya tenías)