# backend/routers/usuarios.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from core.database import get_db
from core.security import create_access_token, get_current_user
from schemas.usuarios import UsuarioCreate, UsuarioResponse, UsuarioUpdate, LoginRequest
from services.usuario_service import UsuarioService

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)

# ============================================================
# SOLO ADMIN PUEDE CREAR USUARIOS
# ============================================================
@router.post("/", response_model=UsuarioResponse)
def crear_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_user)
):
    if admin["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede crear usuarios")

    return UsuarioService.crear_usuario(db, data)


# ============================================================
# LISTAR USUARIOS (ADMIN)
# ============================================================
@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_user)
):
    if admin["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede listar usuarios")

    return UsuarioService.listar_usuarios(db)


# ============================================================
# OBTENER USUARIO
# ============================================================
@router.get("/{id}", response_model=UsuarioResponse)
def obtener_usuario(
    id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_user)
):
    if admin["rol"] != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")

    user = UsuarioService.obtener_por_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user


# ============================================================
# ACTUALIZAR USUARIO (ADMIN)
# ============================================================
@router.put("/{id}", response_model=UsuarioResponse)
def actualizar_usuario(
    id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_user)
):
    if admin["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede editar usuarios")

    return UsuarioService.actualizar_usuario(db, id, data)


# ============================================================
# ELIMINAR USUARIO (SOFT DELETE) — ADMIN
# ============================================================
@router.delete("/{id}")
def eliminar_usuario(
    id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_user)
):
    if admin["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede eliminar usuarios")

    return UsuarioService.eliminar_usuario(db, id)


# ============================================================
# LOGIN (JSON STANDARD)
# ============================================================
@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = UsuarioService.autenticar(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    # generar JWT
    # IMPORTANTE: El 'sub' DEBE SER EL ID PARA EL TOKEN
    token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "rol": user.rol
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": user.id,
            "nombres": user.nombres,
            "email": user.email,
            "rol": user.rol
        }
    }
