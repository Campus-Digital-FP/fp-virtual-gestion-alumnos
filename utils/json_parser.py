import json
import os
from pathlib import Path
from logger_config import logger
from models import Registro
from .parser import parse_json

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def _extraer_numero(fichero: Path) -> int:
    """Extrae el número XXXX de estudiantes_XXXX.json"""
    return int(fichero.stem.split('_')[1])


def cargar_fichero_estudiantes() -> Registro:
    """
    Carga el primer fichero /data/estudiantes_XXXX.json que encuentre.
    :return: diccionario con los datos del fichero
    :raises FileNotFoundError: si no existe ningún fichero que encaje
    """
    
     # 1. Buscar todos los estudiantes_*.json
    candidatos = list(_DATA_DIR.glob("estudiantes_*.json"))
    if not candidatos:
        raise FileNotFoundError("No existe ningún fichero /data/estudiantes_XXXX.json")

    # 2. Quedarse con el de número mayor
    fichero_elegido = max(candidatos, key=_extraer_numero)
    logger.info("Cargando fichero de estudiantes...")

    # 3. Cargar contenido
    with fichero_elegido.open(encoding="utf-8") as f:
        logger.info("Fichero de estudiantes cargado correctamente.")
        datos = json.load(f)

    # 4. Borrar todos los .json si estamos en producción que pudiera haber
    # para evitar reutilizar datos antiguos.
    # En PREPRODUCCIÓN o TEST no se borran para facilitar las pruebas.
    if os.getenv("ENVIRONMENT") == "PRODUCCION":
        for f_json in _DATA_DIR.glob("*.json"):
            f_json.unlink(missing_ok=True)

    return parse_json(datos)
        

def procesaJsonEstudiantes(y, alumnos_sigad):
    """
    Procesa el fichero JSON obteniendo los alumnos y que estudian y los
    añade a alumnos_sigad
    """
    estudiantes=y["estudiantes"]
    # print( "type(estudiantes): ", type(estudiantes) ) # str
    estudiantesJson=json.loads(estudiantes)
    # print( "type(estudiantesJson: ",type(estudiantesJson) ) # dict

    fecha=estudiantesJson["fecha"]
    hora=estudiantesJson["hora"]
    alumnos=estudiantesJson["alumnos"]

    # print("fecha: " + str(fecha) + " y hora: " + str(hora) + " de creación del fichero")
    i = 0
    for alumno in alumnos:
        # print("i: ", i)
        # print("type(alumno): ", type(alumno) ) # dict
        idAlumno = alumno["idAlumno"]
        idTipoDocumento = alumno["idTipoDocumento"]
        documento = alumno["documento"]
        nombre = alumno["nombre"]
        apellido1 = alumno["apellido1"]
        apellido2 = alumno["apellido2"]
        emailSigad = alumno["email"] # este es el email de SIGAD
        centros = alumno["centros"]
        # print( "type(centros): ", type(centros) ) # list
        # print( "len(centros): ", len(centros) ) # 
        # creo el objeto
        miAlumno = Alumno(idAlumno, idTipoDocumento, documento, nombre, 
                apellido1, apellido2, emailSigad)
        # miAlumno.toText()
        #
        j=0
        for centro in centros:
            # print("  i: " + str(i) + ", j: " + str(j) + ", centro: " + str(centro) )
            # print("type(centro): ", type(centro) ) # dict

            codigoCentro = centro["codigoCentro"]
            centroo = centro["centro"]
            ciclos=centro["ciclos"]
            # print("ciclos: ", ciclos)
            # print("type(ciclos): ", type(ciclos) ) # str

            miCentro = Centro(codigoCentro, centroo)

            k = 0
            for ciclo in ciclos:
                # print("    i: ", i, ", j: ", j, ", k: ", k, ", ciclo: ", ciclo )
                # print("type(ciclo): ", type(ciclo) ) # dict
                
                idFicha = ciclo["idFicha"]
                codigoCiclo = ciclo["codigoCiclo"]
                cicloo = ciclo["ciclo"]
                siglasCiclo = ciclo["siglasCiclo"]
                modulos = ciclo["modulos"]

                miCiclo = Ciclo(idFicha, codigoCiclo, cicloo, siglasCiclo)

                l = 0
                for modulo in modulos:
                    #
                    idMateria = modulo["idMateria"]
                    moduloo = modulo["modulo"]
                    siglasModulo = modulo["siglasModulo"]
                    #
                    miModulo = Modulo(idMateria, moduloo, siglasModulo)
                    #
                    miCiclo.addModulo(miModulo)
                #
                miCentro.addCiclo(miCiclo)
            # Add miCentro to miAlumno
            miAlumno.addCentro(miCentro)
        # Add miAlumno to alumnos_sigad
        alumnos_sigad.append(miAlumno)
    #
    # End of procesaJsonEstudiantes
    #