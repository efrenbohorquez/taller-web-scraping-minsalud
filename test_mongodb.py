"""
Script de prueba para verificar y configurar MongoDB
"""
import sys
import os
from pathlib import Path

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')

sys.path.insert(0, str(Path(__file__).parent / "src"))

from scraper import MinSaludScraper
import json

def test_pymongo_instalado():
    """Verificar si PyMongo está instalado"""
    print("\n" + "="*60)
    print("🧪 TEST 1: Verificar PyMongo")
    print("="*60)
    
    try:
        import pymongo
        print(f"✅ PyMongo instalado - Versión: {pymongo.__version__}")
        return True
    except ImportError:
        print("❌ PyMongo NO instalado")
        print("\n💡 Instalar con: pip install pymongo")
        return False

def test_configuracion_mongo():
    """Verificar configuración de MongoDB"""
    print("\n" + "="*60)
    print("🧪 TEST 2: Verificar Configuración")
    print("="*60)
    
    from config import MONGO_URI, DB_NAME, COLLECTION_NAME
    
    print(f"📝 MONGO_URI: {MONGO_URI[:50]}...")
    print(f"📝 Base de datos: {DB_NAME}")
    print(f"📝 Colección: {COLLECTION_NAME}")
    
    # Advertencias sobre configuración
    if MONGO_URI == "mongodb://localhost:27017/":
        print("\n⚠️  Usando MongoDB local (localhost)")
        print("   Asegúrate de que MongoDB está corriendo localmente")
    elif "mongodb+srv://" in MONGO_URI:
        print("\n✅ Configurado para MongoDB Atlas")
    
    return True

def test_conexion_mongodb():
    """Probar conexión a MongoDB"""
    print("\n" + "="*60)
    print("🧪 TEST 3: Probar Conexión")
    print("="*60)
    
    scraper = MinSaludScraper()
    return scraper.verificar_conexion_mongodb()

def test_operaciones_basicas():
    """Probar operaciones básicas de MongoDB"""
    print("\n" + "="*60)
    print("🧪 TEST 4: Operaciones Básicas")
    print("="*60)
    
    try:
        from pymongo import MongoClient
        from config import MONGO_URI, DB_NAME, COLLECTION_NAME
        
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Test 1: Insertar documento de prueba
        test_doc = {
            'file': 'test_documento.pdf',
            'timestamp': '2025-10-07T00:00:00',
            'text': 'Este es un documento de prueba',
            'method': 'TEST',
            '_test': True
        }
        
        print("📝 Insertando documento de prueba...")
        result = collection.insert_one(test_doc)
        print(f"✅ Documento insertado con ID: {result.inserted_id}")
        
        # Test 2: Buscar documento
        print("\n🔍 Buscando documento de prueba...")
        found = collection.find_one({'_test': True})
        if found:
            print(f"✅ Documento encontrado: {found['file']}")
        
        # Test 3: Actualizar documento
        print("\n🔄 Actualizando documento de prueba...")
        collection.update_one(
            {'_test': True},
            {'$set': {'text': 'Texto actualizado'}}
        )
        print("✅ Documento actualizado")
        
        # Test 4: Eliminar documento de prueba
        print("\n🗑️  Eliminando documento de prueba...")
        result = collection.delete_one({'_test': True})
        print(f"✅ Documento eliminado: {result.deleted_count}")
        
        client.close()
        
        print("\n✅ Todas las operaciones básicas funcionan correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en operaciones: {e}")
        return False

def test_indices():
    """Verificar índices en la colección"""
    print("\n" + "="*60)
    print("🧪 TEST 5: Verificar Índices")
    print("="*60)
    
    try:
        from pymongo import MongoClient
        from config import MONGO_URI, DB_NAME, COLLECTION_NAME
        
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        indices = collection.list_indexes()
        
        print("📑 Índices existentes:")
        for idx in indices:
            print(f"  - {idx['name']}: {idx['key']}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando índices: {e}")
        return False

def mostrar_guia_configuracion():
    """Mostrar guía de configuración de MongoDB"""
    print("\n" + "="*60)
    print("📚 GUÍA DE CONFIGURACIÓN DE MONGODB")
    print("="*60)
    
    print("""
┌─────────────────────────────────────────────────────────┐
│  OPCIÓN 1: MongoDB Local                                │
└─────────────────────────────────────────────────────────┘

1. Instalar MongoDB Community:
   https://www.mongodb.com/try/download/community

2. Iniciar MongoDB:
   Windows: mongod --dbpath C:\\data\\db
   
3. Configurar en config.py:
   MONGO_URI = "mongodb://localhost:27017/"

┌─────────────────────────────────────────────────────────┐
│  OPCIÓN 2: MongoDB Atlas (Cloud)                        │
└─────────────────────────────────────────────────────────┘

1. Crear cuenta gratuita:
   https://www.mongodb.com/cloud/atlas/register

2. Crear cluster gratuito (M0)

3. Crear usuario de base de datos:
   - Database Access → Add New Database User
   - Usuario: minsalud_user
   - Password: (genera uno seguro)

4. Configurar IP whitelist:
   - Network Access → Add IP Address
   - Agregar: 0.0.0.0/0 (permitir todo - solo para desarrollo)

5. Obtener connection string:
   - Clusters → Connect → Connect your application
   - Copiar la URI

6. Configurar en config.py o .env:
   MONGO_URI = "mongodb+srv://usuario:password@cluster.mongodb.net/"
   DB_NAME = "minsalud_db"
   COLLECTION_NAME = "normativa"

┌─────────────────────────────────────────────────────────┐
│  VARIABLES DE ENTORNO (.env)                            │
└─────────────────────────────────────────────────────────┘

Crear archivo .env en la raíz del proyecto:

MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/
MONGO_DB_NAME=minsalud_db
MONGO_COLLECTION_NAME=normativa

┌─────────────────────────────────────────────────────────┐
│  VERIFICAR CONEXIÓN                                     │
└─────────────────────────────────────────────────────────┘

python main.py --test-mongo
python test_mongodb.py

""")

def main():
    print("\n" + "🧪"*30)
    print(" "*15 + "SUITE DE PRUEBAS - MONGODB")
    print("🧪"*30 + "\n")
    
    # Test 1: PyMongo instalado
    if not test_pymongo_instalado():
        print("\n❌ PyMongo no está instalado. No se pueden continuar las pruebas.")
        mostrar_guia_configuracion()
        return
    
    # Test 2: Configuración
    test_configuracion_mongo()
    
    # Test 3: Conexión
    conexion_ok = test_conexion_mongodb()
    
    if not conexion_ok:
        print("\n❌ No se pudo conectar a MongoDB")
        mostrar_guia_configuracion()
        return
    
    # Test 4: Operaciones básicas
    test_operaciones_basicas()
    
    # Test 5: Índices
    test_indices()
    
    # Resumen final
    print("\n" + "="*60)
    print("✅ PRUEBAS DE MONGODB COMPLETADAS")
    print("="*60)
    print("\n💡 Para cargar datos a MongoDB:")
    print("   python main.py --only-mongo")
    print("\n💡 Para ver ayuda completa:")
    print("   python main.py --help")

if __name__ == "__main__":
    main()
