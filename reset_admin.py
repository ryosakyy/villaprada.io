import sys
import os

backend_path = os.path.join(os.getcwd(), 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from sqlalchemy import create_engine, text
from core.database import DATABASE_URL
from core.security import hash_password
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
is_local = any(local in DATABASE_URL.lower() for local in ["localhost", "127.0.0.1"])
ssl_args = {"ssl": ssl_context} if not is_local else {}

try:
    engine = create_engine(DATABASE_URL, connect_args=ssl_args)
    new_hash = hash_password("123456")

    with engine.connect() as conn:
        # Reset password for the main admin
        conn.execute(
            text("UPDATE usuarios SET password_hash = :h, estado = 1 WHERE email = 'admin@villa.com'"), 
            {"h": new_hash}
        )
        conn.commit()
        print("SUCCESS: Password for admin@villa.com reset to: 123456")
except Exception as e:
    print(f"ERROR: {e}")
