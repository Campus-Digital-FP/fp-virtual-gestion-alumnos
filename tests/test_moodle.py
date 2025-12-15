# test_moodle.py
import io
import unittest
from unittest.mock import patch
from moodle import get_moodle  # Asegúrate de que moodle.py esté en el mismo directorio o ajusta el import


class TestGetMoodle(unittest.TestCase):

    @patch("os.popen")
    def test_get_moodle_with_predesarrollo(self, mock_popen):
        # Simulamos la salida exacta de `docker ps | grep predesarrollo`
        mock_output = """7c13b91c0866   cateduac/moodle:4.1.3-nginx-fpm-unoconv              "docker-entrypoint.s…"   13 days ago      Up 13 days      80/tcp, 9000/tcp                                                               predesarrollofpvirtualaragones-moodle-1
d9f4dd854fc7   redis                                                "docker-entrypoint.s…"   13 days ago      Up 13 days      6379/tcp                                                                       predesarrollofpvirtualaragones-redis-1
06cdf526a79e   nginx:latest                                         "/docker-entrypoint.…"   13 days ago      Up 13 days      80/tcp                                                                         predesarrollofpvirtualaragones-web-1"""
        mock_popen.return_value = io.StringIO(mock_output)

        resultado = get_moodle("predesarrollo")

        esperado = [
            {
                "url": "predesarrollofpvirtualaragones-moodle-1.fpvirtualaragon.es",
                "container_name": "predesarrollofpvirtualaragones-moodle-1"
            }
        ]

        self.assertEqual(resultado, esperado)


if __name__ == "__main__":
    unittest.main()