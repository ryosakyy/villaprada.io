from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.contratos import Contrato
from schemas.contratos import ContratoCreate, ContratoUpdate
from services.disponibilidad_service import DisponibilidadService


class ContratoService:

    @staticmethod
    def crear_contrato(data: ContratoCreate, db: Session):

        # Validar disponibilidad con horario
        disponible = DisponibilidadService.verificar_fecha(
            data.fecha_evento, db, data.hora_inicio, data.hora_fin
        )
        if disponible:
            raise HTTPException(
                status_code=400,
                detail=f"El horario {data.hora_inicio}-{data.hora_fin} para la fecha {data.fecha_evento} ya está ocupado."
            )

        contrato = Contrato(
            cliente_id=data.cliente_id,
            fecha_evento=data.fecha_evento,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
            paquete=data.paquete,
            monto_total=data.monto_total,
            adelanto=data.adelanto,
            saldo=data.monto_total - data.adelanto,
            estado=data.estado
        )

        db.add(contrato)
        db.commit()
        db.refresh(contrato)

        # Registrar fecha como ocupada con horario
        DisponibilidadService.registrar_ocupado(
            fecha=data.fecha_evento,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
            motivo=f"Contrato ID {contrato.id}",
            db=db
        )

        return contrato

    @staticmethod
    def listar_contratos(db: Session):
        return db.query(Contrato).all()

    @staticmethod
    def obtener_contrato(id: int, db: Session):
        return db.query(Contrato).filter(Contrato.id == id).first()

    @staticmethod
    def actualizar_contrato(id: int, data: ContratoUpdate, db: Session):
        contrato = db.query(Contrato).filter(Contrato.id == id).first()
        if not contrato:
            return None

        fecha_original = contrato.fecha_evento
        nueva_fecha = data.fecha_evento

        # Si no cambia fecha → actualizar normal
        if not nueva_fecha or nueva_fecha == fecha_original:
            for campo, valor in data.dict(exclude_unset=True).items():
                setattr(contrato, campo, valor)
            db.commit()
            db.refresh(contrato)
            return contrato

        # Si cambia → validar con nuevo horario
        h_ini = data.hora_inicio or contrato.hora_inicio
        h_fin = data.hora_fin or contrato.hora_fin
        f_evt = data.fecha_evento or contrato.fecha_evento

        disponible = DisponibilidadService.verificar_fecha(f_evt, db, h_ini, h_fin)
        # Nota: si es la misma reserva, el overlap fallará detectándose a sí misma si hiciéramos un flush.
        # Por ahora lo dejamos así y si da problemas filtramos el ID del contrato actual en verificar_fecha.
        if disponible:
            raise HTTPException(
                status_code=400,
                detail=f"No se puede cambiar. El horario solicitado ya está ocupado."
            )

        # Liberar la fecha original
        DisponibilidadService.liberar_fecha(fecha_original, db)

        # Registrar nueva fecha
        DisponibilidadService.registrar_ocupado(
            fecha=nueva_fecha,
            motivo=f"Contrato ID {contrato.id}",
            db=db
        )

        # Actualizar datos
        for campo, valor in data.dict(exclude_unset=True).items():
            setattr(contrato, campo, valor)

        db.commit()
        db.refresh(contrato)
        return contrato

    @staticmethod
    def eliminar_contrato(id: int, db: Session):
        contrato = db.query(Contrato).filter(Contrato.id == id).first()
        if not contrato:
            return None

        # Liberar fecha
        DisponibilidadService.liberar_fecha(contrato.fecha_evento, db)

        db.delete(contrato)
        db.commit()
        return True
