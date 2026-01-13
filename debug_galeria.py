import sys
import os

# Ajustar path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from core.database import SessionLocal
from models.galeria import Galeria

db = SessionLocal()
try:
    total = db.query(Galeria).count()
    print(f"Total de registros en galeria: {total}")
    
    primeros = db.query(Galeria).limit(3).all()
    for g in primeros:
        print(f"ID: {g.id}, Titulo: {g.titulo}, URL: {g.imagen_url}")
finally:
    db.close()
