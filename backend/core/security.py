from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext

# ELIMINAMOS LA DEPENDENCIA DE SETTINGS PARA EVITAR ERRORES
# from core.config import settings 

# ---------- CONFIGURACIÓN FIJA (LA SOLUCIÓN) ----------
# Al poner esto fijo, el token NO muere si reinicias el servidor
SECRET_KEY = "clave_super_secreta_villa_prada_fija_123" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480 # 8 horas

# ---------- Configuración bcrypt ----------
import bcrypt

# Middleware de seguridad para rutas protegidas
from fastapi.security import HTTPBearer
oauth2_scheme = HTTPBearer()

# ================== CONTRASEÑAS ==================

def hash_password(password: str) -> str:
    """Encripta una contraseña usando bcrypt directamente."""
    # Bcrypt tiene un límite de 72 caracteres
    pwd_bytes = password[:72].encode('utf-8')
    # Generar salt y hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con su hash."""
    try:
        # Bcrypt requiere bytes
        pwd_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except Exception as e:
        print(f"❌ Error verificando password: {e}")
        return False


# ================== TOKENS JWT ==================

def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """
    Crea un token JWT con los datos enviados.
    """
    to_encode = data.copy()
    
    # Convierte 'sub' a string para evitar problemas de compatibilidad JWT
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.now() + timedelta(
        minutes=expires_delta if expires_delta else ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Valida un token JWT y retorna el payload si es válido."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ================== DEPENDENCIA PARA RUTAS PROTEGIDAS ==================

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    """
    Extrae el token del header Authorization: Bearer <token>
    y verifica su validez.
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        print(f"❌ TOKEN RECHAZADO: {token[:15]}...") # Log para ver en consola Python
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload