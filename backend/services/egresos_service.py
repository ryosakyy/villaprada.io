from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from models.egresos import Egreso
from models.contratos import Contrato
from models.pagos import Pago

# Aquí importamos TODO lo necesario para evitar el ImportError
from schemas.egresos import (
    EgresoCreate, EgresoUpdate,
    ResumenMensual, ResumenAnual, ResumenEgresosContrato,
    UtilidadContrato, UtilidadMensual
)

class EgresoService:

    # ================= CRUD =================

    @staticmethod
    def crear(data: EgresoCreate, db: Session):
        # Nota: El router usa su propia lógica para crear cuando hay fotos,
        # pero mantenemos esto para creaciones simples si fuera necesario.
        egreso = Egreso(**data.dict())
        db.add(egreso)
        db.commit()
        db.refresh(egreso)
        return egreso

    @staticmethod
    def listar(db: Session):
        return db.query(Egreso).all()

    @staticmethod
    def obtener(id: int, db: Session):
        return db.query(Egreso).filter(Egreso.id == id).first()

    @staticmethod
    def actualizar(id: int, data: EgresoUpdate, db: Session):
        egreso = db.query(Egreso).filter(Egreso.id == id).first()
        if not egreso:
            return None
        
        for campo, valor in data.dict(exclude_unset=True).items():
            setattr(egreso, campo, valor)

        db.commit()
        db.refresh(egreso)
        return egreso

    @staticmethod
    def eliminar(id: int, db: Session):
        egreso = db.query(Egreso).filter(Egreso.id == id).first()
        if not egreso:
            return None
        db.delete(egreso)
        db.commit()
        return True


    # ============= RESÚMENES PRO =============

    @staticmethod
    def resumen_contrato(contrato_id: int, db: Session):
        total = db.query(
            func.coalesce(func.sum(Egreso.monto), 0)
        ).filter(Egreso.contrato_id == contrato_id).scalar()

        return ResumenEgresosContrato(
            contrato_id=contrato_id,
            total_egresos=total
        )

    @staticmethod
    def resumen_mensual(anio: int, mes: int, db: Session):
        total = db.query(
            func.coalesce(func.sum(Egreso.monto), 0)
        ).filter(
            extract("year", Egreso.fecha) == anio,
            extract("month", Egreso.fecha) == mes
        ).scalar()

        return ResumenMensual(
            anio=anio,
            mes=mes,
            total_egresos=total
        )

    @staticmethod
    def resumen_anual(anio: int, db: Session):
        total = db.query(
            func.coalesce(func.sum(Egreso.monto), 0)
        ).filter(
            extract("year", Egreso.fecha) == anio
        ).scalar()

        return ResumenAnual(
            anio=anio,
            total_egresos=total
        )


    # ============= UTILIDADES =============

    @staticmethod
    def utilidad_contrato(contrato_id: int, db: Session):
        contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
        if not contrato:
            return None

        # ingresos = adelanto + pagos
        total_pagos = db.query(
            func.coalesce(func.sum(Pago.monto), 0)
        ).filter(Pago.contrato_id == contrato_id).scalar()

        ingresos = contrato.adelanto + total_pagos

        # egresos asociados
        egresos = db.query(
            func.coalesce(func.sum(Egreso.monto), 0)
        ).filter(Egreso.contrato_id == contrato_id).scalar()

        utilidad = ingresos - egresos

        return UtilidadContrato(
            contrato_id=contrato_id,
            ingresos=ingresos,
            egresos=egresos,
            utilidad=utilidad
        )

    @staticmethod
    def utilidad_mensual(anio: int, mes: int, db: Session):
        
        # ingresos del mes
        ingresos = db.query(func.coalesce(
            func.sum(Pago.monto), 0
        )).filter(
            extract("year", Pago.fecha_pago) == anio,
            extract("month", Pago.fecha_pago) == mes
        ).scalar()

        # egresos del mes
        egresos = db.query(func.coalesce(
            func.sum(Egreso.monto), 0
        )).filter(
            extract("year", Egreso.fecha) == anio,
            extract("month", Egreso.fecha) == mes
        ).scalar()

        utilidad = ingresos - egresos

        return UtilidadMensual(
            anio=anio,
            mes=mes,
            ingresos=ingresos,
            egresos=egresos,
            utilidad=utilidad
        )