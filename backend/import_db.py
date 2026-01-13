import os
import sys
from sqlalchemy import create_engine, text

def import_database():
    print("--- MIGRADOR DE BASE DE DATOS A LA NUBE ---")
    print("Este script te ayudará a subir tu archivo .sql a TiDB Cloud (o cualquier DB).")
    
    # 1. Obtener la URL de conexión
    db_url = input("\nPegar aquí tu CONNECTION STRING de TiDB \n(ej. mysql+pymysql://user:pass@host:4000/test):\n").strip()
    
    if not db_url:
        print("❌ Error: Necesitas la URL de conexión.")
        return

    # 2. Obtener el archivo SQL
    sql_file = input("\nArrastra tu archivo .sql aquí o escribe la ruta:\n").strip()
    
    # Limpiar comillas que Windows a veces agrega al arrastrar
    sql_file = sql_file.replace('"', '').replace("'", "")

    if not os.path.exists(sql_file):
        print(f"❌ Error: No encuentro el archivo {sql_file}")
        return

    print(f"\n🚀 Conectando a la nube... ({db_url.split('@')[1] if '@' in db_url else '...'})")
    
    try:
        # Crear motor de conexión
        # Aseguramos que use pymysql
        if db_url.startswith("mysql://"):
            db_url = db_url.replace("mysql://", "mysql+pymysql://")
        
        engine = create_engine(db_url, echo=False)
        
        with engine.connect() as connection:
            print("✅ Conexión exitosa. Leyendo archivo SQL...")
            
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()

            # Separar comandos (una aproximación simple por punto y coma)
            # Nota: Esto puede fallar con stored procedures complejos, pero sirve para dumps simples
            # Para mayor robustez en el futuro, se puede usar toolings específicos, pero esto suele bastar.
            statements = sql_content.split(';')
            
            total = len(statements)
            print(f"📦 Encontradas {total} sentencias SQL. Ejecutando...")

            for i, statement in enumerate(statements):
                stmt = statement.strip()
                if stmt:
                    try:
                        connection.execute(text(stmt))
                        print(f"\rProgreso: {i+1}/{total}", end="")
                    except Exception as e:
                        print(f"\n⚠️ Advertencia en sentencia {i+1}: {e}")
                        # No detenemos el script, a veces fallan drops si no existe tabla
            
            connection.commit()
            print("\n\n✨ ¡LISTO! Tu base de datos ha sido migrada a la nube exitosamente.")

    except Exception as e:
        print(f"\n❌ Ocurrió un error fatal: {e}")

if __name__ == "__main__":
    import_database()
