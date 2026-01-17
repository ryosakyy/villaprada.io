import sys
import os

# Asegurar que el path incluya la carpeta backend para importar core
backend_path = os.path.join(os.getcwd(), 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from sqlalchemy import create_engine, text
from core.database import DATABASE_URL
import ssl

print(f"DEBUG: Conectando a {DATABASE_URL.split('@')[-1]}") # Solo mostrar el host por seguridad

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
is_local = any(local in DATABASE_URL.lower() for local in ["localhost", "127.0.0.1"])
ssl_args = {"ssl": ssl_context} if not is_local else {}

try:
    engine = create_engine(DATABASE_URL, connect_args=ssl_args)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, email, nombres, rol, estado, password_hash FROM usuarios"))
        print("\n--- LISTA DE USUARIOS ---")
        for row in result:
            # En SQLAlchemy 2.0+, los resultados son Row objects que se acceden por atributo o mapeo
            r = row._mapping
            print(f"ID: {r['id']} | Email: {r['email']} | Nombres: {r['nombres']} | Rol: {r['rol']} | Estado: {r['estado']} | Hash Prefix: {r['password_hash'][:10]}...")
        print("-------------------------\n")
except Exception as e:
    print(f"❌ Error diagnosticando DB: {e}")
