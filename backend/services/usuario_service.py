from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models.usuarios import Usuario
from schemas.usuarios import UsuarioCreate, UsuarioUpdate
from core.security import hash_password, verify_password

class UsuarioService:
    @staticmethod
    def crear_usuario(db: Session, data: UsuarioCreate):
        if db.query(Usuario).filter(Usuario.email == data.email).first():
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        nuevo = Usuario(
            nombres=data.nombres,
            email=data.email,
            password_hash=hash_password(data.password),
            rol=data.rol,
            estado=True
        )
        try:
            db.add(nuevo)
            db.commit()
            db.refresh(nuevo)
            return nuevo
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error de integridad")

    @staticmethod
    def listar_usuarios(db: Session):
        return db.query(Usuario).order_by(Usuario.id.desc()).all()

    @staticmethod
    def obtener_por_id(db: Session, id: int):
        return db.query(Usuario).filter(Usuario.id == id).first()

    @staticmethod
    def actualizar_usuario(db: Session, id: int, data: UsuarioUpdate):
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        datos_actualizar = data.dict(exclude_unset=True)
        if "password" in datos_actualizar and datos_actualizar["password"]:
            usuario.password_hash = hash_password(datos_actualizar["password"])
        
        for llave, valor in datos_actualizar.items():
            if llave != "password":
                setattr(usuario, llave, valor)

        try:
            db.commit()
            db.refresh(usuario)
            return usuario
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Email ya en uso")

    # === NUEVO: Lógica de Autenticación para corregir el Error 500 ===
    @staticmethod
    def autenticar(db: Session, email: str, password: str):
        usuario = db.query(Usuario).filter(Usuario.email == email).first()
        if not usuario or not verify_password(password, usuario.password_hash):
            return None
        return usuario

    # === NUEVO: Lógica de Borrado para evitar errores en el Router ===
    @staticmethod
    def eliminar_usuario(db: Session, id: int):
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        usuario.estado = False  # Soft delete
        db.commit()
        return {"message": "Usuario desactivado"}