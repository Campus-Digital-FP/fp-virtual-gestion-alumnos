import pytest
from unittest.mock import Mock, patch
import logging

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Simula variables de entorno"""
    monkeypatch.setenv("API_USER", "test_user")
    monkeypatch.setenv("API_PASSWORD", "test_pass")
    monkeypatch.setenv("API_BASE_URL", "https://test.api.com")

@pytest.fixture
def mock_requests():
    """Mock del módulo requests"""
    with patch('utils.api_client.requests') as mock_req:
        yield mock_req

@pytest.fixture
def setup_test_logger():
    """Logger para tests"""
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)
    return logger