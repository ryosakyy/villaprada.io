# backend/routers/disponibilidad.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from core.security import get_current_user
from models.disponibilidad import Disponibilidad
from models.reservas import Reserva
from schemas.disponibilidad import DisponibilidadCreate, DisponibilidadOut, DisponibilidadUpdate

import calendar

router = APIRouter(
    prefix="/disponibilidad",
    tags=["Disponibilidad"]
)

# ============================================================
# 0. Endpoint PÚBLICO para landing page (SIN TOKEN)
# ============================================================
@router.get("/publico/fechas-ocupadas")
def fechas_ocupadas_publico(anio: int = None, mes: int = None, db: Session = Depends(get_db)):
    """
    Retorna fechas ocupadas con detalle de horarios para la landing page.
    Si no se especifica mes/anio, retorna todo (o se podría limitar a hoy en adelante).
    """
    query = db.query(Disponibilidad).filter(Disponibilidad.estado.in_(["ocupado", "bloqueado"]))

    if anio and mes:
        # Filtrar por mes específico
        from sqlalchemy import extract
        query = query.filter(
            extract('year', Disponibilidad.fecha) == anio,
            extract('month', Disponibilidad.fecha) == mes
        )
    
    registros_disponibilidad = query.all()

    # Query Reservas (Events)
    query_reservas = db.query(Reserva).filter(Reserva.estado.in_(["confirmado", "pendiente"]))
    if anio and mes:
        query_reservas = query_reservas.filter(
            extract('year', Reserva.fecha_evento) == anio,
            extract('month', Reserva.fecha_evento) == mes
        )
    registros_reservas = query_reservas.all()
    
    # Merge results
    resultados = []

    # Add manual blocks
    for r in registros_disponibilidad:
        resultados.append({
            "fecha": r.fecha,
            "hora_inicio": str(r.hora_inicio) if r.hora_inicio else None,
            "hora_fin": str(r.hora_fin) if r.hora_fin else None,
            "estado": r.estado
        })

    # Add reservations (as "ocupado")
    for r in registros_reservas:
        resultados.append({
            "fecha": r.fecha_evento,
            "hora_inicio": str(r.hora_inicio) if r.hora_inicio else None,
            "hora_fin": str(r.hora_fin) if r.hora_fin else None,
            "estado": "ocupado"
        })
    
    # Sort by date
    resultados.sort(key=lambda x: (x['fecha'], x['hora_inicio'] or '00:00:00'))

    return resultados


# ============================================================
# 1. Crear / Bloquear fecha (PROTEGIDO)
# ============================================================
@router.post("/", response_model=DisponibilidadOut, dependencies=[Depends(get_current_user)])
def bloquear_fecha(data: DisponibilidadCreate, db: Session = Depends(get_db)):
    existe = db.query(Disponibilidad).filter(Disponibilidad.fecha == data.fecha).first()
    if existe:
        raise HTTPException(status_code=400, detail="La fecha ya está registrada.")

    nueva = Disponibilidad(
        fecha=data.fecha,
        estado=data.estado,
        motivo=data.motivo
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# ============================================================
# 2. Obtener una fecha por ID (PROTEGIDO)  ← requerido por tu frontend
# ============================================================
@router.get("/{id}", response_model=DisponibilidadOut, dependencies=[Depends(get_current_user)])
def obtener_disponibilidad(id: int, db: Session = Depends(get_db)):
    disp = db.query(Disponibilidad).filter(Disponibilidad.id == id).first()
    if not disp:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return disp

# ============================================================
# 3. Actualizar disponibilidad (PROTEGIDO)
# ============================================================
@router.put("/{id}", response_model=DisponibilidadOut, dependencies=[Depends(get_current_user)])
def actualizar_disponibilidad(id: int, data: DisponibilidadUpdate, db: Session = Depends(get_db)):
    disp = db.query(Disponibilidad).filter(Disponibilidad.id == id).first()
    if not disp:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    disp.estado = data.estado
    disp.motivo = data.motivo

    db.commit()
    db.refresh(disp)
    return disp

# ============================================================
# 4. Listar todas las fechas registradas (PROTEGIDO)
# ============================================================
@router.get("/", response_model=List[DisponibilidadOut], dependencies=[Depends(get_current_user)])
def listar_disponibilidad(db: Session = Depends(get_db)):
    return db.query(Disponibilidad).all()

# ============================================================
# 5. Verificar una fecha (PROTEGIDO)
# ============================================================
@router.get("/verificar/{fecha}", dependencies=[Depends(get_current_user)])
def verificar_fecha(fecha: str, db: Session = Depends(get_db)):
    registro = db.query(Disponibilidad).filter(Disponibilidad.fecha == fecha).first()
    if not registro:
        return {"fecha": fecha, "estado": "libre"}

    return {"fecha": fecha, "estado": registro.estado, "motivo": registro.motivo}

# ============================================================
# 6. Calendario completo (PROTEGIDO)
# ============================================================
@router.get("/calendario", dependencies=[Depends(get_current_user)])
def calendario(db: Session = Depends(get_db)):
    registros = db.query(Disponibilidad).all()
    return [
        {"id": r.id, "fecha": str(r.fecha), "estado": r.estado, "motivo": r.motivo}
        for r in registros
    ]

# ============================================================
# 7. Calendario filtrado por mes (PROTEGIDO)
# ============================================================
@router.get("/calendario/{anio}/{mes}", dependencies=[Depends(get_current_user)])
def calendario_mes(anio: int, mes: int, db: Session = Depends(get_db)):
    registros = db.query(Disponibilidad).filter(
        Disponibilidad.fecha.op("LIKE")(f"{anio}-{mes:02d}-%")
    ).all()

    return [
        {"id": r.id, "fecha": str(r.fecha), "estado": r.estado, "motivo": r.motivo}
        for r in registros
    ]

# ============================================================
# 8. Fechas ocupadas (PROTEGIDO)
# ============================================================
@router.get("/ocupadas", dependencies=[Depends(get_current_user)])
def fechas_ocupadas(db: Session = Depends(get_db)):
    registros = db.query(Disponibilidad).filter(Disponibilidad.estado == "ocupado").all()
    return [
        {"id": r.id, "fecha": str(r.fecha), "motivo": r.motivo}
        for r in registros
    ]

# ============================================================
# 9. Fechas bloqueadas (PROTEGIDO)
# ============================================================
@router.get("/bloqueadas", dependencies=[Depends(get_current_user)])
def fechas_bloqueadas(db: Session = Depends(get_db)):
    registros = db.query(Disponibilidad).filter(Disponibilidad.estado == "bloqueado").all()
    return [
        {"id": r.id, "fecha": str(r.fecha), "motivo": r.motivo}
        for r in registros
    ]

# ============================================================
# 10. Fechas libres por mes (PROTEGIDO)
# ============================================================
@router.get("/libres/{anio}/{mes}", dependencies=[Depends(get_current_user)])
def fechas_libres(anio: int, mes: int, db: Session = Depends(get_db)):
    dias = calendar.monthrange(anio, mes)[1]

    ocupadas = db.query(Disponibilidad).filter(
        Disponibilidad.fecha.op("LIKE")(f"{anio}-{mes:02d}-%")
    ).all()

    ocupadas_fechas = {str(o.fecha) for o in ocupadas}

    libres = []
    for dia in range(1, dias + 1):
        fecha = f"{anio}-{mes:02d}-{dia:02d}"
        if fecha not in ocupadas_fechas:
            libres.append(fecha)

    return {"libres": libres}
