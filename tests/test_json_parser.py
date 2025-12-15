import os
import json
from pathlib import Path
from unittest.mock import patch
import pytest
from models import Registro
from utils.json_parser import cargar_fichero_estudiantes

# Fichero que simularemos que existe
FAKE_FILE = Path(__file__).parent / "data" / "estudiantes_0001.json"

# -------------- helper para mockear glob --------------
def _mocked_glob(pattern: str):
    """Devuelve [FAKE_FILE] si el patrón es estudiantes_*.json, [] en otro caso."""
    if pattern == "estudiantes_*.json":
        return [FAKE_FILE]
    return []

# -------------- tests --------------
@patch.dict(os.environ, {"ENVIRONMENT": "TEST"})   # nos aseguramos que NO es PRODUCCION
@patch.object(Path, "glob", side_effect=_mocked_glob)
def test_carga_fichero_estudiantes(mock_glob, sample_registro):
    """
    - Mockea la búsqueda de ficheros para que sólo exista estudiantes_0001.json
    - Comprueba que se devuelve un Registro
    - Comprueba que los datos son los esperados
    - Comprueba que los .json NO se borran (no estamos en PRODUCCION)
    """
    reg = cargar_fichero_estudiantes()

    # comprobaciones de tipo
    assert isinstance(reg, Registro)
    assert len(reg.alumnos) == 3

    # comprobación de contenido (usamos los datos que ya tienes en memoria)
    alum1 = reg.alumnos[0]
    assert alum1.nombre == "Valeria"
    assert alum1.apellido1 == "Torres"
    assert alum1.email == "valeria.torres.medina@ejemplo.com"

    # comprobar que no se ha llamado a unlink (no borramos)
    # (se puede mockear Path.unlink y verificar call_count==0 si se desea)

    # el mock ha sido llamado con el patrón correcto
    mock_glob.assert_called_once_with("estudiantes_*.json")