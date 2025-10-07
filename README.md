# MinSalud Web Scraper

Un sistema completo de web scraping **ético y legal** para extraer documentos de normatividad del sitio web del Ministerio de Salud de Colombia.

## 🚀 Características

- ✅ **Crawling inteligente**: Extrae automáticamente todos los links del sitio
- ✅ **Descarga paralela**: Descarga PDFs de manera eficiente
- ✅ **Extracción de texto**: Usa PDFMiner y OCR como respaldo
- ✅ **Base de datos**: Carga automática a MongoDB Atlas
- ✅ **Logging completo**: Seguimiento detallado de todo el proceso
- ✅ **Manejo de errores**: Robusto y resistente a fallos
- 🛡️ **Módulo de Ética**: Cumplimiento con leyes colombianas (Ley 1273/2009, Ley 1581/2012)
- 🔒 **Rate Limiting**: Control de tasa de peticiones (2s mínimo entre requests)
- 📋 **Auditoría Completa**: Registro de todas las actividades para accountability
- ⚖️ **Respeto robots.txt**: Verificación automática antes de cada request

## 📋 Instalación

### 1. Instalar dependencias básicas
```bash
pip install -r requirements.txt
```

### 2. Dependencias opcionales para OCR
```bash
# Para Windows
pip install pytesseract pdf2image Pillow

# Descargar e instalar Tesseract OCR
# https://github.com/UB-Mannheim/tesseract/wiki
```

### 3. Configurar MongoDB
Editar `config.py` con tu URI de MongoDB Atlas:
```python
MONGO_URI = "mongodb+srv://usuario:password@cluster0.mongodb.net/"
```

## 🎯 Uso

### Ejecutar pipeline completo
```bash
python main.py
```

### Ejecutar solo partes específicas
```bash
# Solo extraer links
python main.py --only-crawl

# Solo descargar PDFs
python main.py --only-download

# Solo extraer texto
python main.py --only-text

# Solo cargar a MongoDB
python main.py --only-mongo

# Verificar configuración
python main.py --config-check
```

### Prueba básica
```bash
python test_basic.py
```

## �️ Cumplimiento Ético y Legal

Este proyecto incluye un **módulo completo de ética** que garantiza el cumplimiento de las leyes colombianas:

### Leyes Cumplidas
- ✅ **Ley 1273/2009**: Prevención de delitos informáticos
- ✅ **Ley 1581/2012**: Protección de datos personales
- ✅ **Ley 1712/2014**: Acceso a información pública
- ✅ **Decreto 1377/2013**: Reglamentación de datos

### Controles Implementados
- 🔒 **Whitelist de dominios**: Solo `minsalud.gov.co` y `datos.gov.co`
- ⏱️ **Rate limiting**: 2 segundos mínimo entre peticiones
- 🤖 **robots.txt**: Verificación automática antes de cada request
- 🔍 **Detección de datos personales**: Protege cédulas, emails, teléfonos
- 📝 **Auditoría completa**: Log de todas las actividades en `logs/ethical_audit.log`

### Ejecutar Tests Éticos
```bash
# Verificar cumplimiento legal
python test_ethical.py

# Ver reporte de cumplimiento
python -c "from ethical_compliance import print_compliance_report; print_compliance_report()"
```

### Documentación Ética
- 📄 **POLITICAS_ETICA_LEGAL.md**: Marco legal completo
- 🎓 **CERTIFICACION_ETICA.md**: Resultados de tests y certificación
- 📋 Ver también: `ethical_compliance.py` para detalles técnicos

## �📁 Estructura del proyecto

```
minsalud_scraper/
├── main.py              # Script principal
├── config.py            # Configuraciones
├── requirements.txt     # Dependencias
├── test_basic.py        # Pruebas básicas
├── data/
│   ├── pdfs/           # PDFs descargados
│   ├── json_output/    # Textos extraídos (JSON)
│   └── Links_MinSalud.json  # Lista de links
├── logs/               # Archivos de log
└── src/
    └── scraper.py      # Código principal
```

## ⚙️ Configuración

El archivo `config.py` contiene todas las configuraciones:

- **URLs**: Sitio web objetivo
- **Rutas**: Directorios de almacenamiento  
- **MongoDB**: Configuración de base de datos
- **OCR**: Configuración de Tesseract
- **Paralelización**: Número de workers

## 📊 Salida

### Archivos JSON individuales
Cada PDF procesado genera un archivo JSON con:
```json
{
    "file": "nombre_archivo.pdf",
    "timestamp": "2025-10-07T...",
    "text": "texto extraído...",
    "method": "PDFMINER|OCR",
    "size_bytes": 123456,
    "char_count": 5000
}
```

### Base de datos MongoDB
Los mismos datos se cargan automáticamente a MongoDB Atlas.

## 🔧 Solución de problemas

### Error de OCR
```bash
# Instalar Tesseract en Windows
choco install tesseract

# O descargar desde:
# https://github.com/UB-Mannheim/tesseract/wiki
```

### Error de MongoDB
- Verificar URI de conexión
- Comprobar conectividad de red
- Validar credenciales

### Errores de red
- El script incluye reintentos automáticos
- Ajustar `REQUEST_TIMEOUT` en config.py

## 📈 Rendimiento

- **Descarga paralela**: Hasta 5 PDFs simultáneos
- **Extracción inteligente**: PDFMiner primero, OCR como respaldo
- **Manejo de memoria**: Procesamiento por chunks
- **Logging eficiente**: Rotación automática de logs

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para feature
3. Commit cambios
4. Push a la rama
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es de código abierto bajo licencia MIT.

---
**Desarrollado para el Taller de Big Data y Web Scraping** 🚀