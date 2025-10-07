# 🗄️ GUÍA COMPLETA DE MONGODB PARA MINSALUD SCRAPER

## 📋 Índice
1. [Introducción](#introducción)
2. [Opción 1: MongoDB Atlas (Cloud - Recomendado)](#opción-1-mongodb-atlas-cloud)
3. [Opción 2: MongoDB Local](#opción-2-mongodb-local)
4. [Configuración del Proyecto](#configuración-del-proyecto)
5. [Pruebas y Verificación](#pruebas-y-verificación)
6. [Uso del Módulo](#uso-del-módulo)
7. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Introducción

El módulo de MongoDB permite almacenar los documentos extraídos en una base de datos NoSQL para:
- ✅ Consultas rápidas y eficientes
- ✅ Búsquedas de texto completo
- ✅ Escalabilidad
- ✅ Backup automático (Atlas)
- ✅ Acceso desde múltiples aplicaciones

---

## ☁️ Opción 1: MongoDB Atlas (Cloud - Recomendado)

### Ventajas
- ✅ Gratis hasta 512 MB
- ✅ Sin instalación local
- ✅ Backup automático
- ✅ Alta disponibilidad
- ✅ Acceso desde cualquier lugar

### Pasos de Configuración

#### 1. Crear Cuenta en MongoDB Atlas

1. Ir a: https://www.mongodb.com/cloud/atlas/register
2. Registrarse con email (o Google/GitHub)
3. Verificar email

#### 2. Crear Cluster Gratuito

1. Hacer clic en "Build a Database"
2. Seleccionar **FREE** (M0 Sandbox)
3. Elegir región (preferiblemente cercana):
   - US East (N. Virginia) - us-east-1
   - US West (Oregon) - us-west-2
4. Nombrar el cluster (ej: `minsalud-cluster`)
5. Hacer clic en "Create Cluster"
6. Esperar 3-5 minutos mientras se crea

#### 3. Crear Usuario de Base de Datos

1. En el menú lateral, ir a **Database Access**
2. Hacer clic en "Add New Database User"
3. Configurar:
   ```
   Authentication Method: Password
   Username: minsalud_user
   Password: (generar uno fuerte o crear uno)
   ```
4. Database User Privileges: **Read and write to any database**
5. Guardar el password en un lugar seguro
6. Hacer clic en "Add User"

#### 4. Configurar Network Access (Whitelist de IPs)

1. En el menú lateral, ir a **Network Access**
2. Hacer clic en "Add IP Address"
3. **Para desarrollo/pruebas**:
   - Hacer clic en "Allow Access from Anywhere"
   - Esto agregará `0.0.0.0/0`
   - ⚠️ **NO recomendado para producción**
4. **Para producción**:
   - Agregar solo tu IP específica
5. Hacer clic en "Confirm"

#### 5. Obtener Connection String

1. Ir a **Database** en el menú lateral
2. En tu cluster, hacer clic en "Connect"
3. Seleccionar "Connect your application"
4. Driver: **Python** / Version: **3.12 or later**
5. Copiar el Connection String:
   ```
   mongodb+srv://minsalud_user:<password>@cluster0.xxxxx.mongodb.net/
   ```
6. **IMPORTANTE**: Reemplazar `<password>` con tu password real

#### 6. Configurar en el Proyecto

**Opción A: Archivo .env (Recomendado)**

Crear archivo `.env` en la raíz del proyecto:

```ini
MONGO_URI=mongodb+srv://minsalud_user:TU_PASSWORD_AQUI@cluster0.xxxxx.mongodb.net/
MONGO_DB_NAME=minsalud_db
MONGO_COLLECTION_NAME=normativa
```

**Opción B: Editar config.py directamente**

Editar `config.py`:

```python
MONGO_URI = "mongodb+srv://minsalud_user:TU_PASSWORD_AQUI@cluster0.xxxxx.mongodb.net/"
DB_NAME = "minsalud_db"
COLLECTION_NAME = "normativa"
```

---

## 💻 Opción 2: MongoDB Local

### Ventajas
- ✅ Control total
- ✅ Sin límite de almacenamiento (depende de tu disco)
- ✅ No requiere internet para trabajar

### Desventajas
- ❌ Requiere instalación
- ❌ No tiene backup automático
- ❌ Solo accesible desde tu máquina

### Pasos de Configuración

#### 1. Instalar MongoDB Community Edition

**Windows:**

1. Descargar desde: https://www.mongodb.com/try/download/community
2. Ejecutar el instalador (.msi)
3. Durante instalación:
   - Seleccionar "Complete"
   - Marcar "Install MongoDB as a Service"
   - Dejar opciones por defecto
4. Finalizar instalación

**Linux (Ubuntu/Debian):**

```bash
# Importar clave pública
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Agregar repositorio
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Actualizar e instalar
sudo apt-get update
sudo apt-get install -y mongodb-org

# Iniciar servicio
sudo systemctl start mongod
sudo systemctl enable mongod
```

**macOS:**

```bash
# Instalar con Homebrew
brew tap mongodb/brew
brew install mongodb-community@6.0

# Iniciar servicio
brew services start mongodb-community@6.0
```

#### 2. Iniciar MongoDB

**Windows:**

Si se instaló como servicio, ya debería estar corriendo.
Para verificar:

```powershell
# Verificar que el servicio está corriendo
Get-Service -Name MongoDB

# O iniciar manualmente
mongod --dbpath C:\data\db
```

**Linux/macOS:**

```bash
# Verificar estado
sudo systemctl status mongod

# Iniciar si no está corriendo
sudo systemctl start mongod
```

#### 3. Configurar en el Proyecto

Editar `config.py` o crear `.env`:

```ini
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=minsalud_db
MONGO_COLLECTION_NAME=normativa
```

---

## ⚙️ Configuración del Proyecto

### Estructura de Configuración

El proyecto soporta dos métodos de configuración:

#### 1. Variables de Entorno (.env)

Crear archivo `.env` en la raíz:

```ini
# MongoDB Connection
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
MONGO_DB_NAME=minsalud_db
MONGO_COLLECTION_NAME=normativa
```

#### 2. Edición Directa (config.py)

Editar `config.py` líneas 19-21:

```python
MONGO_URI = "tu_connection_string_aqui"
DB_NAME = "minsalud_db"
COLLECTION_NAME = "normativa"
```

---

## 🧪 Pruebas y Verificación

### 1. Verificar PyMongo Instalado

```powershell
python -c "import pymongo; print(pymongo.__version__)"
```

Debe mostrar: `4.15.2` o superior

### 2. Probar Conexión

```powershell
python main.py --test-mongo
```

O ejecutar suite completa:

```powershell
python test_mongodb.py
```

### 3. Verificar Configuración

```powershell
python main.py --config-check
```

---

## 🚀 Uso del Módulo

### Cargar Datos a MongoDB

```powershell
# Solo cargar a MongoDB (requiere archivos JSON en data/json_output/)
python main.py --only-mongo

# Pipeline completo (crawling + download + texto + MongoDB)
python main.py
```

### Características del Módulo

#### ✅ Inserción por Lotes (Batch Insert)
- Inserta múltiples documentos a la vez
- Configurable: `batch_size=100` por defecto
- Mejora rendimiento significativamente

#### ✅ Detección de Duplicados
- Verifica si el documento ya existe (por campo `file`)
- No re-inserta documentos existentes
- Ahorra espacio y tiempo

#### ✅ Actualización Inteligente
- Si el documento existe pero el texto cambió, lo actualiza
- Mantiene histórico con timestamp

#### ✅ Índices Automáticos
- Índice en campo `file` (único)
- Índice en campo `timestamp`
- Índice de texto completo para búsquedas

#### ✅ Metadata Enriquecida
- `_uploaded_at`: Timestamp de carga
- `_source_file`: Archivo JSON origen
- `file`: Nombre del PDF original
- `timestamp`: Cuando se extrajo el texto
- `text`: Contenido del documento
- `method`: Método de extracción (NORMAL/OCR)

### Ejemplo de Documento en MongoDB

```json
{
  "_id": ObjectId("..."),
  "file": "resolucion_123_2025.pdf",
  "timestamp": "2025-10-07T12:30:00",
  "text": "Contenido del documento...",
  "method": "NORMAL",
  "_uploaded_at": "2025-10-07T13:45:00",
  "_source_file": "minsalud_texto_001.json"
}
```

---

## 🔍 Consultas y Búsquedas

### Desde Python

```python
from pymongo import MongoClient

client = MongoClient("tu_connection_string")
db = client["minsalud_db"]
collection = db["normativa"]

# Buscar por nombre de archivo
doc = collection.find_one({"file": "resolucion_123.pdf"})

# Buscar por texto (búsqueda de texto completo)
resultados = collection.find({
    "$text": {"$search": "vacunación covid"}
})

# Contar documentos
total = collection.count_documents({})
print(f"Total de documentos: {total}")

# Documentos por método de extracción
por_metodo = collection.aggregate([
    {"$group": {"_id": "$method", "count": {"$sum": 1}}}
])
```

### Desde MongoDB Compass (GUI)

1. Descargar: https://www.mongodb.com/try/download/compass
2. Conectar con tu connection string
3. Navegar a `minsalud_db` → `normativa`
4. Usar filtros visuales para buscar

---

## 🛠️ Solución de Problemas

### Error: "No se puede establecer conexión"

**MongoDB Local:**
```powershell
# Verificar que MongoDB está corriendo
Get-Service -Name MongoDB

# Iniciar si está detenido
Start-Service -Name MongoDB
```

**MongoDB Atlas:**
- Verificar IP en Network Access whitelist
- Verificar username y password
- Verificar que reemplazaste `<password>` en el connection string

### Error: "Authentication failed"

- Verificar username y password
- Recrear usuario en Atlas → Database Access
- Verificar que el password no tiene caracteres especiales sin encodear

### Error: "ServerSelectionTimeoutError"

- Verificar conexión a internet (Atlas)
- Verificar que MongoDB está corriendo (Local)
- Aumentar timeout en código si internet es lento

### Error: "Duplicate key error"

- El documento ya existe en la base de datos
- El módulo actualiza automáticamente si el texto cambió
- Verificar índice único en campo `file`

### Ver Documentos Insertados

```python
# Verificar en MongoDB Compass
# O con Python:
python -c "from pymongo import MongoClient; client = MongoClient('tu_uri'); db = client['minsalud_db']; print(f'Total docs: {db.normativa.count_documents({})}')"
```

---

## 📊 Estadísticas y Monitoreo

El módulo proporciona estadísticas detalladas:

```
📊 RESUMEN DE CARGA A MONGODB
============================================================
✅ Nuevos documentos insertados: 150
🔄 Documentos actualizados: 5
⏭️  Documentos duplicados (sin cambios): 10
📁 Total en colección: 165
============================================================
```

---

## 🎯 Mejores Prácticas

### Desarrollo
- ✅ Usar MongoDB Atlas tier gratuito
- ✅ Permitir acceso desde cualquier IP (0.0.0.0/0)
- ✅ Usar archivo .env para credenciales
- ✅ NO subir .env a Git

### Producción
- ✅ Restringir IPs en whitelist
- ✅ Usar usuarios con permisos limitados
- ✅ Habilitar backup automático
- ✅ Usar SSL/TLS
- ✅ Monitorear uso de recursos

### Optimización
- ✅ Usar batch inserts (ya implementado)
- ✅ Crear índices apropiados (ya implementado)
- ✅ Verificar duplicados antes de insertar (ya implementado)
- ✅ Limitar tamaño de documentos (< 16 MB)

---

## 📞 Soporte Adicional

- **MongoDB Docs**: https://www.mongodb.com/docs/
- **MongoDB University**: https://university.mongodb.com/ (cursos gratuitos)
- **PyMongo Docs**: https://pymongo.readthedocs.io/

---

## ✅ Checklist de Configuración

- [ ] MongoDB instalado (local) o cuenta creada (Atlas)
- [ ] Cluster creado (Atlas) o servicio corriendo (local)
- [ ] Usuario de base de datos creado (Atlas)
- [ ] IP agregada a whitelist (Atlas)
- [ ] Connection string obtenido
- [ ] Archivo .env creado con credenciales
- [ ] PyMongo instalado (`pip install pymongo`)
- [ ] Conexión verificada (`python main.py --test-mongo`)
- [ ] Índices creados automáticamente
- [ ] Primera carga exitosa (`python main.py --only-mongo`)

---

**¡Listo para usar MongoDB con MinSalud Scraper!** 🎉
