"""
MinSalud Web Scraper - Script completo
Extrae hipervínculos, descarga PDFs, extrae texto y carga a MongoDB
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
import logging
from datetime import datetime
from urllib.parse import urljoin
from pathlib import Path
import concurrent.futures
from io import StringIO
import traceback

# Importaciones para extracción de texto PDF
try:
    from pdfminer.high_level import extract_text_to_fp
    from pdfminer.layout import LAParams
    PDF_MINER_AVAILABLE = True
except ImportError:
    print("⚠️  PDFMiner no disponible. Solo se usará OCR para PDFs.")
    PDF_MINER_AVAILABLE = False

# Importaciones para OCR
try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    print("⚠️  OCR no disponible. Instalar: pip install pytesseract pdf2image Pillow")
    OCR_AVAILABLE = False

# Importaciones para MongoDB
try:
    from pymongo import MongoClient
    MONGO_AVAILABLE = True
except ImportError:
    print("⚠️  PyMongo no disponible. Instalar: pip install pymongo")
    MONGO_AVAILABLE = False

from config import *

# Importar módulo de ética y cumplimiento
try:
    import sys
    sys.path.append(str(Path(__file__).parent.parent))
    from ethical_compliance import ethical_validator, require_ethical_approval
    ETHICAL_MODULE_AVAILABLE = True
except ImportError:
    print("⚠️ Módulo de ética no disponible")
    ETHICAL_MODULE_AVAILABLE = False
    ethical_validator = None

class MinSaludScraper:
    def __init__(self):
        self.setup_logging()
        
        # Inicializar validador ético
        if ETHICAL_MODULE_AVAILABLE:
            self.ethical_validator = ethical_validator
            logging.info("🛡️ Módulo de ética y cumplimiento legal activado")
        else:
            self.ethical_validator = None
            logging.warning("⚠️ Scraper ejecutándose SIN validación ética")
        self.setup_directories()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.links_visitados = set()
        self.todos_los_links = []
        self.estadisticas = {
            'paginas_procesadas': 0,
            'pdfs_descargados': 0,
            'textos_extraidos': 0,
            'documentos_mongo': 0,
            'errores': []
        }
    
    def setup_logging(self):
        """Configurar sistema de logging"""
        ensure_directories()
        log_file = LOGS_DIR / f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format=LOG_FORMAT,
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_directories(self):
        """Crear directorios necesarios"""
        ensure_directories()
        self.logger.info("✅ Directorios configurados correctamente")
    
    def extraer_hipervinculos(self, url):
        """Extraer todos los hipervínculos de una página"""
        links = []
        
        try:
            # 🛡️ VALIDACIONES ÉTICAS
            if self.ethical_validator:
                # Validar dominio permitido
                self.ethical_validator.validate_domain(url)
                
                # Verificar robots.txt
                if not self.ethical_validator.check_robots_txt(url):
                    self.logger.warning(f"⚠️ robots.txt no permite acceso a: {url}")
                    return []
                
                # Aplicar límite de tasa
                self.ethical_validator.rate_limit()
                
                # Registrar actividad
                self.ethical_validator.log_scraping_activity(url, 'extraer_links', 'iniciado')
            
            self.logger.info(f"🔍 Extrayendo links de: {url}")
            
            # Usar cabeceras éticas si está disponible
            headers = self.ethical_validator.get_ethical_headers() if self.ethical_validator else {}
            response = self.session.get(url, timeout=REQUEST_TIMEOUT, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Buscar contenedor con diferentes posibles clases
            container_div = None
            clases_posibles = ['container_blanco', 'contenido', 'content', 'main-content']
            
            for clase in clases_posibles:
                container_div = soup.find('div', class_=clase)
                if container_div:
                    self.logger.info(f"📦 Usando contenedor: '{clase}'")
                    break
            
            # Si no se encuentra contenedor específico, usar body completo
            if not container_div:
                self.logger.warning("⚠️  No se encontró contenedor específico, usando body completo")
                container_div = soup.find('body')
            
            if container_div:
                for link in container_div.find_all('a', href=True):
                    href = link.get('href')
                    if href:
                        full_url = urljoin(url, href)
                        
                        # Validar dominio
                        if full_url.startswith(DOMINIO_BASE):
                            if full_url.endswith('.aspx'):
                                links.append({'url': full_url, 'type': 'ASPX'})
                            elif full_url.endswith('.pdf'):
                                links.append({'url': full_url, 'type': 'PDF'})
            
            self.logger.info(f"✅ Encontrados {len(links)} links válidos")
            return links
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error accediendo a {url}: {e}"
            self.logger.error(error_msg)
            self.estadisticas['errores'].append(error_msg)
            return []
        except Exception as e:
            error_msg = f"Error inesperado en {url}: {e}"
            self.logger.error(error_msg)
            self.estadisticas['errores'].append(error_msg)
            return []
    
    def crawl_sitio_web(self, max_paginas=None):
        """Recorrer todo el sitio web y extraer links
        
        Args:
            max_paginas (int, optional): Límite de páginas a procesar (para pruebas)
        """
        self.logger.info("🕷️  Iniciando crawling del sitio web...")
        if max_paginas:
            self.logger.info(f"⚡ Modo prueba: máximo {max_paginas} páginas")
        
        links_a_visitar = [{'url': URL_INICIAL, 'type': 'ASPX'}]
        
        while links_a_visitar:
            # Verificar límite de páginas si está definido
            if max_paginas and len(self.links_visitados) >= max_paginas:
                self.logger.info(f"⚡ Límite de {max_paginas} páginas alcanzado")
                break
            
            pagina_actual = links_a_visitar.pop(0)
            url_actual = pagina_actual['url']
            
            if url_actual not in self.links_visitados and pagina_actual['type'] == 'ASPX':
                self.links_visitados.add(url_actual)
                self.estadisticas['paginas_procesadas'] += 1
                
                nuevos_links = self.extraer_hipervinculos(url_actual)
                
                for link in nuevos_links:
                    if link['url'] not in self.links_visitados:
                        # Evitar duplicados en todos_los_links
                        if not any(l['url'] == link['url'] for l in self.todos_los_links):
                            self.todos_los_links.append(link)
                        
                        # Si es ASPX, agregar a la cola
                        if link['type'] == 'ASPX':
                            links_a_visitar.append(link)
                
                # Delay entre requests
                time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Guardar JSON con todos los links
        self.guardar_links_json()
        
        self.logger.info(f"✅ Crawling completado. {len(self.todos_los_links)} links encontrados")
    
    def guardar_links_json(self):
        """Guardar lista de links en archivo JSON"""
        json_data = {
            'timestamp': datetime.now().isoformat(),
            'total_links': len(self.todos_los_links),
            'links': self.todos_los_links
        }
        
        with open(LINKS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"💾 Archivo JSON guardado: {LINKS_JSON_PATH}")
    
    def cargar_links_desde_json(self):
        """Cargar links desde archivo JSON existente"""
        try:
            if not Path(LINKS_JSON_PATH).exists():
                raise FileNotFoundError(f"No se encontró el archivo {LINKS_JSON_PATH}")
            
            with open(LINKS_JSON_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.todos_los_links = data.get('links', [])
            self.logger.info(f"📂 Cargados {len(self.todos_los_links)} links desde JSON")
            
        except Exception as e:
            error_msg = f"Error cargando links desde JSON: {e}"
            self.logger.error(error_msg)
            raise
    
    def descargar_pdf(self, pdf_url):
        """Descargar un archivo PDF individual"""
        try:
            file_name = os.path.basename(pdf_url)
            if not file_name.endswith('.pdf'):
                file_name += '.pdf'
            
            file_path = PDF_DIR / file_name
            
            # Verificar si ya existe
            if file_path.exists():
                self.logger.info(f"⏭️  PDF ya existe: {file_name}")
                return str(file_path)
            
            response = self.session.get(pdf_url, stream=True, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            with open(file_path, 'wb') as pdf_file:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        pdf_file.write(chunk)
            
            self.estadisticas['pdfs_descargados'] += 1
            self.logger.info(f"📥 PDF descargado: {file_name}")
            return str(file_path)
            
        except Exception as e:
            error_msg = f"Error descargando PDF {pdf_url}: {e}"
            self.logger.error(error_msg)
            self.estadisticas['errores'].append(error_msg)
            return None
    
    def descargar_pdfs_paralelo(self):
        """Descargar todos los PDFs en paralelo"""
        pdf_links = [link['url'] for link in self.todos_los_links if link['type'] == 'PDF']
        
        if not pdf_links:
            self.logger.info("📄 No hay PDFs para descargar")
            return []
        
        self.logger.info(f"📥 Descargando {len(pdf_links)} PDFs...")
        
        archivos_descargados = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_url = {executor.submit(self.descargar_pdf, url): url for url in pdf_links}
            
            for future in concurrent.futures.as_completed(future_to_url):
                resultado = future.result()
                if resultado:
                    archivos_descargados.append(resultado)
        
        self.logger.info(f"✅ {len(archivos_descargados)} PDFs descargados exitosamente")
        return archivos_descargados
    
    def extraer_texto_pdf_normal(self, pdf_path):
        """Extraer texto usando PDFMiner"""
        if not PDF_MINER_AVAILABLE:
            return None
        
        try:
            output_string = StringIO()
            with open(pdf_path, 'rb') as file:
                extract_text_to_fp(file, output_string, laparams=LAParams())
            
            texto = output_string.getvalue().strip()
            return texto if len(texto) > 50 else None  # Mínimo 50 caracteres
            
        except Exception as e:
            self.logger.warning(f"PDFMiner falló en {pdf_path}: {e}")
            return None
    
    def extraer_texto_pdf_ocr(self, pdf_path):
        """Extraer texto usando OCR"""
        if not OCR_AVAILABLE:
            return None
        
        try:
            images = convert_from_path(pdf_path)
            texto_completo = []
            
            for i, imagen in enumerate(images):
                texto_pagina = pytesseract.image_to_string(
                    imagen, 
                    lang=TESSERACT_LANG,
                    config=OCR_CONFIG
                )
                if texto_pagina.strip():
                    texto_completo.append(f"--- Página {i+1} ---\n{texto_pagina}")
            
            texto_final = "\n\n".join(texto_completo)
            return texto_final if len(texto_final.strip()) > 50 else None
            
        except Exception as e:
            self.logger.warning(f"OCR falló en {pdf_path}: {e}")
            return None
    
    def extraer_texto_pdf(self, pdf_path):
        """Extraer texto de PDF usando el mejor método disponible"""
        archivo_nombre = os.path.basename(pdf_path)
        
        # Intentar primero PDFMiner (más rápido y preciso)
        texto = self.extraer_texto_pdf_normal(pdf_path)
        if texto:
            return texto, 'PDFMINER'
        
        # Si falla, intentar OCR
        texto = self.extraer_texto_pdf_ocr(pdf_path)
        if texto:
            return texto, 'OCR'
        
        # Si ambos fallan
        self.logger.warning(f"❌ No se pudo extraer texto de: {archivo_nombre}")
        return None, 'FALLIDO'
    
    def procesar_pdfs_texto(self):
        """Procesar todos los PDFs y extraer texto"""
        pdf_files = list(PDF_DIR.glob("*.pdf"))
        
        if not pdf_files:
            self.logger.info("📄 No hay archivos PDF para procesar")
            return
        
        self.logger.info(f"📝 Procesando texto de {len(pdf_files)} PDFs...")
        
        for i, pdf_path in enumerate(pdf_files, 1):
            try:
                self.logger.info(f"📖 Procesando {i}/{len(pdf_files)}: {pdf_path.name}")
                
                texto, metodo = self.extraer_texto_pdf(pdf_path)
                
                if texto:
                    # Crear JSON individual
                    json_data = {
                        'file': pdf_path.name,
                        'timestamp': datetime.now().isoformat(),
                        'text': texto,
                        'method': metodo,
                        'size_bytes': pdf_path.stat().st_size,
                        'char_count': len(texto)
                    }
                    
                    # Guardar JSON
                    json_filename = f"minsalud_texto_{i:03d}.json"
                    json_path = JSON_OUTPUT_DIR / json_filename
                    
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, indent=2, ensure_ascii=False)
                    
                    self.estadisticas['textos_extraidos'] += 1
                    self.logger.info(f"✅ Texto extraído y guardado: {json_filename}")
                    
                else:
                    error_msg = f"No se pudo extraer texto de: {pdf_path.name}"
                    self.estadisticas['errores'].append(error_msg)
                
            except Exception as e:
                error_msg = f"Error procesando {pdf_path.name}: {e}"
                self.logger.error(error_msg)
                self.estadisticas['errores'].append(error_msg)
    
    def cargar_a_mongodb(self, batch_size=100, crear_indices=True):
        """
        Cargar datos extraídos a MongoDB Atlas con optimizaciones
        
        Args:
            batch_size (int): Número de documentos a insertar por lote
            crear_indices (bool): Crear índices en la colección
        """
        if not MONGO_AVAILABLE:
            self.logger.warning("⚠️  PyMongo no disponible. Saltando carga a MongoDB")
            return
        
        try:
            # Conectar a MongoDB con timeout
            self.logger.info(f"🔌 Conectando a MongoDB...")
            client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000,  # 5 segundos timeout
                connectTimeoutMS=10000  # 10 segundos timeout
            )
            
            # Verificar conexión
            client.admin.command('ping')
            self.logger.info("✅ Conexión a MongoDB exitosa")
            
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]
            
            self.logger.info(f"🗄️  Base de datos: {DB_NAME}")
            self.logger.info(f"📁 Colección: {COLLECTION_NAME}")
            
            # Crear índices para mejorar rendimiento
            if crear_indices:
                self._crear_indices_mongodb(collection)
            
            # Obtener archivos JSON
            json_files = list(JSON_OUTPUT_DIR.glob("minsalud_texto_*.json"))
            
            if not json_files:
                self.logger.warning("📄 No hay archivos JSON para cargar")
                return
            
            self.logger.info(f"📊 {len(json_files)} archivos JSON encontrados")
            
            documentos_cargados = 0
            documentos_actualizados = 0
            documentos_duplicados = 0
            batch = []
            
            for i, json_file in enumerate(json_files, 1):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Agregar metadata adicional
                    data['_uploaded_at'] = datetime.now().isoformat()
                    data['_source_file'] = str(json_file.name)
                    
                    # Verificar si ya existe (por nombre de archivo)
                    existente = collection.find_one({'file': data['file']})
                    
                    if existente:
                        # Actualizar si el texto es diferente
                        if existente.get('text') != data.get('text'):
                            collection.update_one(
                                {'_id': existente['_id']},
                                {'$set': data}
                            )
                            documentos_actualizados += 1
                            self.logger.info(f"🔄 Actualizado: {data['file']}")
                        else:
                            documentos_duplicados += 1
                            self.logger.debug(f"⏭️  Ya existe: {data['file']}")
                    else:
                        # Agregar al batch para inserción
                        batch.append(data)
                        
                        # Insertar cuando el batch esté lleno
                        if len(batch) >= batch_size:
                            result = collection.insert_many(batch)
                            documentos_cargados += len(result.inserted_ids)
                            self.logger.info(f"💾 Batch insertado: {len(result.inserted_ids)} documentos")
                            batch = []
                    
                    # Mostrar progreso
                    if i % 10 == 0:
                        self.logger.info(f"📈 Progreso: {i}/{len(json_files)} archivos procesados")
                    
                except json.JSONDecodeError as e:
                    error_msg = f"Error JSON en {json_file.name}: {e}"
                    self.logger.error(error_msg)
                    self.estadisticas['errores'].append(error_msg)
                except Exception as e:
                    error_msg = f"Error procesando {json_file.name}: {e}"
                    self.logger.error(error_msg)
                    self.estadisticas['errores'].append(error_msg)
            
            # Insertar documentos restantes del batch
            if batch:
                result = collection.insert_many(batch)
                documentos_cargados += len(result.inserted_ids)
                self.logger.info(f"💾 Batch final insertado: {len(result.inserted_ids)} documentos")
            
            # Guardar estadísticas
            self.estadisticas['documentos_mongo'] = documentos_cargados
            
            # Resumen final
            print("\n" + "="*60)
            print("📊 RESUMEN DE CARGA A MONGODB")
            print("="*60)
            print(f"✅ Nuevos documentos insertados: {documentos_cargados}")
            print(f"🔄 Documentos actualizados: {documentos_actualizados}")
            print(f"⏭️  Documentos duplicados (sin cambios): {documentos_duplicados}")
            print(f"📁 Total en colección: {collection.count_documents({})}")
            print("="*60)
            
            self.logger.info(f"✅ Carga completada: {documentos_cargados} nuevos, {documentos_actualizados} actualizados")
            
            # Cerrar conexión
            client.close()
            
        except Exception as e:
            error_msg = f"Error en MongoDB: {e}"
            self.logger.error(error_msg)
            self.estadisticas['errores'].append(error_msg)
            
            # Mostrar ayuda si hay error de conexión
            if "connection" in str(e).lower() or "timeout" in str(e).lower():
                print("\n⚠️  ERROR DE CONEXIÓN A MONGODB")
                print("="*60)
                print("Posibles soluciones:")
                print("1. Verificar MONGO_URI en config.py o .env")
                print("2. Verificar que MongoDB está corriendo (local)")
                print("3. Verificar credenciales de MongoDB Atlas")
                print("4. Verificar conexión a internet")
                print("5. Verificar IP en whitelist (MongoDB Atlas)")
                print("="*60)
    
    def _crear_indices_mongodb(self, collection):
        """Crear índices en la colección de MongoDB"""
        try:
            # Índice en el campo 'file' (único)
            collection.create_index('file', unique=True)
            self.logger.info("📑 Índice creado en campo 'file'")
            
            # Índice en timestamp
            collection.create_index('timestamp')
            self.logger.info("📑 Índice creado en campo 'timestamp'")
            
            # Índice de texto para búsquedas
            collection.create_index([('text', 'text')])
            self.logger.info("📑 Índice de texto creado")
            
        except Exception as e:
            self.logger.warning(f"⚠️  Error creando índices: {e}")
    
    def verificar_conexion_mongodb(self):
        """Verificar conexión a MongoDB y mostrar información"""
        if not MONGO_AVAILABLE:
            print("❌ PyMongo no está instalado")
            return False
        
        try:
            print("\n🔍 VERIFICANDO CONEXIÓN A MONGODB")
            print("="*60)
            print(f"URI: {MONGO_URI[:50]}...")
            print(f"Base de datos: {DB_NAME}")
            print(f"Colección: {COLLECTION_NAME}")
            print("="*60)
            
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]
            
            count = collection.count_documents({})
            
            print(f"✅ Conexión exitosa")
            print(f"📊 Documentos en colección: {count}")
            
            if count > 0:
                print("\n📄 Documento de ejemplo:")
                doc = collection.find_one()
                print(f"  - Archivo: {doc.get('file', 'N/A')}")
                print(f"  - Método: {doc.get('method', 'N/A')}")
                print(f"  - Timestamp: {doc.get('timestamp', 'N/A')}")
                print(f"  - Texto (primeros 100 chars): {doc.get('text', '')[:100]}...")
            
            client.close()
            print("="*60)
            return True
            
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            print("\n💡 Sugerencias:")
            print("  - Verificar MONGO_URI en config.py")
            print("  - Para MongoDB Atlas: verificar usuario/password")
            print("  - Para MongoDB local: verificar que está corriendo")
            print("="*60)
            return False
    
    def mostrar_estadisticas(self):
        """Mostrar estadísticas finales del procesamiento"""
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS FINALES")
        print("="*60)
        print(f"🕷️  Páginas web procesadas: {self.estadisticas['paginas_procesadas']}")
        print(f"🔗 Total de links encontrados: {len(self.todos_los_links)}")
        print(f"📥 PDFs descargados: {self.estadisticas['pdfs_descargados']}")
        print(f"📝 Textos extraídos: {self.estadisticas['textos_extraidos']}")
        print(f"🗄️  Documentos en MongoDB: {self.estadisticas['documentos_mongo']}")
        print(f"❌ Errores encontrados: {len(self.estadisticas['errores'])}")
        
        if self.estadisticas['errores']:
            print("\n🚨 ERRORES:")
            for i, error in enumerate(self.estadisticas['errores'][:5], 1):
                print(f"  {i}. {error}")
            if len(self.estadisticas['errores']) > 5:
                print(f"  ... y {len(self.estadisticas['errores']) - 5} errores más")
        
        print("="*60)
    
    def ejecutar_pipeline_completo(self):
        """Ejecutar todo el pipeline de scraping"""
        inicio = time.time()
        
        try:
            print("🚀 INICIANDO PIPELINE DE WEB SCRAPING MINSALUD")
            print("="*60)
            
            # Paso 1: Crawling del sitio web
            self.crawl_sitio_web()
            
            # Paso 2: Descargar PDFs
            self.descargar_pdfs_paralelo()
            
            # Paso 3: Extraer texto de PDFs
            self.procesar_pdfs_texto()
            
            # Paso 4: Cargar a MongoDB
            self.cargar_a_mongodb()
            
            # Mostrar estadísticas
            duracion = time.time() - inicio
            print(f"\n⏱️  Pipeline completado en {duracion/60:.1f} minutos")
            
            self.mostrar_estadisticas()
            
        except KeyboardInterrupt:
            self.logger.info("❌ Pipeline interrumpido por el usuario")
            self.mostrar_estadisticas()
        except Exception as e:
            error_msg = f"Error crítico en pipeline: {e}"
            self.logger.error(error_msg)
            self.logger.error(traceback.format_exc())
            print(f"\n💥 {error_msg}")

if __name__ == "__main__":
    scraper = MinSaludScraper()
    scraper.ejecutar_pipeline_completo()