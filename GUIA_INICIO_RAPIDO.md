# 🚀 GUÍA RÁPIDA: Cómo Usar Este Repositorio

## 📥 Clonar el Repositorio

### Opción 1: HTTPS (Recomendado para principiantes)
```bash
git clone https://github.com/efrenbohorquez/taller-web-scraping-minsalud.git
cd taller-web-scraping-minsalud
```

### Opción 2: SSH (Requiere configuración de llaves SSH)
```bash
git clone git@github.com:efrenbohorquez/taller-web-scraping-minsalud.git
cd taller-web-scraping-minsalud
```

### Opción 3: GitHub Desktop
1. Abrir GitHub Desktop
2. File > Clone Repository
3. Buscar: `efrenbohorquez/taller-web-scraping-minsalud`
4. Elegir ubicación local
5. Click en "Clone"

---

## ⚙️ Configuración Inicial

### 1. Crear Entorno Virtual (Recomendado)
```bash
# En Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar MongoDB (Opcional)
```bash
# Copiar plantilla de configuración
cp .env.example .env

# Editar .env con tu conexión MongoDB Atlas
# MONGO_URI=mongodb+srv://usuario:password@cluster0.mongodb.net/
# MONGO_DB_NAME=minsalud_db
# MONGO_COLLECTION_NAME=normativa
```

---

## 🎯 Ejecutar el Proyecto

### Verificar Tests Éticos
```bash
# Ejecutar suite de tests éticos (debe pasar 8/8)
python test_ethical.py
```

**Resultado esperado**:
```
✅ SUITE DE TESTS COMPLETADA
   - Tests ejecutados: 8
   - Módulo de ética: FUNCIONAL
   - Cumplimiento normativo: VERIFICADO
```

### Pipeline Completo
```bash
# Extraer links + descargar PDFs + extraer texto + cargar a MongoDB
python main.py
```

### Ejecutar Solo Partes Específicas

#### Solo Extraer Links
```bash
python main.py --only-crawl
```

#### Solo Descargar PDFs
```bash
python main.py --only-download
```

#### Solo Extraer Texto de PDFs
```bash
python main.py --only-text
```

#### Solo Cargar a MongoDB
```bash
python main.py --only-mongo
```

#### Verificar Configuración
```bash
python main.py --config-check
```

---

## 📊 Consultar MongoDB

### Usando la Herramienta Interactiva
```bash
python consulta_mongodb.py
```

**Menú disponible**:
1. 📊 Mostrar estadísticas de la colección
2. 📋 Listar todos los documentos
3. 🔍 Buscar por texto
4. 📄 Ver documento completo
5. 🚪 Salir

### Búsqueda por Texto
```python
# Ejemplo en Python
from consulta_mongodb import buscar_por_texto

resultados = buscar_por_texto("alimentos")
# Retorna documentos relevantes con score de relevancia
```

---

## 🛡️ Verificar Cumplimiento Ético

### Ver Reporte de Cumplimiento
```bash
python -c "from ethical_compliance import print_compliance_report; print_compliance_report()"
```

### Revisar Log de Auditoría
```bash
# En Windows
type logs\ethical_audit.log

# En Linux/Mac
cat logs/ethical_audit.log
```

### Generar Reporte Personalizado
```python
from ethical_compliance import ethical_validator

# Generar reporte completo
report = ethical_validator.generate_compliance_report()
print(report)

# Validar uso ético
is_compliant = ethical_validator.validate_ethical_use()
```

---

## 📁 Estructura de Archivos

```
taller-web-scraping-minsalud/
│
├── 📖 Documentación Principal
│   ├── README.md                     ⭐ Empieza aquí
│   ├── LICENSE                       📄 Licencia MIT
│   ├── GUIA_INICIO_RAPIDO.md        🚀 Esta guía
│   └── RESUMEN_GITHUB.md            📊 Resumen completo
│
├── 📚 Documentación Ética
│   ├── POLITICAS_ETICA_LEGAL.md     ⚖️ Marco legal (500+ líneas)
│   ├── CERTIFICACION_ETICA.md       ✅ Certificación (8/8 tests)
│   └── GUIA_EJECUCION.md            📝 Guía de uso
│
├── 🐍 Código Fuente
│   ├── main.py                       🎯 Script principal
│   ├── config.py                     ⚙️ Configuraciones
│   ├── ethical_compliance.py         🛡️ Módulo ético (450+ líneas)
│   ├── consulta_mongodb.py           🔍 Consultas MongoDB
│   └── src/scraper.py                🕷️ Lógica de scraping
│
├── 🧪 Tests
│   ├── test_ethical.py               ⭐ Tests éticos (8/8)
│   ├── test_basic.py                 ✅ Tests básicos
│   ├── test_scraper.py               🕸️ Tests scraper
│   └── test_mongodb.py               🗄️ Tests MongoDB
│
├── 📦 Configuración
│   ├── requirements.txt              📋 Dependencias
│   ├── .env.example                  🔐 Plantilla variables
│   └── .gitignore                    🚫 Archivos excluidos
│
└── 📁 Datos
    ├── Links_MinSalud.json           🔗 43 links
    ├── pdfs/                         📄 43 PDFs
    └── json_output/                  📝 12 JSONs extraídos
```

---

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
# Asegurarse de que el entorno virtual está activo
pip install -r requirements.txt
```

### Error: "MongoDB connection failed"
```bash
# Verificar .env con credenciales correctas
python main.py --test-mongo
```

### Error: OCR no funciona
```bash
# Instalar Tesseract OCR
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
# Linux: sudo apt-get install tesseract-ocr
# Mac: brew install tesseract
```

### Tests Éticos Fallan
```bash
# Verificar conexión a internet (para robots.txt)
# Verificar que ethical_compliance.py no ha sido modificado
python test_ethical.py
```

---

## 📊 Comandos Útiles de Git

### Ver Estado
```bash
git status
```

### Ver Historial
```bash
git log --oneline
git log --graph --oneline --all
```

### Crear Nueva Rama
```bash
git checkout -b mi-nueva-funcionalidad
```

### Actualizar desde GitHub
```bash
git pull origin main
```

### Subir Cambios
```bash
git add .
git commit -m "Descripción del cambio"
git push origin main
```

---

## 🎓 Ejemplos de Uso

### Ejemplo 1: Extraer Todo y Cargar a MongoDB
```bash
# 1. Verificar ética
python test_ethical.py

# 2. Ejecutar pipeline completo
python main.py

# 3. Consultar resultados
python consulta_mongodb.py
```

### Ejemplo 2: Solo Búsqueda en MongoDB
```bash
# 1. Iniciar herramienta interactiva
python consulta_mongodb.py

# 2. Seleccionar opción 3 (Buscar por texto)

# 3. Ingresar término: "alimentos"

# 4. Ver resultados con relevancia
```

### Ejemplo 3: Generar Reporte de Cumplimiento
```bash
# Ver reporte en consola
python -c "from ethical_compliance import print_compliance_report; print_compliance_report()"

# Guardar reporte en archivo
python -c "from ethical_compliance import ethical_validator; report = ethical_validator.generate_compliance_report(); open('reporte_etica.txt', 'w', encoding='utf-8').write(report)"
```

---

## 📈 Métricas del Proyecto

### Datos Disponibles
- ✅ **43 PDFs** descargados
- ✅ **12 documentos** extraídos (2.4 MB de texto)
- ✅ **43 links** identificados
- ✅ **3 índices** MongoDB (file, timestamp, text)

### Tests
- ✅ **8/8 tests éticos** pasando
- ✅ **100% cobertura** ética
- ✅ **4 tests técnicos** adicionales

### Cumplimiento
- ✅ **5 leyes colombianas** implementadas
- ✅ **Rate limiting**: 2s mínimo, 20/min máximo
- ✅ **Whitelist**: Solo minsalud.gov.co y datos.gov.co
- ✅ **Auditoría**: Log completo JSON

---

## 🔗 Enlaces Importantes

### Repositorio
- **GitHub**: https://github.com/efrenbohorquez/taller-web-scraping-minsalud
- **Issues**: https://github.com/efrenbohorquez/taller-web-scraping-minsalud/issues
- **Commits**: https://github.com/efrenbohorquez/taller-web-scraping-minsalud/commits/main

### Documentación Legal
- **Ley 1273/2009**: http://www.secretariasenado.gov.co/senado/basedoc/ley_1273_2009.html
- **Ley 1581/2012**: http://www.secretariasenado.gov.co/senado/basedoc/ley_1581_2012.html
- **Ley 1712/2014**: http://www.secretariasenado.gov.co/senado/basedoc/ley_1712_2014.html

### Recursos Externos
- **MongoDB Atlas**: https://www.mongodb.com/cloud/atlas
- **BeautifulSoup4**: https://www.crummy.com/software/BeautifulSoup/
- **PDFMiner**: https://github.com/euske/pdfminer

---

## ⚠️ Advertencias Importantes

### Uso Ético
- ⚠️ **Solo para fines educativos e investigación**
- ⚠️ **No usar para propósitos comerciales sin autorización**
- ⚠️ **Respetar siempre las leyes colombianas**
- ⚠️ **No modificar el módulo ético**

### Datos Personales
- ⚠️ **NUNCA recopilar datos personales**
- ⚠️ **Verificar logs de advertencia**
- ⚠️ **Reportar detecciones de datos sensibles**

### Servidores
- ⚠️ **No sobrecargar servidores**
- ⚠️ **Respetar rate limiting (2s mínimo)**
- ⚠️ **No evadir robots.txt**

---

## 🎯 Objetivos de Aprendizaje

Después de usar este repositorio, deberías poder:

1. ✅ Implementar web scraping ético en Python
2. ✅ Cumplir con leyes colombianas de ciberseguridad
3. ✅ Integrar MongoDB Atlas en proyectos
4. ✅ Extraer texto de PDFs con múltiples métodos
5. ✅ Crear tests automatizados
6. ✅ Documentar legalmente proyectos de scraping
7. ✅ Usar control de versiones (Git/GitHub)

---

## 📞 Soporte

### Problemas Técnicos
- **Crear Issue**: https://github.com/efrenbohorquez/taller-web-scraping-minsalud/issues
- **Revisar Issues Existentes**: Antes de crear uno nuevo

### Contribuciones
- **Fork** el repositorio
- **Crear rama** para tu feature
- **Hacer pull request** con descripción clara

### Preguntas
- **Revisar documentación** primero (README.md, guías)
- **Buscar en Issues** cerrados
- **Crear Issue** con etiqueta "question"

---

## ✅ Checklist de Inicio

Antes de empezar, asegúrate de:

- [ ] ✅ Python 3.13 instalado
- [ ] ✅ Git instalado
- [ ] ✅ Repositorio clonado
- [ ] ✅ Entorno virtual creado
- [ ] ✅ Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] ✅ Tests éticos pasando (`python test_ethical.py`)
- [ ] ✅ Documentación ética leída (POLITICAS_ETICA_LEGAL.md)
- [ ] ✅ MongoDB configurado (opcional)
- [ ] ✅ .env creado desde .env.example (si usas MongoDB)

---

## 🎉 ¡Listo para Empezar!

Una vez completado el checklist:

```bash
# 1. Verificar que todo funciona
python test_ethical.py

# 2. Ejecutar el scraper
python main.py --only-text

# 3. Ver resultados
python consulta_mongodb.py  # Si tienes MongoDB
# O revisar data/json_output/
```

---

**¡Bienvenido al proyecto! 🚀**

**Desarrollado para el Taller de Big Data y Web Scraping**  
**Fecha**: 7 de octubre de 2025  
**Estado**: ✅ PRODUCCIÓN - LISTO PARA USAR
