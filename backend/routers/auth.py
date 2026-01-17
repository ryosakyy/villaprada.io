# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import create_access_token, get_current_user
from models.usuarios import Usuario
from schemas.usuarios import UsuarioCreate
from services.usuario_service import UsuarioService

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


# ============================================================
# CREAR ADMIN (por única vez o desde Swagger)
# ============================================================
@router.post("/crear_admin")
def crear_admin(data: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo = UsuarioService.crear_usuario(db, data)
    return {
        "mensaje": "Administrador creado correctamente",
        "usuario": nuevo
    }


# ============================================================
# LOGIN
#   Se llama así desde el front:
#   POST /auth/login?email=admin@villa.com&password=123456
# ============================================================
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    # Usamos la lógica centralizada
    usuario = UsuarioService.autenticar(db, email, password)

    if not usuario:
        from fastapi import status
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Incluimos info útil en el token
    token = create_access_token({
        "sub": str(usuario.id),
        "email": usuario.email,
        "rol": usuario.rol
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "nombres": usuario.nombres,
            "email": usuario.email,
            "rol": usuario.rol,
        }
    }


# ============================================================
# PERFIL (PROTEGIDO CON JWT)
# ============================================================
@router.get("/perfil")
def perfil(
    token_data: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user_id = token_data.get("sub")
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id": usuario.id,
        "nombres": usuario.nombres,
        "email": usuario.email,
        "rol": usuario.rol,
        "estado": usuario.estado,
        "fecha_creacion": usuario.fecha_creacion,
    }
