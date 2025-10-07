"""
Script de prueba rápida para verificar funcionalidad básica
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_basic_functionality():
    """Prueba básica de funcionalidad"""
    print("🧪 EJECUTANDO PRUEBAS BÁSICAS")
    print("="*40)
    
    # Test 1: Verificar imports
    try:
        from scraper import MinSaludScraper
        print("✅ Import del scraper exitoso")
    except ImportError as e:
        print(f"❌ Error importando scraper: {e}")
        return False
    
    # Test 2: Crear instancia
    try:
        scraper = MinSaludScraper()
        print("✅ Instancia del scraper creada")
    except Exception as e:
        print(f"❌ Error creando scraper: {e}")
        return False
    
    # Test 3: Verificar conectividad básica
    try:
        from config import URL_INICIAL
        response = scraper.session.get(URL_INICIAL, timeout=10)
        if response.status_code == 200:
            print("✅ Conectividad web exitosa")
        else:
            print(f"⚠️  Respuesta HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        return False
    
    # Test 4: Prueba de extracción de links (solo 1 página)
    try:
        links = scraper.extraer_hipervinculos(URL_INICIAL)
        print(f"✅ Extracción de links exitosa: {len(links)} links encontrados")
        
        # Mostrar algunos ejemplos
        if links:
            print("📄 Ejemplos de links encontrados:")
            for i, link in enumerate(links[:3]):
                print(f"  {i+1}. [{link['type']}] {link['url']}")
    except Exception as e:
        print(f"❌ Error extrayendo links: {e}")
        return False
    
    print("\n🎉 Todas las pruebas básicas pasaron exitosamente")
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)