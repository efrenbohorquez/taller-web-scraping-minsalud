# 🚀 GUÍA RÁPIDA DE EJECUCIÓN

## ✅ Verificación Inicial

```powershell
# 1. Navegar al directorio del proyecto
cd "c:\Users\efren\TALLER BIG DATA WEB SCRAPING\minsalud_scraper"

# 2. Verificar configuración
python main.py --config-check
```

## 📋 Ejecución Paso a Paso (Recomendado para Primera Vez)

### PASO 1: Crawling (Extraer Links)
```powershell
python main.py --only-crawl
```
**Resultado esperado**: Archivo `data/Links_MinSalud.json` con todos los links encontrados

### PASO 2: Descargar PDFs
```powershell
python main.py --only-download
```
**Resultado esperado**: PDFs descargados en `data/pdfs/`

### PASO 3: Extraer Texto de PDFs
```powershell
python main.py --only-text
```
**Resultado esperado**: JSONs con texto en `data/json_output/`

### PASO 4: Cargar a MongoDB (Opcional)
```powershell
# Primero configurar MongoDB URI en .env o config.py
python main.py --only-mongo
```
**Resultado esperado**: Documentos cargados en MongoDB

---

## ⚡ Ejecución Completa (Todo de una vez)

```powershell
python main.py
```

**Ejecuta automáticamente**:
1. ✅ Crawling
2. ✅ Descarga de PDFs
3. ✅ Extracción de texto
4. ✅ Carga a MongoDB

⏱️ **Tiempo estimado**: Depende del número de documentos (puede ser varias horas para todo el sitio)

---

## 🧪 Modo Prueba Rápida

```powershell
# Ejecutar suite de pruebas (procesamiento limitado)
python test_scraper.py
```

**Características del modo prueba**:
- Límite de 5 páginas
- Proceso rápido (~30 segundos)
- Ideal para verificar funcionamiento

---

## 📊 Monitoreo en Tiempo Real

### Ver logs en tiempo real
```powershell
# En otra terminal
Get-Content "logs/scraper_$(Get-Date -Format 'yyyyMMdd')*.log" -Wait
```

### Verificar archivos generados
```powershell
# Ver cantidad de PDFs descargados
(Get-ChildItem "data/pdfs" -Filter *.pdf).Count

# Ver cantidad de JSONs generados
(Get-ChildItem "data/json_output" -Filter *.json).Count

# Ver el archivo de links
Get-Content "data/Links_MinSalud.json" | python -m json.tool
```

---

## 🛠️ Solución de Problemas Comunes

### Error: "ModuleNotFoundError"
```powershell
pip install -r requirements.txt --upgrade
```

### Error: "pytesseract not found"
1. Descargar Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Instalar en `C:\Program Files\Tesseract-OCR\`
3. Agregar al PATH del sistema

### Error: "MongoDB connection failed"
- Verificar que MongoDB está ejecutándose (local)
- O configurar MONGO_URI correctamente para MongoDB Atlas
- Para omitir MongoDB temporalmente, ejecutar solo pasos 1-3

### El scraper no encuentra PDFs
- Normal si la sección del sitio no tiene PDFs directos
- Algunos documentos pueden estar en subsecciones
- Ejecutar sin límite de páginas para exploración completa

---

## 📈 Estadísticas Esperadas

### Tiempos Aproximados por Operación

| Operación | Tiempo por Página/Archivo |
|-----------|---------------------------|
| Crawling | 1-2 seg/página |
| Descarga PDF | 0.5-5 seg/archivo |
| Extracción Normal | 0.1-0.5 seg/PDF |
| Extracción OCR | 2-10 seg/PDF |
| Carga MongoDB | <0.1 seg/doc |

### Recursos del Sistema

| Recurso | Uso Típico |
|---------|------------|
| CPU | 10-30% (descarga), 50-80% (OCR) |
| RAM | 200-500 MB |
| Disco | Depende de cantidad de PDFs |
| Red | 1-5 Mbps promedio |

---

## 🎯 Casos de Uso

### Caso 1: Solo quiero los links
```powershell
python main.py --only-crawl
# Resultado: data/Links_MinSalud.json
```

### Caso 2: Ya tengo los links, solo quiero PDFs
```powershell
python main.py --only-download
# Resultado: data/pdfs/*.pdf
```

### Caso 3: Quiero todo excepto MongoDB
```powershell
python main.py --only-crawl
python main.py --only-download
python main.py --only-text
# Resultado: PDFs + JSONs sin cargar a base de datos
```

### Caso 4: Pipeline completo con MongoDB
```powershell
# Configurar .env con MONGO_URI
python main.py
# Resultado: Todo el proceso completo
```

---

## 📞 Ayuda Adicional

### Ver ayuda del CLI
```powershell
python main.py --help
```

### Revisar documentación completa
```powershell
# Abrir README.md
notepad README.md

# Abrir resumen de ejecución
notepad RESUMEN_EJECUCION.md
```

### Verificar estado del proyecto
```powershell
# Ver estructura de directorios
tree /F

# Ver últimos logs
Get-Content "logs/*.log" | Select-Object -Last 50
```

---

## ✅ Checklist Pre-Ejecución

Antes de ejecutar el scraper completo, verificar:

- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Tesseract instalado (para OCR)
- [ ] Conexión a Internet estable
- [ ] MongoDB configurado (si se va a usar)
- [ ] Espacio en disco suficiente (~1-5 GB recomendado)
- [ ] Verificación de configuración exitosa (`python main.py --config-check`)

---

## 🎉 ¡Listo para Ejecutar!

Una vez verificado todo, ejecutar:

```powershell
# Modo completo
python main.py

# O paso a paso
python main.py --only-crawl
python main.py --only-download
python main.py --only-text
```

**¡El scraper hará el resto automáticamente!**
