# backend/routers/galeria.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from core.security import get_current_user
from core.cloudinary_config import cloudinary

from schemas.galeria import GaleriaCreate, GaleriaUpdate, GaleriaResponse
from services.galeria_service import GaleriaService
from models.galeria import Galeria

router = APIRouter(
    prefix="/galeria",
    tags=["Galería"],
)


# ================================================================
# CREAR GALERÍA (CON IMAGEN)
# ================================================================
@router.post("/", response_model=GaleriaResponse, dependencies=[Depends(get_current_user)])
async def crear_galeria(
    titulo: str = Form(...),
    descripcion: Optional[str] = Form(None),
    categoria: Optional[str] = Form(None),
    contrato_id: Optional[str] = Form(None),
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if contrato_id in (None, "", "0"):
        contrato_id_final = None
    else:
        contrato_id_final = int(contrato_id)

    # Subir imagen
    try:
        result = cloudinary.uploader.upload(
            imagen.file,
            folder="villa_prada/galeria",
            resource_type="image"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo imagen: {e}")

    imagen_url = result["secure_url"]
    public_id = result["public_id"]

    data = GaleriaCreate(
        titulo=titulo,
        descripcion=descripcion,
        categoria=categoria,
        contrato_id=contrato_id_final
    )

    nuevo = GaleriaService.crear_galeria(db, data, imagen_url, public_id)
    return nuevo


# ================================================================
# LISTAR TODAS LAS IMÁGENES
# ================================================================
@router.get("/", response_model=List[GaleriaResponse])
def listar_galeria(db: Session = Depends(get_db)):
    return GaleriaService.listar_galeria(db)


# ================================================================
# GALERÍA LIGERA (SÓLO MINI DATOS PARA PÁGINA PÚBLICA)
# ================================================================
@router.get("/light-list")
def galeria_light(db: Session = Depends(get_db)):
    return GaleriaService.galeria_light(db)


# ================================================================
# BUSCAR (debe ir antes de /{id})
# ================================================================
@router.get("/buscar/{texto}", response_model=List[GaleriaResponse])
def buscar(texto: str, db: Session = Depends(get_db)):
    return GaleriaService.buscar(db, texto)


# ================================================================
# OBTENER POR ID
# ================================================================
@router.get("/{id}", response_model=GaleriaResponse)
def obtener_galeria(id: int, db: Session = Depends(get_db)):
    gal = GaleriaService.obtener_galeria(id, db)
    if not gal:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    return gal


# ================================================================
# MOSTRAR SOLO LA IMAGEN (URL DIRECTA)
# ================================================================
@router.get("/imagen/{id}")
def obtener_imagen(id: int, db: Session = Depends(get_db)):
    gal = GaleriaService.obtener_galeria(id, db)
    if not gal:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    return {"url": gal.imagen_url}


# ================================================================
# LISTAR POR CATEGORÍA
# ================================================================
@router.get("/categoria/{categoria}", response_model=List[GaleriaResponse])
def listar_por_categoria(categoria: str, db: Session = Depends(get_db)):
    return GaleriaService.listar_por_categoria(categoria, db)


# ================================================================
# EDITAR INFORMACIÓN
# ================================================================
@router.put("/{id}", response_model=GaleriaResponse, dependencies=[Depends(get_current_user)])
def actualizar_galeria(id: int, data: GaleriaUpdate, db: Session = Depends(get_db)):
    gal = GaleriaService.actualizar_galeria(id, data, db)
    if not gal:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")
    return gal


# ================================================================
# CAMBIAR SOLO LA IMAGEN
# ================================================================
@router.put("/{id}/imagen", response_model=GaleriaResponse, dependencies=[Depends(get_current_user)])
async def actualizar_imagen(id: int, nueva_imagen: UploadFile = File(...), db: Session = Depends(get_db)):

    gal = GaleriaService.obtener_galeria(id, db)
    if not gal:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    # Eliminar imagen anterior
    try:
        cloudinary.uploader.destroy(gal.public_id)
    except:
        pass

    # Subir nueva imagen
    try:
        result = cloudinary.uploader.upload(
            nueva_imagen.file,
            folder="villa_prada/galeria"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo imagen nueva: {e}")

    gal.imagen_url = result["secure_url"]
    gal.public_id = result["public_id"]

    db.commit()
    db.refresh(gal)

    return gal


# ================================================================
# ELIMINAR ELEMENTO DE LA GALERÍA
# ================================================================
@router.delete("/{id}", dependencies=[Depends(get_current_user)])
def eliminar_galeria(id: int, db: Session = Depends(get_db)):

    gal = GaleriaService.obtener_galeria(id, db)
    if not gal:
        raise HTTPException(status_code=404, detail="Elemento no encontrado")

    try:
        cloudinary.uploader.destroy(gal.public_id)
    except:
        pass

    GaleriaService.eliminar_galeria(id, db)
    return {"mensaje": "Elemento eliminado correctamente"}


# ================================================================
# PAGINADO
# ================================================================
@router.get("/paginado", response_model=List[GaleriaResponse])
def paginado(page: int = 1, limit: int = 12, db: Session = Depends(get_db)):
    return GaleriaService.paginado(db, page, limit)





# ================================================================
# SUBIDA MÚLTIPLE
# ================================================================
@router.post("/multiple", response_model=List[GaleriaResponse], dependencies=[Depends(get_current_user)])
async def subir_multiple(
    categoria: Optional[str] = Form(None),
    contrato_id: Optional[str] = Form(None),
    imagenes: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):

    if contrato_id in (None, "", "0"):
        contrato_id_final = None
    else:
        contrato_id_final = int(contrato_id)

    return GaleriaService.crear_galeria_masiva(
        db=db,
        archivos=imagenes,
        categoria=categoria,
        contrato_id=contrato_id_final
    )


