"""
Configuraciones centralizadas para el proyecto MinSalud Web Scraper
"""
import os
from pathlib import Path

# Intentar cargar variables de entorno desde .env
try:
    from decouple import config as env_config
    USE_ENV = True
except ImportError:
    USE_ENV = False
    print("⚠️  python-decouple no disponible. Usando configuración por defecto")

# Configuración de rutas
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
JSON_OUTPUT_DIR = DATA_DIR / "json_output"
LOGS_DIR = BASE_DIR / "logs"
LINKS_JSON_PATH = DATA_DIR / "Links_MinSalud.json"

# URLs del sitio web de MinSalud
URL_INICIAL = "https://www.minsalud.gov.co/Normativa/Paginas/normativa.aspx"
DOMINIO_BASE = "https://www.minsalud.gov.co/Normativa/"

# Configuración de MongoDB
if USE_ENV:
    MONGO_URI = env_config("MONGO_URI", default="mongodb://localhost:27017/")
    DB_NAME = env_config("MONGO_DB_NAME", default="minsalud_db")
    COLLECTION_NAME = env_config("MONGO_COLLECTION_NAME", default="normativa")
else:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("MONGO_DB_NAME", "minsalud_db")
    COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "normativa")

# Configuración de OCR
TESSERACT_LANG = "spa"  # Idioma español
OCR_CONFIG = "--oem 3 --psm 6"

# Configuración de solicitudes HTTP
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3
DELAY_BETWEEN_REQUESTS = 1  # segundos

# Configuración de procesamiento
CHUNK_SIZE = 8192  # Para descargas de archivos
MAX_WORKERS = 4  # Para procesamiento paralelo

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Extensiones de archivos soportadas
ALLOWED_EXTENSIONS = {
    'aspx': 'ASPX',
    'pdf': 'PDF'
}

# Crear directorios si no existen
def ensure_directories():
    """Crear todos los directorios necesarios"""
    directories = [DATA_DIR, PDF_DIR, JSON_OUTPUT_DIR, LOGS_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        
if __name__ == "__main__":
    ensure_directories()
    print("Directorios creados correctamente.")