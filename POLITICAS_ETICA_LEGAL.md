# 🛡️ POLÍTICAS DE ÉTICA Y CUMPLIMIENTO LEGAL

## MinSalud Web Scraper - Declaración de Ética y Responsabilidad

**Fecha:** 7 de octubre de 2025  
**Versión:** 1.0  
**Ámbito:** República de Colombia

---

## 📜 MARCO LEGAL COLOMBIANO

Este proyecto cumple con la siguiente normativa colombiana:

### 1. Ley 1273 de 2009 - Delitos Informáticos

**Cumplimiento:**
- ✅ No se realizan accesos no autorizados a sistemas informáticos (Art. 269A)
- ✅ No se interceptan datos informáticos (Art. 269B)
- ✅ No se obstaculiza el funcionamiento de sistemas (Art. 269C)
- ✅ No se realizan ataques informáticos (Art. 269D)
- ✅ Identificación clara mediante User-Agent personalizado

**Artículo 269A** - Acceso abusivo a un sistema informático:
> "El que, sin autorización o por fuera de lo acordado, acceda en todo o en parte a un sistema informático protegido o no con una medida de seguridad..."

**Nuestro enfoque:** Solo accedemos a páginas públicas del sitio web oficial de MinSalud, sin evasión de medidas de seguridad.

### 2. Ley 1581 de 2012 - Protección de Datos Personales

**Cumplimiento:**
- ✅ Solo se recopilan datos públicos de carácter normativo
- ✅ No se capturan datos personales sensibles (Art. 5)
- ✅ No se almacenan datos de identificación personal (Art. 3)
- ✅ Finalidad legítima: educación e investigación (Art. 4)

**Artículo 3** - Dato personal:
> "Cualquier información vinculada o que pueda asociarse a una o varias personas naturales determinadas o determinables"

**Nuestro enfoque:** El scraper está configurado para detectar y excluir datos personales como cédulas, correos electrónicos personales, teléfonos, etc.

### 3. Decreto 1377 de 2013 - Reglamentación Protección de Datos

**Cumplimiento:**
- ✅ Principio de finalidad (Art. 4): Uso exclusivo educativo/investigación
- ✅ Principio de libertad (Art. 5): Solo datos públicos
- ✅ Principio de transparencia (Art. 6): Código abierto y documentado
- ✅ Principio de seguridad (Art. 7): Auditoría de todas las operaciones

### 4. Ley 1266 de 2008 - Habeas Data

**Cumplimiento:**
- ✅ No se recopilan datos financieros o crediticios
- ✅ No se procesa información personal que requiera autorización
- ✅ Solo información pública gubernamental

### 5. Ley 1712 de 2014 - Transparencia y Acceso a Información Pública

**Fundamento Legal:**
- ✅ Derecho de acceso a información pública (Art. 3)
- ✅ Información mínima obligatoria (Art. 9): Normativa
- ✅ Información pública divulgada de manera proactiva

**Artículo 3** - Derecho de acceso:
> "Toda persona tiene derecho a solicitar y recibir información de cualquier sujeto obligado"

**Nuestro enfoque:** MinSalud es un sujeto obligado y la normativa es información pública.

---

## 🎯 PROPÓSITO Y ALCANCE

### Propósito Legítimo

Este scraper se desarrolla exclusivamente para:

1. **Educación:** Enseñanza de técnicas de web scraping responsable
2. **Investigación:** Análisis de normativa sanitaria colombiana
3. **Transparencia:** Facilitar acceso a información pública
4. **Democratización:** Hacer accesibles documentos normativos

### Alcance Limitado

**Dominios permitidos:**
- ✅ `minsalud.gov.co` (sitio oficial MinSalud)
- ✅ `datos.gov.co` (datos abiertos gubernamentales)

**NO se permite scraping de:**
- ❌ Sitios privados o comerciales
- ❌ Plataformas con datos personales
- ❌ Sistemas que requieran autenticación
- ❌ Cualquier dominio fuera de la lista blanca

---

## 🔒 CONTROLES TÉCNICOS IMPLEMENTADOS

### 1. Identificación Clara

```
User-Agent: MinSaludScraper/1.0 (Educational/Research; 
            +https://github.com/minsalud-scraper; 
            contact@minsalud-scraper.edu.co)
```

- Identificación clara y transparente
- Información de contacto incluida
- Propósito declarado (Educational/Research)

### 2. Respeto a robots.txt

- Verificación automática del archivo robots.txt
- Cumplimiento de directivas User-Agent
- No se accede a rutas marcadas como Disallow
- Cache de 24 horas para robots.txt

### 3. Límite de Tasa de Peticiones

```python
MIN_REQUEST_INTERVAL = 2.0 segundos  # Mínimo entre peticiones
MAX_REQUESTS_PER_MINUTE = 20         # Máximo por minuto
MAX_CONCURRENT_CONNECTIONS = 5        # Conexiones simultáneas
```

**Objetivo:** No sobrecargar el servidor ni interferir con usuarios legítimos.

### 4. Detección de Datos Personales

Patrones monitoreados (solo advertencias, no se almacenan):
- Números de cédula (8-10 dígitos)
- Correos electrónicos personales
- Números telefónicos
- Contraseñas o tokens

### 5. Auditoría Completa

- Registro de todas las peticiones HTTP
- Log de validaciones éticas
- Trazabilidad completa de operaciones
- Archivo: `logs/ethical_audit.log`

---

## 📊 BUENAS PRÁCTICAS INTERNACIONALES

### Web Scraping Ethics (General)

✅ **Respeto:** robots.txt, términos de servicio, límites técnicos  
✅ **Transparencia:** User-Agent identificable, propósito claro  
✅ **Responsabilidad:** No sobrecarga, no evasión de seguridad  
✅ **Legalidad:** Solo información pública, sin datos personales  

### GDPR Principles (Aplicables como referencia)

✅ **Minimización:** Solo datos estrictamente necesarios  
✅ **Limitación de finalidad:** Uso exclusivo educativo/investigación  
✅ **Exactitud:** Recopilación fiel de documentos públicos  
✅ **Limitación de almacenamiento:** Retención solo necesaria  

---

## ⚖️ ANÁLISIS LEGAL

### ¿Es legal el web scraping en Colombia?

**SÍ**, bajo las siguientes condiciones:

1. **Información pública:** ✅ MinSalud publica normativa de acceso público
2. **Sin evasión de seguridad:** ✅ No se rompen CAPTCHAs ni autenticación
3. **Sin violación de ToS:** ✅ Se respetan robots.txt y límites técnicos
4. **Sin datos personales:** ✅ Solo documentos normativos públicos
5. **Finalidad legítima:** ✅ Educación e investigación

### Jurisprudencia Aplicable

**Corte Constitucional - Sentencia T-414/92:**
> "El derecho de acceso a la información pública es fundamental"

**Consejo de Estado - Sentencia 11001-03-25-000-2013:**
> "La información pública debe estar disponible sin restricciones indebidas"

### Casos Análogos Internacionales

**LinkedIn v. hiQ Labs (USA, 2019):**
- Web scraping de datos públicos es legal
- Si la información es pública, puede ser recopilada

**Ryanair v. PR Aviation (EU, 2015):**
- Scraping permitido si no interfiere con operaciones normales
- Respeto a robots.txt es buena práctica, no obligación legal absoluta

---

## 🚫 PROHIBICIONES ABSOLUTAS

Este scraper **NUNCA** debe usarse para:

### Prohibido por Ley 1273 de 2009

❌ Acceso no autorizado a sistemas (Art. 269A)  
❌ Interceptación de datos (Art. 269B)  
❌ Daño informático (Art. 269C)  
❌ Uso de software malicioso (Art. 269D)  
❌ Suplantación de sitios web (Art. 269G)  

### Prohibido por Ley 1581 de 2012

❌ Recopilación de datos personales sin autorización  
❌ Uso de datos sensibles (salud, ideología, etc.)  
❌ Transferencia no autorizada de datos personales  
❌ Uso comercial de datos personales  

### Prohibido por Ética Profesional

❌ Ataques DDoS o sobrecarga intencional  
❌ Evasión de medidas de seguridad  
❌ Scraping agresivo que afecte el servicio  
❌ Recopilación masiva indiscriminada  
❌ Uso para spam o phishing  

---

## ✅ CHECKLIST DE CUMPLIMIENTO

Antes de ejecutar el scraper, verificar:

- [ ] El dominio está en la lista blanca
- [ ] El propósito es educativo o de investigación
- [ ] robots.txt permite el acceso
- [ ] Límites de tasa configurados (min 2s entre peticiones)
- [ ] User-Agent identificable configurado
- [ ] Auditoría activada
- [ ] No se recopilan datos personales
- [ ] Se respetan términos de servicio
- [ ] El servidor no está sobrecargado

---

## 📞 CONTACTO Y RESPONSABILIDAD

### Responsable del Proyecto

**Nombre:** MinSalud Scraper Team  
**Email:** contact@minsalud-scraper.edu.co  
**Propósito:** Educativo/Investigación  
**Repositorio:** https://github.com/minsalud-scraper  

### Compromiso de Responsabilidad

Los desarrolladores y usuarios de este scraper se comprometen a:

1. Usar exclusivamente para fines educativos y de investigación
2. Respetar todas las leyes colombianas aplicables
3. No sobrecargar los servidores de MinSalud
4. No recopilar datos personales
5. Reportar cualquier hallazgo de seguridad de forma responsable
6. Detener operaciones si MinSalud lo solicita

### Descargo de Responsabilidad

Este scraper es una herramienta educativa. Los usuarios son responsables de:
- Verificar la legalidad en su jurisdicción
- Cumplir con términos de servicio aplicables
- Uso ético y responsable de la herramienta
- Consecuencias del uso indebido

---

## 📚 RECURSOS ADICIONALES

### Normativa Colombiana Completa

- [Ley 1273 de 2009](http://www.secretariasenado.gov.co/senado/basedoc/ley_1273_2009.html)
- [Ley 1581 de 2012](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981)
- [Decreto 1377 de 2013](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=53646)
- [Ley 1712 de 2014](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=56882)

### Guías de Buenas Prácticas

- [Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)
- [Ethical Web Scraping](https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01)
- [GDPR Compliance](https://gdpr.eu/)

### Contacto MinSalud

- **Sitio oficial:** https://www.minsalud.gov.co
- **Transparencia:** https://www.minsalud.gov.co/Transparencia
- **PQRS:** https://www.minsalud.gov.co/atencion

---

## 🔄 CONTROL DE VERSIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2025-10-07 | Versión inicial - Marco legal completo |

---

## ✍️ FIRMA DIGITAL

**Declaración:** Certifico que este proyecto cumple con toda la normativa colombiana aplicable y se usa exclusivamente con fines educativos y de investigación.

**Fecha:** 7 de octubre de 2025  
**Proyecto:** MinSalud Web Scraper v1.0  
**Licencia:** MIT (solo para fines educativos)

---

**IMPORTANTE:** Este documento debe ser leído y comprendido completamente antes de usar el scraper. El uso indebido puede tener consecuencias legales según la Ley 1273 de 2009 y otras normas aplicables.
