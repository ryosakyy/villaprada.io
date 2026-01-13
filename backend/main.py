from fastapi import FastAPI, Depends 
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine

# Routers
# <--- 1. AGREGADO "servicios" AQUÍ ABAJO
from routers import (
    auth, clientes, contratos, reservas, paquetes, pagos,
    egresos, disponibilidad, galeria, dashboard, reportes, usuarios,
    servicios 
)

# Importamos la función de seguridad para proteger las rutas
from routers.auth import get_current_user 

# =============================================================
# APP FASTAPI
# =============================================================
app = FastAPI(
    title="Sistema Villa Prada",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# =============================================================
# CURACIÓN DE BASE DE DATOS 2.0 (NUCLEAR OPTION)
# =============================================================
from sqlalchemy import text
import logging

def recreate_tables_preserving_data():
    """
    Estrategia para TiDB Cloud:
    1. Respalda los datos en memoria.
    2. Elimina las tablas (DROP).
    3. Recrea las tablas con SQLAlchemy (create_all) para tener AUTO_INCREMENT.
    4. Restaura los datos.
    """
    from core.database import SessionLocal
    db = SessionLocal()
    
    # Orden para borrado (evitar FK constraints issues aunque lo desactivaremos)
    tables = [
        "egresos", "pagos", "galeria", "reservas", "disponibilidad", # Hijos
        "contratos", # Intermedio
        "clientes", "paquetes", "servicios", "usuarios" # Padres
    ]
    
    backup_data = {}
    
    print("\n--- ☢️ INICIANDO REPARACIÓN PROFUNDA DE BASE DE DATOS ☢️ ---")
    
    try:
        # 1. RESPALDO DE DATOS
        print("📥 Respaldando datos...")
        for table in tables:
            try:
                result = db.execute(text(f"SELECT * FROM `{table}`"))
                # Convertimos filas a dicts
                rows = [dict(row._mapping) for row in result]
                backup_data[table] = rows
                print(f"   - {table}: {len(rows)} registros respaldados.")
            except Exception as e:
                print(f"   ⚠️ No se pudo leer {table} (quizás no existe): {e}")
                backup_data[table] = []

        # 2. DROPEAR TABLAS
        print("🔥 Eliminando tablas defectuosas...")
        db.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        for table in tables:
            try:
                db.execute(text(f"DROP TABLE IF EXISTS `{table}`;"))
                print(f"   - {table} eliminada.")
            except Exception as e:
                print(f"   ❌ Error eliminando {table}: {e}")
        db.execute(text("SET FOREIGN_KEY_CHECKS=1;"))

        # 3. RECREAR TABLAS
        print("🏗️ Reconstruyendo esquema correcto...")
        Base.metadata.create_all(bind=engine)
        print("   ✅ Tablas creadas con AUTO_INCREMENT.")

        # 4. RESTAURAR DATOS
        print("📤 Restaurando datos...")
        db.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
        for table in reversed(tables): # Orden inverso para insertar (Padres primero)
            rows = backup_data.get(table, [])
            if not rows:
                continue
                
            print(f"   Restaurando {table} ({len(rows)} registros)...")
            for row in rows:
                # Construir INSERT dinámico
                keys = list(row.keys())
                # Manejar valores DATE/DATETIME que ya son objetos Python gracias a SQLAlchemy
                placeholders = [f":{k}" for k in keys]
                sql = f"INSERT INTO `{table}` ({', '.join(keys)}) VALUES ({', '.join(placeholders)})"
                
                try:
                    db.execute(text(sql), row)
                except Exception as insert_err:
                    print(f"   ⚠️ Error insertando fila en {table}: {insert_err}")
                    
        db.execute(text("SET FOREIGN_KEY_CHECKS=1;"))
        db.commit()
        print("--- ✅ REPARACIÓN COMPLETADA CON ÉXITO ---")

    except Exception as critical_e:
        print(f"❌❌ ERROR CRÍTICO DURANTE LA MIGRACIÓN: {critical_e}")
        db.rollback()
    finally:
        db.close()

# =============================================================
# =============================================================
# CORS (Configuración Universal para Vercel/Producción)
# =============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Exception handler global que incluye CORS headers manualmente para evitar "Unknown Error"
from fastapi.responses import JSONResponse
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    import traceback
    print(f"❌ ERROR GLOBAL: {str(exc)}")
    traceback.print_exc()
    
    response = JSONResponse(
        status_code=500,
        content={"detail": f"Error interno: {str(exc)}"}
    )
    # Forzar headers CORS en la respuesta de error
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# =============================================================
# REGISTRO DE ROUTERS
# =============================================================
app.include_router(auth.router)
app.include_router(clientes.router)

# 🔒 Contratos requiere seguridad
app.include_router(
    contratos.router, 
    dependencies=[Depends(get_current_user)]
)

app.include_router(reservas.router)
app.include_router(paquetes.router)
app.include_router(pagos.router)
app.include_router(egresos.router)
app.include_router(disponibilidad.router)
app.include_router(galeria.router)
app.include_router(dashboard.router)
app.include_router(reportes.router)
app.include_router(usuarios.router)

# <--- 2. AGREGADO EL ROUTER DE SERVICIOS
app.include_router(servicios.router) 

@app.on_event("startup")
async def startup_event():
    # 1. Ejecutar reparación profunda de base de datos
    # Comentar esta línea después del primer despliegue exitoso si se desea optimizar el arranque
    try:
        recreate_tables_preserving_data()
    except Exception as e:
        print(f"❌ Error crítico en migración: {e}")

    # 2. Log de rutas para depuración
    print("\n--- RUTAS REGISTRADAS ---")
    for route in app.routes:
        if hasattr(route, "path"):
            print(f"Ruta: {route.path} | Nombre: {route.name}")
    print("-------------------------\n")

@app.get("/")
def root():
    return {"message": "API Villa Prada Funcionando 🚀"}