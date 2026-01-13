import sys
import os

# Agregar el directorio ROOT y BACKEND
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)
sys.path.append(os.path.join(base_path, 'backend'))

from backend.core.database import SessionLocal
from backend.models.servicios import Servicio
from sqlalchemy import text

def debug_servicios():
    db = SessionLocal()
    try:
        print("--- CONECTANDO A LA BASE DE DATOS ---")
        # Verificar si la tabla existe
        result = db.execute(text("SHOW TABLES LIKE 'servicios'"))
        if not result.first():
            print("[ERROR] LA TABLA 'servicios' NO EXISTE EN LA BD.")
            return

        print("[OK] La tabla 'servicios' existe.")

        # Consultar datos
        servicios = db.query(Servicio).all()
        print(f"--- LISTANDO SERVICIOS (Total: {len(servicios)}) ---")
        for s in servicios:
            print(f"ID: {s.id} | Nombre: {s.nombre} | Precio: {s.precio} | Estado: {s.estado}")
        
        if len(servicios) == 0:
            print("[WARN] La tabla existe pero esta VACIA.")

    except Exception as e:
        print(f"[ERROR] CONSULTANDO BD: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_servicios()
