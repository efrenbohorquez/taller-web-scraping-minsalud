"""
Script para consultar documentos en MongoDB Atlas
Permite ver y buscar documentos de MinSalud
"""

from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME
from datetime import datetime
import json

def conectar_mongodb():
    """Conectar a MongoDB Atlas"""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Verificar conexión
        client.server_info()
        print("✅ Conectado a MongoDB Atlas\n")
        return collection
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        return None

def mostrar_estadisticas(collection):
    """Mostrar estadísticas de la colección"""
    print("="*60)
    print("📊 ESTADÍSTICAS DE LA COLECCIÓN")
    print("="*60)
    
    total = collection.count_documents({})
    print(f"📁 Total de documentos: {total}")
    
    # Contar por método de extracción
    pipeline = [
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ]
    
    metodos = list(collection.aggregate(pipeline))
    print(f"\n📄 Documentos por método de extracción:")
    for metodo in metodos:
        print(f"   - {metodo['_id']}: {metodo['count']}")
    
    print("="*60 + "\n")

def listar_documentos(collection, limit=10):
    """Listar documentos con información resumida"""
    print("="*60)
    print(f"📋 LISTA DE DOCUMENTOS (primeros {limit})")
    print("="*60)
    
    documentos = collection.find().limit(limit)
    
    for i, doc in enumerate(documentos, 1):
        print(f"\n{i}. {doc.get('file', 'Sin nombre')}")
        print(f"   📅 Fecha: {doc.get('timestamp', 'N/A')}")
        print(f"   🔧 Método: {doc.get('method', 'N/A')}")
        print(f"   📝 Tamaño texto: {len(doc.get('text', ''))} caracteres")
        texto_preview = doc.get('text', '')[:100].replace('\n', ' ')
        print(f"   📖 Preview: {texto_preview}...")
    
    print("\n" + "="*60 + "\n")

def buscar_por_texto(collection, termino):
    """Buscar documentos por texto"""
    print("="*60)
    print(f"🔍 BÚSQUEDA: '{termino}'")
    print("="*60)
    
    # Búsqueda de texto completo
    resultados = collection.find(
        {"$text": {"$search": termino}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(5)
    
    count = 0
    for doc in resultados:
        count += 1
        print(f"\n{count}. {doc.get('file', 'Sin nombre')}")
        print(f"   📊 Relevancia: {doc.get('score', 0):.2f}")
        print(f"   📅 Fecha: {doc.get('timestamp', 'N/A')}")
        
        # Encontrar contexto del término
        texto = doc.get('text', '')
        termino_lower = termino.lower()
        pos = texto.lower().find(termino_lower)
        
        if pos != -1:
            inicio = max(0, pos - 50)
            fin = min(len(texto), pos + len(termino) + 50)
            contexto = texto[inicio:fin].replace('\n', ' ')
            print(f"   📖 Contexto: ...{contexto}...")
    
    if count == 0:
        print("❌ No se encontraron resultados")
    
    print("\n" + "="*60 + "\n")

def ver_documento_completo(collection, nombre_archivo):
    """Ver un documento completo por nombre de archivo"""
    print("="*60)
    print(f"📄 DOCUMENTO COMPLETO")
    print("="*60)
    
    doc = collection.find_one({"file": nombre_archivo})
    
    if doc:
        print(f"\n📁 Archivo: {doc.get('file', 'N/A')}")
        print(f"📅 Timestamp: {doc.get('timestamp', 'N/A')}")
        print(f"🔧 Método: {doc.get('method', 'N/A')}")
        print(f"📤 Subido: {doc.get('_uploaded_at', 'N/A')}")
        print(f"📂 Origen: {doc.get('_source_file', 'N/A')}")
        print(f"\n{'='*60}")
        print("📝 CONTENIDO:")
        print(f"{'='*60}\n")
        print(doc.get('text', 'Sin contenido'))
    else:
        print(f"❌ No se encontró el documento: {nombre_archivo}")
    
    print("\n" + "="*60 + "\n")

def menu_interactivo():
    """Menú interactivo para consultas"""
    collection = conectar_mongodb()
    
    if not collection:
        return
    
    while True:
        print("\n" + "="*60)
        print("🗄️  CONSULTA MONGODB - MINSALUD")
        print("="*60)
        print("1. Ver estadísticas")
        print("2. Listar documentos")
        print("3. Buscar por texto")
        print("4. Ver documento completo")
        print("5. Salir")
        print("="*60)
        
        opcion = input("\n👉 Selecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            mostrar_estadisticas(collection)
        
        elif opcion == "2":
            try:
                limit = input("¿Cuántos documentos mostrar? (default: 10): ").strip()
                limit = int(limit) if limit else 10
                listar_documentos(collection, limit)
            except ValueError:
                print("❌ Número inválido, usando 10")
                listar_documentos(collection, 10)
        
        elif opcion == "3":
            termino = input("🔍 Ingresa término de búsqueda: ").strip()
            if termino:
                buscar_por_texto(collection, termino)
            else:
                print("❌ Debes ingresar un término")
        
        elif opcion == "4":
            nombre = input("📁 Ingresa nombre del archivo: ").strip()
            if nombre:
                ver_documento_completo(collection, nombre)
            else:
                print("❌ Debes ingresar un nombre de archivo")
        
        elif opcion == "5":
            print("\n👋 ¡Hasta luego!\n")
            break
        
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    # Modo interactivo por defecto
    menu_interactivo()
