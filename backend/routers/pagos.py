import shutil
import os
import uuid
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_user
from services.pagos_service import PagoService
from schemas.pagos import PagoCreate, PagoUpdate, PagoResponse, PagoResumen

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"]
)

# Directorio donde se guardarán las imágenes
UPLOAD_DIR = "static/pagos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ============================================================
# CREAR PAGO CON IMAGEN (PROTEGIDO)
# ============================================================
@router.post("/", response_model=PagoResponse, dependencies=[Depends(get_current_user)])
def crear_pago(
    contrato_id: int = Form(...),
    monto: float = Form(...),
    fecha_pago: date = Form(...),
    metodo: str = Form(...),
    observacion: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None), # Archivo opcional
    db: Session = Depends(get_db)
):
    ruta_imagen = None

    # 1. Guardar archivo si existe
    if file:
        extension = file.filename.split(".")[-1]
        nombre_unico = f"{uuid.uuid4()}.{extension}"
        ruta_archivo = os.path.join(UPLOAD_DIR, nombre_unico)
        
        with open(ruta_archivo, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Ruta relativa para la BD (ej: static/pagos/foto.jpg)
        ruta_imagen = f"{UPLOAD_DIR}/{nombre_unico}"

    # 2. Crear objeto Schema manualmente para pasarlo al Servicio
    # Esto permite reutilizar toda la lógica de validación de tu servicio
    pago_data = PagoCreate(
        contrato_id=contrato_id,
        monto=monto,
        fecha_pago=fecha_pago,
        metodo=metodo,
        observacion=observacion,
        comprobante_url=ruta_imagen
    )

    try:
        return PagoService.crear_pago(pago_data, db)
    except ValueError as e:
        # Si falló, podríamos borrar la imagen subida para no dejar basura, 
        # pero por ahora simplemente lanzamos el error.
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================
# LISTAR PAGOS (PROTEGIDO)
# ============================================================
@router.get("/", response_model=List[PagoResponse], dependencies=[Depends(get_current_user)])
def listar_pagos(db: Session = Depends(get_db)):
    return PagoService.listar_pagos(db)


# ============================================================
# OBTENER PAGO (PROTEGIDO)
# ============================================================
@router.get("/{id}", response_model=PagoResponse, dependencies=[Depends(get_current_user)])
def obtener_pago(id: int, db: Session = Depends(get_db)):
    pago = PagoService.obtener_pago(id, db)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago


# ============================================================
# PAGOS POR CONTRATO (PROTEGIDO)
# ============================================================
@router.get("/contrato/{contrato_id}", response_model=List[PagoResponse], dependencies=[Depends(get_current_user)])
def pagos_por_contrato(contrato_id: int, db: Session = Depends(get_db)):
    return PagoService.listar_pagos_por_contrato(contrato_id, db)


# ============================================================
# ACTUALIZAR PAGO (PROTEGIDO)
# ============================================================
@router.put("/{id}", response_model=PagoResponse, dependencies=[Depends(get_current_user)])
def actualizar_pago(id: int, data: PagoUpdate, db: Session = Depends(get_db)):
    try:
        pago = PagoService.actualizar_pago(id, data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago


# ============================================================
# ELIMINAR PAGO (PROTEGIDO)
# ============================================================
@router.delete("/{id}", dependencies=[Depends(get_current_user)])
def eliminar_pago(id: int, db: Session = Depends(get_db)):
    eliminado = PagoService.eliminar_pago(id, db)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return {"mensaje": "Pago eliminado correctamente"}


# ============================================================
# RESUMEN DEL CONTRATO (PROTEGIDO)
# ============================================================
@router.get("/resumen/{contrato_id}", response_model=PagoResumen, dependencies=[Depends(get_current_user)])
def resumen_contrato(contrato_id: int, db: Session = Depends(get_db)):
    resumen = PagoService.resumen_contrato(contrato_id, db)
    if not resumen:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    return resumen