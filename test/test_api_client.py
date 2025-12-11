import pytest
from utils import api_client
from unittest.mock import Mock

def test_solicitar_datos_success(mock_requests, mock_env_vars):
    # Configurar mock de respuesta exitosa
    mock_response = Mock()
    mock_response.json.return_value = {"codigo": 0, "idSolicitud": 12345}
    mock_response.raise_for_status.return_value = None
    mock_requests.get.return_value = mock_response
    
    resultado = api_client.solicitar_datos("user", "pass")
    
    assert resultado["idSolicitud"] == 12345
    mock_requests.get.assert_called_once()

def test_solicitar_datos_error(mock_requests, mock_env_vars):
    mock_response = Mock()
    mock_response.json.return_value = {"codigo": -1, "mensaje": "Error"}
    mock_response.raise_for_status.return_value = None
    mock_requests.get.return_value = mock_response
    
    with pytest.raises(ValueError, match="Error en la solicitud inicial"):
        api_client.solicitar_datos("user", "pass")