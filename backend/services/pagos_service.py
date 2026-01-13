from sqlalchemy.orm import Session
from sqlalchemy import func
from models.pagos import Pago
from models.contratos import Contrato
from schemas.pagos import PagoCreate, PagoUpdate, PagoResumen

class PagoService:

    # --------- FUNCIONES INTERNAS ---------
    @staticmethod
    def _obtener_totales(db: Session, contrato: Contrato) -> PagoResumen:
        total_pagos = db.query(
            func.coalesce(func.sum(Pago.monto), 0)
        ).filter(Pago.contrato_id == contrato.id).scalar()

        total_pagado = contrato.adelanto + total_pagos
        saldo = max(contrato.monto_total - total_pagado, 0)

        # actualizar estado del contrato según saldo
        if saldo == 0:
            contrato.estado = "completo"
        elif total_pagado == 0:
            contrato.estado = "pendiente"
        else:
            contrato.estado = "parcial"

        contrato.saldo = saldo

        return PagoResumen(
            contrato_id=contrato.id,
            monto_total=contrato.monto_total,
            adelanto=contrato.adelanto,
            total_pagos=total_pagos,
            total_pagado=total_pagado,
            saldo=saldo,
            estado=contrato.estado,
        )

    @staticmethod
    def _recalcular_contrato(db: Session, contrato: Contrato) -> PagoResumen:
        resumen = PagoService._obtener_totales(db, contrato)
        db.commit()
        db.refresh(contrato)
        return resumen

    # --------- CRUD PAGOS ---------

    @staticmethod
    def crear_pago(data: PagoCreate, db: Session):
        contrato = db.query(Contrato).filter(Contrato.id == data.contrato_id).first()
        if not contrato:
            raise ValueError("Contrato no encontrado")

        if data.monto <= 0:
            raise ValueError("El monto del pago debe ser mayor que 0")

        # calcular saldo actual antes del pago
        resumen_actual = PagoService._obtener_totales(db, contrato)
        if data.monto > resumen_actual.saldo:
            raise ValueError("El monto del pago excede el saldo pendiente")

        nuevo = Pago(
            contrato_id=data.contrato_id,
            fecha_pago=data.fecha_pago,
            monto=data.monto,
            metodo=data.metodo,
            observacion=data.observacion,
            # AQUI: Pasamos la url de la imagen a la BD
            comprobante_url=data.comprobante_url 
        )

        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)

        PagoService._recalcular_contrato(db, contrato)
        return nuevo

    @staticmethod
    def listar_pagos(db: Session):
        return db.query(Pago).all()

    @staticmethod
    def obtener_pago(id: int, db: Session):
        return db.query(Pago).filter(Pago.id == id).first()

    @staticmethod
    def listar_pagos_por_contrato(contrato_id: int, db: Session):
        return db.query(Pago).filter(Pago.contrato_id == contrato_id).all()

    @staticmethod
    def actualizar_pago(id: int, data: PagoUpdate, db: Session):
        pago = db.query(Pago).filter(Pago.id == id).first()
        if not pago:
            return None

        contrato = db.query(Contrato).filter(Contrato.id == pago.contrato_id).first()
        if not contrato:
            return None

        # aplicar cambios al pago
        for campo, valor in data.dict(exclude_unset=True).items():
            setattr(pago, campo, valor)

        if pago.monto <= 0:
            raise ValueError("El monto del pago debe ser mayor que 0")

        db.commit()
        db.refresh(pago)

        PagoService._recalcular_contrato(db, contrato)
        return pago

    @staticmethod
    def eliminar_pago(id: int, db: Session):
        pago = db.query(Pago).filter(Pago.id == id).first()
        if not pago:
            return None

        contrato = db.query(Contrato).filter(Contrato.id == pago.contrato_id).first()
        if not contrato:
            return None

        db.delete(pago)
        db.commit()

        PagoService._recalcular_contrato(db, contrato)
        return True

    @staticmethod
    def resumen_contrato(contrato_id: int, db: Session) -> PagoResumen | None:
        contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
        if not contrato:
            return None
        resumen = PagoService._obtener_totales(db, contrato)
        return resumen