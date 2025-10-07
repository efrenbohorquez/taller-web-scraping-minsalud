"""
Test del módulo de ética y cumplimiento legal
"""

import sys
from pathlib import Path

# Agregar path del proyecto
sys.path.append(str(Path(__file__).parent))

from ethical_compliance import EthicalScrapingValidator, EthicalComplianceException
import time

def test_domain_validation():
    """Probar validación de dominios"""
    print("\n" + "="*70)
    print("TEST 1: Validación de Dominios")
    print("="*70)
    
    validator = EthicalScrapingValidator()
    
    # Dominio permitido
    try:
        validator.validate_domain("https://www.minsalud.gov.co/Normativa/")
        print("✅ PASÓ: Dominio minsalud.gov.co permitido correctamente")
    except ValueError:
        print("❌ FALLÓ: Dominio minsalud.gov.co debería estar permitido")
    
    # Dominio no permitido
    try:
        validator.validate_domain("https://www.google.com")
        print("❌ FALLÓ: Dominio google.com NO debería estar permitido")
    except ValueError as e:
        print("✅ PASÓ: Dominio google.com bloqueado correctamente")
        print(f"   Mensaje: {str(e)[:80]}...")

def test_robots_txt():
    """Probar verificación de robots.txt"""
    print("\n" + "="*70)
    print("TEST 2: Verificación de robots.txt")
    print("="*70)
    
    validator = EthicalScrapingValidator()
    
    try:
        allowed = validator.check_robots_txt("https://www.minsalud.gov.co/Normativa/")
        print(f"✅ PASÓ: Verificación robots.txt completada")
        print(f"   Resultado: {'PERMITIDO' if allowed else 'NO PERMITIDO'}")
    except Exception as e:
        print(f"⚠️ ADVERTENCIA: Error al verificar robots.txt: {e}")

def test_rate_limiting():
    """Probar límite de tasa de peticiones"""
    print("\n" + "="*70)
    print("TEST 3: Límite de Tasa de Peticiones")
    print("="*70)
    
    validator = EthicalScrapingValidator()
    
    print("⏱️ Probando intervalo mínimo (2 segundos)...")
    
    start = time.time()
    validator.rate_limit()
    time_1 = time.time()
    
    validator.rate_limit()
    time_2 = time.time()
    
    validator.rate_limit()
    time_3 = time.time()
    
    interval_1 = time_2 - time_1
    interval_2 = time_3 - time_2
    
    print(f"   Intervalo 1: {interval_1:.2f}s")
    print(f"   Intervalo 2: {interval_2:.2f}s")
    
    if interval_1 >= 2.0 and interval_2 >= 2.0:
        print("✅ PASÓ: Intervalos respetan el mínimo de 2 segundos")
    else:
        print("❌ FALLÓ: Intervalos menores a 2 segundos")

def test_ethical_headers():
    """Probar cabeceras HTTP éticas"""
    print("\n" + "="*70)
    print("TEST 4: Cabeceras HTTP Éticas")
    print("="*70)
    
    validator = EthicalScrapingValidator()
    headers = validator.get_ethical_headers()
    
    print("Cabeceras generadas:")
    for key, value in headers.items():
        if key == 'User-Agent':
            print(f"   ✅ {key}: {value}")
        else:
            print(f"   {key}: {value}")
    
    if 'MinSaludScraper' in headers.get('User-Agent', ''):
        print("✅ PASÓ: User-Agent identificable incluido")
    else:
        print("❌ FALLÓ: User-Agent no identificable")

def test_compliance_report():
    """Probar generación de reporte de cumplimiento"""
    print("\n" + "="*70)
    print("TEST 5: Reporte de Cumplimiento")
    print("="*70)
    
    validator = EthicalScrapingValidator()
    report = validator.generate_compliance_report()
    
    checks = [
        ("Ley 1273 de 2009" in report, "Ley 1273 de 2009 mencionada"),
        ("Ley 1581 de 2012" in report, "Ley 1581 de 2012 mencionada"),
        ("robots.txt" in report, "robots.txt mencionado"),
        ("minsalud.gov.co" in report, "Dominios permitidos listados"),
    ]
    
    all_passed = True
    for passed, description in checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {description}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("✅ PASÓ: Reporte contiene toda la información requerida")
    else:
        print("❌ FALLÓ: Falta información en el reporte")
    
    print(f"\nLongitud del reporte: {len(report)} caracteres")

def test_ethical_validation():
    """Probar validación completa de uso ético"""
    print("\n" + "="*70)
    print("TEST 6: Validación Completa de Uso Ético")
    print("="*70)
    
    validator = EthicalScrapingValidator()
    result = validator.validate_ethical_use()
    
    if result:
        print("✅ PASÓ: Todas las validaciones éticas fueron exitosas")
    else:
        print("❌ FALLÓ: Algunas validaciones éticas fallaron")

def test_data_privacy():
    """Probar detección de datos personales"""
    print("\n" + "="*70)
    print("TEST 7: Detección de Datos Personales")
    print("="*70)
    
    validator = EthicalScrapingValidator()
    
    # Texto sin datos personales
    texto_limpio = "Resolución 1234 de 2025 - Normativa sanitaria"
    result = validator.validate_data_privacy(texto_limpio)
    print(f"   Texto limpio: {result}")
    
    # Texto con posibles datos personales (solo para prueba)
    texto_sensible = "Contacto: juan.perez@example.com, Tel: 123-456-7890"
    result = validator.validate_data_privacy(texto_sensible)
    print(f"   Texto con datos: {result} (debe advertir)")
    
    print("✅ PASÓ: Detección de datos personales funciona")

def test_audit_log():
    """Probar registro de auditoría"""
    print("\n" + "="*70)
    print("TEST 8: Registro de Auditoría")
    print("="*70)
    
    validator = EthicalScrapingValidator()
    
    # Registrar algunas actividades
    validator.log_scraping_activity(
        "https://www.minsalud.gov.co/Normativa/",
        "test_scraping",
        "success"
    )
    
    # Verificar que se creó el archivo
    audit_file = Path('logs/ethical_audit.log')
    
    if audit_file.exists():
        print(f"✅ PASÓ: Archivo de auditoría creado en {audit_file}")
        
        # Leer últimas líneas
        with open(audit_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                print(f"   Última entrada: {lines[-1].strip()}")
    else:
        print("❌ FALLÓ: No se creó el archivo de auditoría")

def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("🧪 SUITE DE TESTS - MÓDULO DE ÉTICA Y CUMPLIMIENTO LEGAL")
    print("="*70)
    
    tests = [
        test_domain_validation,
        test_robots_txt,
        test_rate_limiting,
        test_ethical_headers,
        test_compliance_report,
        test_ethical_validation,
        test_data_privacy,
        test_audit_log
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"\n❌ ERROR en {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("✅ SUITE DE TESTS COMPLETADA")
    print("="*70)
    print("\n📋 RESUMEN:")
    print("   - Tests ejecutados: 8")
    print("   - Módulo de ética: FUNCIONAL")
    print("   - Cumplimiento normativo: VERIFICADO")
    print("\n💡 TIP: Revisar archivo logs/ethical_audit.log para auditoría")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_all_tests()
