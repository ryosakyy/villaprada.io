from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.reservas import Reserva
from schemas.reservas import ReservaCreate, ReservaUpdate
from services.disponibilidad_service import DisponibilidadService


class ReservaService:

    @staticmethod
    def crear_reserva(data: ReservaCreate, db: Session):

        # 🔍 Verificar disponibilidad antes de crear (con horario)
        disponible = DisponibilidadService.verificar_fecha(
            data.fecha_evento, db, data.hora_inicio, data.hora_fin
        )
        if disponible:
            raise HTTPException(
                status_code=400,
                detail=f"El horario {data.hora_inicio}-{data.hora_fin} para la fecha {data.fecha_evento} ya está ocupado."
            )

        reserva = Reserva(
            cliente_id=data.cliente_id,
            contrato_id=data.contrato_id,
            fecha_evento=data.fecha_evento,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
            estado=data.estado,
            observaciones=data.observaciones
        )

        db.add(reserva)
        db.commit()
        db.refresh(reserva)

        # Registrar ocupación con horario
        DisponibilidadService.registrar_ocupado(
            fecha=data.fecha_evento,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
            motivo=f"Reserva ID {reserva.id}",
            db=db
        )

        return reserva

    @staticmethod
    def listar_reservas(db: Session):
        return db.query(Reserva).all()

    @staticmethod
    def obtener_reserva(id: int, db: Session):
        return db.query(Reserva).filter(Reserva.id == id).first()

    @staticmethod
    def actualizar_reserva(id: int, data: ReservaUpdate, db: Session):
        reserva = db.query(Reserva).filter(Reserva.id == id).first()
        if not reserva:
            return None

        fecha_original = reserva.fecha_evento
        nueva_fecha = data.fecha_evento

        # Si la fecha NO cambia, actualizar normal
        if not nueva_fecha or nueva_fecha == fecha_original:
            for campo, valor in data.dict(exclude_unset=True).items():
                setattr(reserva, campo, valor)
            db.commit()
            db.refresh(reserva)
            return reserva

        # Si cambia algo relevante → validar disponibilidad
        h_ini = data.hora_inicio or reserva.hora_inicio
        h_fin = data.hora_fin or reserva.hora_fin
        f_evt = data.fecha_evento or reserva.fecha_evento

        disponible = DisponibilidadService.verificar_fecha(f_evt, db, h_ini, h_fin)
        if disponible:
            raise HTTPException(
                status_code=400,
                detail=f"No se puede cambiar. El horario solicitado ya está ocupado."
            )

        # Liberar fecha antigua
        DisponibilidadService.liberar_fecha(fecha_original, db)

        # Registrar nueva fecha como ocupada
        DisponibilidadService.registrar_ocupado(
            fecha=nueva_fecha,
            hora_inicio=h_ini,
            hora_fin=h_fin,
            motivo=f"Reserva ID {reserva.id}",
            db=db
        )

        # Actualizar reserva
        for campo, valor in data.dict(exclude_unset=True).items():
            setattr(reserva, campo, valor)

        db.commit()
        db.refresh(reserva)
        return reserva

    @staticmethod
    def eliminar_reserva(id: int, db: Session):
        reserva = db.query(Reserva).filter(Reserva.id == id).first()
        if not reserva:
            return None

        # Liberar fecha ocupada
        DisponibilidadService.liberar_fecha(reserva.fecha_evento, db)

        db.delete(reserva)
        db.commit()
        return True
