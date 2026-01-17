from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, Date
from models.disponibilidad import Disponibilidad
from datetime import date, datetime
from fastapi import HTTPException


class DisponibilidadService:

    @staticmethod
    def verificar_fecha(fecha: date, db: Session, hora_inicio=None, hora_fin=None):
        # 1. Bloquear fechas pasadas
        hoy = date.today()
        if fecha < hoy:
            raise HTTPException(status_code=400, detail="No se pueden registrar eventos en fechas pasadas.")

        # 2. Consultar registros para esa fecha
        query = db.query(Disponibilidad).filter(Disponibilidad.fecha == fecha)

        # 3. Si no hay horario (bloqueo total del día), buscamos cualquier registro que exista
        if not hora_inicio or not hora_fin:
            return query.first()

        # 4. Si hay horario, buscamos traslapes
        # Un traslape ocurre si:
        # (nueva_inicio < existente_fin) Y (nueva_fin > existente_inicio)
        overlap = query.filter(
            and_(
                Disponibilidad.hora_inicio < hora_fin,
                Disponibilidad.hora_fin > hora_inicio
            )
        ).first()

        return overlap

    @staticmethod
    def registrar_ocupado(fecha, motivo, db: Session, hora_inicio=None, hora_fin=None):
        ocupado = Disponibilidad(
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            estado="ocupado",
            motivo=motivo
        )
        db.add(ocupado)
        db.commit()
        db.refresh(ocupado)
        return ocupado

    @staticmethod
    def registrar_bloqueado(fecha, motivo, db: Session):
        bloqueado = Disponibilidad(
            fecha=fecha,
            estado="bloqueado",
            motivo=motivo
        )
        db.add(bloqueado)
        db.commit()
        db.refresh(bloqueado)
        return bloqueado

    @staticmethod
    def liberar_fecha(fecha: str, db: Session):
        registro = db.query(Disponibilidad).filter(
            Disponibilidad.fecha == fecha
        ).first()
        if registro:
            db.delete(registro)
            db.commit()
            return True
        return False
