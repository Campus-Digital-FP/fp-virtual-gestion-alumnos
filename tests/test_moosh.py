# tests/test_moosh.py
"""
Tests para utils/moosh.py
"""
import subprocess
import pytest
from unittest.mock import patch, MagicMock
from utils.moosh import run_moosh_command, run_command


@pytest.fixture
def moodle_dict():
    """Datos mínimos para el parámetro moodle."""
    return {"container_name": "moodle_container"}


class TestRunMooshCommand:
    """run_moosh_command"""

    @patch("utils.moosh.subprocess.run")
    def test_run_moosh_command_capture_ok(self, mock_run, moodle_dict):
        """Captura stdout cuando capture=True y el comando finaliza."""
        mock_run.return_value = MagicMock(stdout="moosh output", returncode=0)

        out = run_moosh_command(moodle_dict, "moosh user-list", capture=True)

        mock_run.assert_called_once_with(
            "docker exec moodle_container moosh user-list",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert out == "moosh output"

    @patch("utils.moosh.subprocess.run")
    def test_run_moosh_command_no_capture(self, mock_run, moodle_dict):
        """Sin captura: subprocess.run sin capture_output."""
        run_moosh_command(moodle_dict, "moosh cache-clear", capture=False)

        mock_run.assert_called_once_with(
            "docker exec moodle_container moosh cache-clear",
            shell=True,
            timeout=10,
        )

    @patch("utils.moosh.subprocess.run")
    def test_run_moosh_command_timeout(self, mock_run, moodle_dict):
        """TimeoutExpired → retorna cadena vacía y log."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="moosh", timeout=10)

        out = run_moosh_command(moodle_dict, "moosh heavy-task", capture=True, timeout=5)

        assert out == ""
        # se puede chequear log si se desa con caplog fixture


class TestRunCommand:
    """run_command"""

    @patch("utils.moosh.subprocess.run")
    def test_run_command_capture(self, mock_run):
        """Captura stdout."""
        mock_run.return_value.stdout = "shell output"

        result = run_command("echo hello", capture=True)

        mock_run.assert_called_once_with(
            "echo hello",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result == "shell output"

    @patch("utils.moosh.subprocess.run")
    def test_run_command_no_capture(self, mock_run):
        """Ejecución simple sin captura."""
        run_command("ls /tmp", capture=False)

        mock_run.assert_called_once_with(
            "ls /tmp",
            shell=True,
            timeout=10,
        )

    @patch("utils.moosh.subprocess.run")
    def test_run_command_timeout(self, mock_run):
        """Timeout → retorna vacío."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="sleep", timeout=10)

        out = run_command("sleep 20", capture=True, timeout=2)

        assert out == ""