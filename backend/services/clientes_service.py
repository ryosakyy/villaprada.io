from sqlalchemy.orm import Session
from models.clientes import Cliente
from schemas.clientes import ClienteCreate, ClienteUpdate

class ClienteService:

    @staticmethod
    def crear_cliente(data: ClienteCreate, db: Session):
        from fastapi import HTTPException
        # Verificar duplicados por DNI
        existe_dni = db.query(Cliente).filter(Cliente.dni == data.dni).first()
        if existe_dni:
            raise HTTPException(status_code=400, detail=f"Ya existe un cliente con el DNI {data.dni}")
        
        # Verificar duplicados por Correo (si se proporciona)
        if data.correo:
            existe_correo = db.query(Cliente).filter(Cliente.correo == data.correo).first()
            if existe_correo:
                raise HTTPException(status_code=400, detail=f"Ya existe un cliente con el correo {data.correo}")

        nuevo = Cliente(
            dni=data.dni,
            nombre=data.nombre,
            telefono=data.telefono,
            correo=data.correo,
            direccion=data.direccion
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    @staticmethod
    def listar_clientes(db: Session):
        return db.query(Cliente).all()

    @staticmethod
    def obtener_cliente(id: int, db: Session):
        return db.query(Cliente).filter(Cliente.id == id).first()

    @staticmethod
    def actualizar_cliente(id: int, data: ClienteUpdate, db: Session):
        cliente = db.query(Cliente).filter(Cliente.id == id).first()
        if not cliente:
            return None

        for campo, valor in data.dict(exclude_unset=True).items():
            setattr(cliente, campo, valor)

        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def eliminar_cliente(id: int, db: Session):
        cliente = db.query(Cliente).filter(Cliente.id == id).first()
        if not cliente:
            return None

        # --- CASCADE DELETE MANUAL ---
        from models.contratos import Contrato
        from models.pagos import Pago
        from models.egresos import Egreso

        # 1. Obtener IDs de contratos asociados
        contratos = db.query(Contrato).filter(Contrato.cliente_id == id).all()
        contrato_ids = [c.id for c in contratos]

        if contrato_ids:
            # 2. Eliminar todos los PAGOS de esos contratos
            db.query(Pago).filter(Pago.contrato_id.in_(contrato_ids)).delete(synchronize_session=False)
            
            # 3. Eliminar todos los EGRESOS de esos contratos
            db.query(Egreso).filter(Egreso.contrato_id.in_(contrato_ids)).delete(synchronize_session=False)
            
            # 4. Eliminar los CONTRATOS
            db.query(Contrato).filter(Contrato.cliente_id == id).delete(synchronize_session=False)

        # 5. Finalmente eliminar al cliente
        db.delete(cliente)
        db.commit()
        return True
