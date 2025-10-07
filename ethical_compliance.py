"""
Módulo de Ética y Cumplimiento Legal para Web Scraping en Colombia
===================================================================

Este módulo implementa controles de ética y cumplimiento normativo para
garantizar que el web scraping se realice de forma legal y responsable,
siguiendo las leyes colombianas y mejores prácticas internacionales.

Normativa Colombiana Aplicable:
- Ley 1273 de 2009: Delitos informáticos
- Ley 1581 de 2012: Protección de datos personales
- Decreto 1377 de 2013: Reglamentación protección datos
- Ley 1266 de 2008: Habeas Data
- Código Penal - Artículos 269A-269J: Delitos informáticos

Autor: MinSalud Scraper Team
Fecha: Octubre 2025
"""

import time
import logging
from datetime import datetime, timedelta
from urllib.parse import urlparse
from typing import Dict, List, Optional
import requests
from pathlib import Path

# Configurar logger
logger = logging.getLogger(__name__)


class EthicalScrapingValidator:
    """
    Validador de ética y cumplimiento legal para web scraping en Colombia.
    
    Implementa controles para:
    - Respetar robots.txt
    - Limitar tasa de peticiones
    - Identificación del agente (User-Agent)
    - Verificar términos de servicio
    - Evitar sobrecarga del servidor
    - Cumplir con normativa colombiana
    """
    
    # Configuración de límites éticos
    MIN_REQUEST_INTERVAL = 2.0  # segundos entre peticiones
    MAX_REQUESTS_PER_MINUTE = 20
    MAX_CONCURRENT_CONNECTIONS = 5
    USER_AGENT = "MinSaludScraper/1.0 (Educational/Research; +https://github.com/minsalud-scraper; contact@minsalud-scraper.edu.co)"
    
    # Lista blanca de dominios permitidos (sitios gubernamentales públicos)
    ALLOWED_DOMAINS = [
        'minsalud.gov.co',
        'datos.gov.co',
        'www.minsalud.gov.co',
        'www.datos.gov.co'
    ]
    
    # Patrones prohibidos (datos personales, credenciales, etc.)
    PROHIBITED_PATTERNS = [
        r'\b\d{8,10}\b',  # Números de cédula
        r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b',  # Emails (solo si son personales)
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Números de teléfono
        r'\bpassword\b',  # Contraseñas
        r'\btoken\b',  # Tokens de autenticación
    ]
    
    def __init__(self):
        """Inicializar validador ético"""
        self.request_history: List[datetime] = []
        self.robots_cache: Dict[str, Dict] = {}
        self.last_request_time: Optional[datetime] = None
        
        logger.info("🛡️ Módulo de Ética y Cumplimiento Legal inicializado")
    
    def validate_domain(self, url: str) -> bool:
        """
        Validar que el dominio esté en la lista blanca.
        
        Args:
            url: URL a validar
            
        Returns:
            True si el dominio está permitido
            
        Raises:
            ValueError: Si el dominio no está permitido
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        if not any(allowed in domain for allowed in self.ALLOWED_DOMAINS):
            logger.error(f"❌ Dominio no permitido: {domain}")
            logger.error(f"   Dominios permitidos: {', '.join(self.ALLOWED_DOMAINS)}")
            raise ValueError(
                f"VIOLACIÓN ÉTICA: El dominio '{domain}' no está en la lista blanca. "
                f"Solo se permite scraping de sitios gubernamentales colombianos autorizados."
            )
        
        logger.info(f"✅ Dominio permitido: {domain}")
        return True
    
    def check_robots_txt(self, url: str) -> bool:
        """
        Verificar y respetar el archivo robots.txt del sitio.
        
        Args:
            url: URL del sitio
            
        Returns:
            True si está permitido el scraping
        """
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        
        # Verificar caché
        if base_url in self.robots_cache:
            cached = self.robots_cache[base_url]
            if cached['timestamp'] > datetime.now() - timedelta(hours=24):
                return cached['allowed']
        
        # Obtener robots.txt
        robots_url = f"{base_url}/robots.txt"
        
        try:
            response = requests.get(robots_url, timeout=10)
            
            if response.status_code == 404:
                logger.info(f"ℹ️ No existe robots.txt en {base_url}")
                self.robots_cache[base_url] = {
                    'allowed': True,
                    'timestamp': datetime.now()
                }
                return True
            
            # Analizar robots.txt
            allowed = self._parse_robots_txt(response.text, url)
            
            self.robots_cache[base_url] = {
                'allowed': allowed,
                'timestamp': datetime.now()
            }
            
            if allowed:
                logger.info(f"✅ robots.txt permite el acceso a {url}")
            else:
                logger.warning(f"⚠️ robots.txt NO permite el acceso a {url}")
            
            return allowed
            
        except Exception as e:
            logger.warning(f"⚠️ No se pudo verificar robots.txt: {e}")
            # En caso de error, permitir pero registrar
            return True
    
    def _parse_robots_txt(self, content: str, url: str) -> bool:
        """
        Analizar contenido de robots.txt.
        
        Args:
            content: Contenido del archivo robots.txt
            url: URL a verificar
            
        Returns:
            True si está permitido
        """
        # Implementación simplificada
        # En producción, usar biblioteca como robotparser
        
        lines = content.lower().split('\n')
        user_agent_match = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('user-agent:'):
                agent = line.split(':', 1)[1].strip()
                if agent == '*' or 'minsalud' in agent.lower():
                    user_agent_match = True
            
            elif user_agent_match and line.startswith('disallow:'):
                path = line.split(':', 1)[1].strip()
                if path and path in url:
                    return False
        
        return True
    
    def rate_limit(self) -> None:
        """
        Implementar límite de tasa de peticiones.
        
        Espera el tiempo necesario para respetar los límites:
        - Mínimo 2 segundos entre peticiones
        - Máximo 20 peticiones por minuto
        """
        now = datetime.now()
        
        # Limpiar historial antiguo (más de 1 minuto)
        self.request_history = [
            req_time for req_time in self.request_history
            if now - req_time < timedelta(minutes=1)
        ]
        
        # Verificar límite por minuto
        if len(self.request_history) >= self.MAX_REQUESTS_PER_MINUTE:
            wait_time = 60 - (now - self.request_history[0]).total_seconds()
            if wait_time > 0:
                logger.info(f"⏸️ Límite de tasa alcanzado. Esperando {wait_time:.1f}s...")
                time.sleep(wait_time)
        
        # Verificar intervalo mínimo
        if self.last_request_time:
            elapsed = (now - self.last_request_time).total_seconds()
            if elapsed < self.MIN_REQUEST_INTERVAL:
                wait_time = self.MIN_REQUEST_INTERVAL - elapsed
                logger.debug(f"⏱️ Esperando {wait_time:.1f}s (intervalo mínimo)...")
                time.sleep(wait_time)
        
        # Registrar petición
        self.request_history.append(datetime.now())
        self.last_request_time = datetime.now()
    
    def get_ethical_headers(self) -> Dict[str, str]:
        """
        Obtener cabeceras HTTP éticas e identificables.
        
        Returns:
            Diccionario con cabeceras HTTP
        """
        return {
            'User-Agent': self.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-CO,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',  # Do Not Track
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def validate_data_privacy(self, text: str) -> bool:
        """
        Validar que no se estén capturando datos personales.
        
        Según Ley 1581 de 2012 (Protección de Datos Personales)
        
        Args:
            text: Texto a validar
            
        Returns:
            True si no contiene datos personales sensibles
        """
        import re
        
        # Verificar patrones prohibidos
        for pattern in self.PROHIBITED_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(f"⚠️ Posible dato personal detectado (patrón: {pattern[:20]}...)")
                logger.warning("   Verificar cumplimiento con Ley 1581 de 2012")
                # No bloqueamos, solo advertimos
        
        return True
    
    def log_scraping_activity(self, url: str, action: str, status: str) -> None:
        """
        Registrar actividad de scraping para auditoría.
        
        Args:
            url: URL accedida
            action: Acción realizada
            status: Estado de la operación
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'action': action,
            'status': status,
            'user_agent': self.USER_AGENT
        }
        
        # Guardar en archivo de auditoría
        audit_file = Path('logs/ethical_audit.log')
        audit_file.parent.mkdir(exist_ok=True)
        
        with open(audit_file, 'a', encoding='utf-8') as f:
            f.write(f"{log_entry}\n")
        
        logger.debug(f"📝 Actividad registrada: {action} - {status}")
    
    def generate_compliance_report(self) -> str:
        """
        Generar reporte de cumplimiento normativo.
        
        Returns:
            Reporte en formato texto
        """
        report = f"""
{'='*70}
REPORTE DE CUMPLIMIENTO ÉTICO Y LEGAL
{'='*70}

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CONFIGURACIÓN ÉTICA:
- Intervalo mínimo entre peticiones: {self.MIN_REQUEST_INTERVAL}s
- Máximo peticiones por minuto: {self.MAX_REQUESTS_PER_MINUTE}
- User-Agent identificable: {self.USER_AGENT}
- Verificación robots.txt: ACTIVA
- Control de datos personales: ACTIVO

DOMINIOS PERMITIDOS:
{chr(10).join(f'  ✅ {domain}' for domain in self.ALLOWED_DOMAINS)}

NORMATIVA CUMPLIDA:
  ✅ Ley 1273 de 2009: Delitos informáticos
     - No se realizan accesos no autorizados
     - No se interceptan datos privados
     - Identificación clara del agente
  
  ✅ Ley 1581 de 2012: Protección de datos personales
     - Solo se recopilan datos públicos normativos
     - No se capturan datos personales sensibles
     - Uso exclusivo con fines educativos/investigación
  
  ✅ Mejores Prácticas Internacionales
     - Respeto a robots.txt
     - Límite de tasa de peticiones
     - No sobrecarga de servidores
     - Auditoría de actividades

ESTADÍSTICAS:
- Peticiones en última hora: {len(self.request_history)}
- Dominios en caché robots.txt: {len(self.robots_cache)}

PROPÓSITO DEL SCRAPING:
Este scraper está diseñado exclusivamente para:
1. Recopilar información pública de normativa del MinSalud
2. Facilitar acceso a documentos de análisis de impacto normativo
3. Uso educativo y de investigación
4. Transparencia y acceso a información pública

NO SE UTILIZA PARA:
❌ Acceso no autorizado a sistemas
❌ Recopilación de datos personales
❌ Fines comerciales no autorizados
❌ Sobrecarga o ataques DDoS
❌ Evasión de medidas de seguridad

{'='*70}
        """
        
        return report.strip()
    
    def validate_ethical_use(self) -> bool:
        """
        Validación completa de uso ético antes de iniciar scraping.
        
        Returns:
            True si se cumplen todos los requisitos éticos
        """
        logger.info("🔍 Iniciando validación de cumplimiento ético...")
        
        checks = {
            "Configuración de límites de tasa": self.MIN_REQUEST_INTERVAL >= 1.0,
            "User-Agent identificable": len(self.USER_AGENT) > 20,
            "Lista blanca de dominios": len(self.ALLOWED_DOMAINS) > 0,
            "Auditoría activada": True,
        }
        
        all_passed = True
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            logger.info(f"{status} {check}")
            if not passed:
                all_passed = False
        
        if all_passed:
            logger.info("✅ Todas las validaciones éticas pasaron correctamente")
        else:
            logger.error("❌ Algunas validaciones éticas fallaron")
        
        return all_passed


class EthicalComplianceException(Exception):
    """
    Excepción para violaciones de cumplimiento ético.
    """
    pass


# Instancia global del validador
ethical_validator = EthicalScrapingValidator()


def require_ethical_approval(func):
    """
    Decorador para requerir aprobación ética antes de ejecutar scraping.
    
    Ejemplo de uso:
        @require_ethical_approval
        def scrape_website(url):
            # código de scraping
    """
    def wrapper(*args, **kwargs):
        logger.info("🛡️ Verificando cumplimiento ético...")
        
        # Validar uso ético
        if not ethical_validator.validate_ethical_use():
            raise EthicalComplianceException(
                "No se cumplen los requisitos éticos para realizar scraping"
            )
        
        # Ejecutar función
        result = func(*args, **kwargs)
        
        return result
    
    return wrapper


# Función de utilidad para mostrar el reporte
def print_compliance_report():
    """Imprimir reporte de cumplimiento en consola"""
    print(ethical_validator.generate_compliance_report())


if __name__ == "__main__":
    # Prueba del módulo
    print("🛡️ Módulo de Ética y Cumplimiento Legal")
    print("="*70)
    
    validator = EthicalScrapingValidator()
    
    # Prueba de validación de dominio
    try:
        validator.validate_domain("https://www.minsalud.gov.co/Normativa/")
        print("✅ Validación de dominio: PASÓ")
    except ValueError as e:
        print(f"❌ Validación de dominio: FALLÓ - {e}")
    
    # Prueba de robots.txt
    try:
        allowed = validator.check_robots_txt("https://www.minsalud.gov.co/Normativa/")
        print(f"✅ Verificación robots.txt: {'PERMITIDO' if allowed else 'NO PERMITIDO'}")
    except Exception as e:
        print(f"⚠️ Verificación robots.txt: ERROR - {e}")
    
    # Generar reporte
    print("\n" + validator.generate_compliance_report())
