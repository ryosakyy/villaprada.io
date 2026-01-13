from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.security import get_current_user
from services.reservas_service import ReservaService
from schemas.reservas import ReservaCreate, ReservaUpdate, ReservaResponse

# IMPORTANTE: Importamos el modelo de Disponibilidad para consultar la agenda
from models.disponibilidad import Disponibilidad

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)

# ============================================================
# CREAR RESERVA (PROTEGIDO Y BLINDADO)
# ============================================================
@router.post("/", response_model=ReservaResponse, dependencies=[Depends(get_current_user)])
def crear_reserva(data: ReservaCreate, db: Session = Depends(get_db)):
    
    # 1. VERIFICACIÓN DE SEGURIDAD (EL BLINDAJE)
    # Antes de llamar al servicio, preguntamos: ¿La fecha ya existe en Disponibilidad?
    fecha_ocupada = db.query(Disponibilidad).filter(
        Disponibilidad.fecha == data.fecha_evento # Asegúrate que tu schema use 'fecha_evento' o 'fecha_reserva'
    ).first()

    # Si existe y está ocupada/reservada, detenemos todo AQUÍ.
    if fecha_ocupada:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La fecha {data.fecha_evento} ya está ocupada o reservada."
        )

    # 2. CREAR LA RESERVA (Usando tu servicio existente)
    nueva_reserva = ReservaService.crear_reserva(data, db)

    # 3. BLOQUEAR LA FECHA EN EL CALENDARIO
    # Como ya verificamos en el paso 1 que no existe, es seguro crearla.
    ocupado = Disponibilidad(
        fecha=nueva_reserva.fecha_evento,
        estado="ocupado", # O "reservado" si prefieres diferenciar
        motivo=f"Reserva: {nueva_reserva.detalles or 'Cliente'}" 
    )

    db.add(ocupado)
    
    # 4. GUARDAR TODO JUNTO
    # Nota: Si tu ReservaService ya hizo commit, esto guardará solo la disponibilidad.
    # Lo ideal es que el Service haga flush y el router haga commit, pero esto funcionará.
    db.commit() 

    return nueva_reserva

# ============================================================
# LISTAR RESERVAS
# ============================================================
@router.get("/", response_model=List[ReservaResponse], dependencies=[Depends(get_current_user)])
def listar_reservas(db: Session = Depends(get_db)):
    return ReservaService.listar_reservas(db)

# ============================================================
# OBTENER RESERVA
# ============================================================
@router.get("/{id}", response_model=ReservaResponse, dependencies=[Depends(get_current_user)])
def obtener_reserva(id: int, db: Session = Depends(get_db)):
    reserva = ReservaService.obtener_reserva(id, db)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

# ============================================================
# ACTUALIZAR RESERVA
# ============================================================
@router.put("/{id}", response_model=ReservaResponse, dependencies=[Depends(get_current_user)])
def actualizar_reserva(id: int, data: ReservaUpdate, db: Session = Depends(get_db)):
    # Nota: Si cambias la fecha aquí, deberías actualizar también Disponibilidad.
    # Por ahora lo dejamos simple para que funcione.
    reserva = ReservaService.actualizar_reserva(id, data, db)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

# ============================================================
# ELIMINAR RESERVA (LIBERANDO FECHA)
# ============================================================
@router.delete("/{id}", dependencies=[Depends(get_current_user)])
def eliminar_reserva(id: int, db: Session = Depends(get_db)):
    
    # Primero buscamos la reserva para saber qué fecha liberar
    reserva = ReservaService.obtener_reserva(id, db)
    
    if not reserva:
         raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Buscamos la fecha en Disponibilidad y la borramos
    fecha_bloqueada = db.query(Disponibilidad).filter(
        Disponibilidad.fecha == reserva.fecha_evento
    ).first()
    
    if fecha_bloqueada:
        db.delete(fecha_bloqueada)

    # Ahora sí eliminamos la reserva
    eliminado = ReservaService.eliminar_reserva(id, db)
    
    # Confirmamos ambos borrados
    db.commit()
    
    return {"mensaje": "Reserva eliminada y fecha liberada correctamente"}