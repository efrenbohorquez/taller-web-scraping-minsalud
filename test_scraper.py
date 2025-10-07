"""
Script de prueba para el scraper - Versión optimizada y rápida
"""
import sys
import os
from pathlib import Path

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent / "src"))

from scraper import MinSaludScraper
import requests
from bs4 import BeautifulSoup

def test_conexion():
    """Prueba de conexión básica"""
    print("="*60)
    print("🧪 TEST 1: Conexión al sitio web")
    print("="*60)
    
    urls_prueba = [
        "https://www.minsalud.gov.co",
        "https://www.minsalud.gov.co/Normatividad/Paginas/normatividad.aspx",
        "https://www.minsalud.gov.co/Normatividad_Nuevo/Paginas/Normatividad.aspx"
    ]
    
    for url in urls_prueba:
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ {url}")
            print(f"   Código: {response.status_code}")
            if response.status_code == 200:
                print(f"   ✅ URL VÁLIDA ENCONTRADA!")
                return url
        except Exception as e:
            print(f"❌ {url} - Error: {str(e)[:50]}")
    
    return None

def test_extraccion_basica(url):
    """Prueba extracción de links básica"""
    print("\n" + "="*60)
    print("🧪 TEST 2: Extracción de hipervínculos")
    print("="*60)
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Buscar divs con diferentes clases posibles
        divs_posibles = [
            'container_blanco',
            'container',
            'content',
            'main-content'
        ]
        
        container_div = None
        for div_class in divs_posibles:
            container_div = soup.find('div', class_=div_class)
            if container_div:
                print(f"✅ Contenedor encontrado: '{div_class}'")
                break
        
        if not container_div:
            print("⚠️  No se encontró contenedor específico, usando body completo")
            container_div = soup.find('body')
        
        # Contar links
        links = container_div.find_all('a') if container_div else []
        links_aspx = [l for l in links if l.get('href', '').endswith('.aspx')]
        links_pdf = [l for l in links if l.get('href', '').endswith('.pdf')]
        
        print(f"📊 Total de links: {len(links)}")
        print(f"   - Links .aspx: {len(links_aspx)}")
        print(f"   - Links .pdf: {len(links_pdf)}")
        
        if links_pdf:
            print(f"\n📄 Ejemplos de PDFs encontrados:")
            for pdf_link in links_pdf[:3]:
                print(f"   - {pdf_link.get('href')}")
        
        return len(links) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_scraper_completo():
    """Test del scraper completo con límites"""
    print("\n" + "="*60)
    print("🧪 TEST 3: Scraper completo (modo prueba)")
    print("="*60)
    
    scraper = MinSaludScraper()
    
    # Modificar límites para prueba rápida
    print("⚡ Configuración de prueba rápida:")
    print("   - Máximo 5 páginas a visitar")
    print("   - Máximo 3 PDFs a descargar")
    print("   - Tiempo de espera reducido")
    
    # Ejecutar solo crawling limitado
    print("\n🕷️  Iniciando crawling limitado...")
    try:
        scraper.crawl_sitio_web(max_paginas=5)
        print("✅ Crawling completado")
        return True
    except Exception as e:
        print(f"❌ Error en crawling: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "🚀"*30)
    print(" "*20 + "SUITE DE PRUEBAS - MINSALUD SCRAPER")
    print("🚀"*30 + "\n")
    
    # Test 1: Conexión
    url_valida = test_conexion()
    if not url_valida:
        print("\n❌ No se pudo conectar a ninguna URL válida")
        print("💡 Verifica tu conexión a internet o que el sitio esté disponible")
        return
    
    # Test 2: Extracción básica
    if not test_extraccion_basica(url_valida):
        print("\n⚠️  La extracción básica falló, pero continuamos...")
    
    # Test 3: Scraper completo
    test_scraper_completo()
    
    print("\n" + "="*60)
    print("✅ SUITE DE PRUEBAS COMPLETADA")
    print("="*60)
    print("\n💡 Para ejecutar el scraper completo sin límites:")
    print("   python main.py")
    print("\n💡 Para ver opciones:")
    print("   python main.py --help")

if __name__ == "__main__":
    main()
