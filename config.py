import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Leer las variables de entorno
USER_PRIMARY = os.getenv("USER_PRIMARY")
PASS_PRIMARY = os.getenv("PASS_PRIMARY")
ACCOUNT_PRIMARY = os.getenv("ACCOUNT_PRIMARY")

# Usar las variables cargadas
print(f"User: {USER_PRIMARY}")
print(f"Account: {ACCOUNT_PRIMARY}")
