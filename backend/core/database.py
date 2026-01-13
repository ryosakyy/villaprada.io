# backend/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings
import os

# ---------- URL de conexión MySQL ----------
# Priorizar DATABASE_URL de variables de entorno (para producción: Render, etc.)
# Si no existe, construir desde settings individuales (para desarrollo local)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@{settings.DB_HOST}/"
    f"{settings.DB_NAME}"
)

# ---------- Configuración SSL ----------
import ssl
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Determinar si necesitamos SSL (Si no es localhost/127.0.0.1, asumimos nube como TiDB)
# Buscamos si el host contiene 'localhost' o '127.0.0.1'
is_local = any(local in DATABASE_URL.lower() for local in ["localhost", "127.0.0.1"])
ssl_args = {"ssl": ssl_context} if not is_local else {}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # Verifica salud de la conexión
    pool_recycle=300,     # Recicla conexiones cada 5 minutos
    connect_args=ssl_args
)

# ---------- ORM Base ----------
# De aquí heredarán TODOS tus modelos (Usuarios, Clientes, Contratos, etc.)
Base = declarative_base()

# ---------- SessionLocal para usar en los endpoints ----------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependencia para FastAPI (inyectar la sesión en los endpoints)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Función opcional para probar la conexión
def test_connection():
    try:
        with engine.connect() as conn:
            print("✅ Conexión correcta a MySQL (XAMPP) ->", settings.DB_NAME)
    except Exception as e:
        print("❌ Error de conexión a la base de datos:", e)
