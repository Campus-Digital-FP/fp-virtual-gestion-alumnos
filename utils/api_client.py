import requests
import json
import time
import os
from datetime import datetime
from logger_config import logger

BASE_URL = os.getenv("API_BASE_URL", "https://aplicaciones.aragon.es/pcrpe/services/alumnosFPDistancia")

"""
    Realiza la primera solicitud y devuelve el JSON con el idSolicitud.
"""
def solicitar_datos(usuario: str, password: str) -> dict:
    
    anio_actual = datetime.now().year          
    url = f"{BASE_URL}/solicitud/{anio_actual}"    
    logger.info("URL -> %s", url)  
    headers = {
        "Accept": "application/json",
        "User-Agent": "fpdistancia-client/1.0",
        "usuario": usuario,
        "password": password
    }

    logger.info("🔗 Realizando solicitud inicial a %s...", url)
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    if data.get("codigo") != 0:
        raise ValueError(f"⚠️ Error en la solicitud inicial: {data}")

    logger.info("✅ idSolicitud recibido: %s", data["idSolicitud"])
    return data

"""
    Segunda solicitud: obtiene los datos de estudiantes.
    Reintenta si la respuesta indica que el fichero aún no está listo (codigo: -1).
"""
def obtener_estudiantes(usuario: str, password: str, id_solicitud: int,
                        reintentos: int = 5, espera: int = 10) -> dict:
    
    url = f"{BASE_URL}/fichero/{id_solicitud}"
    headers = {
        "Accept": "application/json",
        "User-Agent": "fpdistancia-client/1.0",
        "usuario": usuario,
        "password": password
    }

    for intento in range(1, reintentos + 1):
        logger.info(f"📡 ({intento}/{reintentos}) Solicitando fichero de estudiantes...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        codigo = data.get("codigo", None)

        # ✅ Caso correcto
        if codigo == 0:
            estudiantes_json = json.loads(data["estudiantes"])
            logger.info(f"✅ Fichero recibido correctamente con {len(estudiantes_json.get('alumnos', []))} registros")
            return estudiantes_json

        # ⚠️ Caso transitorio: fichero aún no preparado
        if codigo == -1:
            print(f"⚠️ El fichero aún no está listo: {data.get('mensaje')}")
            if intento < reintentos:
                logger.info("⏳ Reintentando en {espera} segundos...")
                time.sleep(espera)
                continue
            else:
                raise TimeoutError("❌ Se agotaron los reintentos. Inténtelo más tarde.")

        # ❌ Caso de error definitivo
        raise ValueError(f"Error en la solicitud: {data.get('mensaje', 'Desconocido')}")

    raise RuntimeError("❌ Error inesperado: no se obtuvo respuesta válida.")

def main():
    logger.info("=== api_client.py Conexión con FP Distancia Aragón ===")
    
    usuario = os.getenv("API_USER")
    password = os.getenv("API_PASSWORD")
    if not usuario or not password:
        logger.error("Faltan API_USER y/o API_PASSWORD")
        return         

    try:
        # 1️⃣ Solicitud inicial
        datos = solicitar_datos(usuario, password)
        id_solicitud = datos["idSolicitud"]
        
        # 🕐 Espera de 3 segundos antes de pedir los datos
        print("⏱ Esperando 3 segundos antes de recuperar los datos...")
        time.sleep(3)

        # 2️⃣ Solicitud de estudiantes con reintento
        estudiantes = obtener_estudiantes(usuario, password, id_solicitud)

        # 3️⃣ Guardar resultados
        nombre_fichero = f"estudiantes_{id_solicitud}.json"
        with open(nombre_fichero, "w", encoding="utf-8") as f:
            json.dump(estudiantes, f, ensure_ascii=False, indent=2)

        logger.info(f"\n✅ Datos guardados correctamente en {nombre_fichero}")       

    except Exception as e:
        logger.info(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()