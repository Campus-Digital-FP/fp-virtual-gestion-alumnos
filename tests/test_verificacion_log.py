# tests/test_resumen_final.py
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Importa la función que quieres testear
from utils.verificacion_log import extraer_resumen_final  # Ajusta el import según tu estructura

# Contenido simulado de un archivo .md válido
MD_CONTENT = """
## RESUMEN de acciones llevadas a cabo por este script:

- Alumnos existentes en moodle antes de ejecutar este programa: 100
- Alumnos existentes en moodle despues de ejecutar este programa: 102
- Alumnos creados por este script: 2
- Alumnos que NO es posible crear por este script: 0
- Alumnos reactivados por este script: 0
- Alumnos suspendidos por este script: 5
- Alumnos cuyo login ha sido modificado por este script: 1
- Alumnos cuyo email ha sido modificado por este script: 3
- Cantidad de matriculas hechas en modulos: 10
- Cantidad de matriculas reactivadas en modulos: 0
- Cantidad de matriculas suspendidas en modulos: 15
- Cantidad de matriculas borradas en tutorías: 1
- Cantidad de matriculas borradas en modulos: 0
- Cantidad de matriculas no hechas por no existir el curso destino: 2
- Cantidad de emails enviados: 0
- Cantidad de emails NO enviados: 3
"""

@pytest.fixture
def setup_md_files(tmp_path):
    # Crear archivos .md con fechas distintas
    (tmp_path / "2026_01_04_04_05_01_www.md").write_text(MD_CONTENT.replace("100", "90"))
    (tmp_path / "2026_01_05_04_05_01_www.md").write_text(MD_CONTENT)
    (tmp_path / "2026_01_03_04_05_01_www.md").write_text(MD_CONTENT.replace("100", "80"))
    return tmp_path

@patch("utils.verificacion_log.logger")
def test_extraer_resumen_final_usa_ultimo_archivo(mock_logger, setup_md_files):
    # Ejecutar la función
    resultado = extraer_resumen_final(str(setup_md_files))

    # Verificar que se usó el archivo más reciente
    mock_logger.info.assert_any_call("Archivo más reciente detectado: 2026_01_05_04_05_01_www.md")

    # Verificar que los valores extraídos son los correctos
    assert resultado["alumnos_antes"] == 100
    assert resultado["alumnos_creados"] == 2
    assert resultado["alumnos_suspendidos"] == 5
    assert resultado["emails_modificados"] == 3
    assert resultado["matriculas_no_hechas"] == 2