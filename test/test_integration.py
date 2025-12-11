import pytest
import os

@pytest.mark.slow
@pytest.mark.skipif(
    not os.getenv("API_USER"),
    reason="Credenciales no configuradas"
)
def test_flujo_completo():
    """Test real contra la API (solo en CI/CD o manual)"""
    from utils import api_client
    
    resultado = main()
    assert resultado is True