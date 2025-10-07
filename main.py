#!/usr/bin/env python3
"""
Script principal para ejecutar el MinSalud Web Scraper

Uso:
    python main.py                    # Ejecutar pipeline completo
    python main.py --only-crawl       # Solo extraer links
    python main.py --only-download    # Solo descargar PDFs
    python main.py --only-text        # Solo extraer texto
    python main.py --only-mongo       # Solo cargar a MongoDB
    python main.py --help             # Mostrar ayuda
"""

import sys
import argparse
from pathlib import Path

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

from scraper import MinSaludScraper

def main():
    parser = argparse.ArgumentParser(
        description="MinSalud Web Scraper - Extrae documentos del sitio de normatividad",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--only-crawl", 
        action="store_true", 
        help="Solo ejecutar crawling y extraer links"
    )
    parser.add_argument(
        "--only-download", 
        action="store_true", 
        help="Solo descargar PDFs (requiere archivo Links_MinSalud.json)"
    )
    parser.add_argument(
        "--only-text", 
        action="store_true", 
        help="Solo extraer texto de PDFs existentes"
    )
    parser.add_argument(
        "--only-mongo", 
        action="store_true", 
        help="Solo cargar archivos JSON existentes a MongoDB"
    )
    parser.add_argument(
        "--config-check", 
        action="store_true", 
        help="Verificar configuración y dependencias"
    )
    parser.add_argument(
        "--test-mongo", 
        action="store_true", 
        help="Probar conexión a MongoDB"
    )
    
    args = parser.parse_args()
    
    # Crear instancia del scraper
    scraper = MinSaludScraper()
    
    try:
        if args.config_check:
            verificar_configuracion(scraper)
        elif args.test_mongo:
            print("🧪 Probando conexión a MongoDB...")
            scraper.verificar_conexion_mongodb()
        elif args.only_crawl:
            print("🕷️  Ejecutando solo crawling...")
            scraper.crawl_sitio_web()
        elif args.only_download:
            print("📥 Ejecutando solo descarga de PDFs...")
            # Cargar links desde JSON existente
            scraper.cargar_links_desde_json()
            scraper.descargar_pdfs_paralelo()
        elif args.only_text:
            print("📝 Ejecutando solo extracción de texto...")
            scraper.procesar_pdfs_texto()
        elif args.only_mongo:
            print("🗄️  Ejecutando solo carga a MongoDB...")
            scraper.cargar_a_mongodb()
        else:
            # Pipeline completo
            print("🚀 Ejecutando pipeline completo...")
            scraper.ejecutar_pipeline_completo()
            
    except KeyboardInterrupt:
        print("\n❌ Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error crítico: {e}")
        sys.exit(1)

def verificar_configuracion(scraper):
    """Verificar que la configuración y dependencias están correctas"""
    print("🔍 VERIFICACIÓN DE CONFIGURACIÓN")
    print("="*50)
    
    # Verificar directorios
    from config import ensure_directories
    ensure_directories()
    print("✅ Directorios creados/verificados")
    
    # Verificar dependencias
    dependencias = {
        "requests": True,
        "beautifulsoup4": True,
        "lxml": True,
    }
    
    try:
        import pdfminer
        dependencias["pdfminer.six"] = True
    except ImportError:
        dependencias["pdfminer.six"] = False
    
    try:
        import pytesseract
        import pdf2image
        dependencias["OCR (pytesseract + pdf2image)"] = True
    except ImportError:
        dependencias["OCR (pytesseract + pdf2image)"] = False
    
    try:
        import pymongo
        dependencias["pymongo"] = True
    except ImportError:
        dependencias["pymongo"] = False
    
    print("\n📦 DEPENDENCIAS:")
    for dep, disponible in dependencias.items():
        estado = "✅" if disponible else "❌"
        print(f"  {estado} {dep}")
    
    # Verificar URLs
    print("\n🌐 VERIFICACIÓN DE CONECTIVIDAD:")
    try:
        from config import URL_INICIAL
        response = scraper.session.get(URL_INICIAL, timeout=10)
        if response.status_code == 200:
            print(f"✅ Sitio web MinSalud accesible: {URL_INICIAL}")
        else:
            print(f"⚠️  Sitio web responde con código: {response.status_code}")
    except Exception as e:
        print(f"❌ No se puede acceder al sitio web: {e}")
    
    print("\n✅ Verificación completada")

if __name__ == "__main__":
    main()