import logging
import logging.handlers
import os
from pathlib import Path

def setup_logger(name: str = "gestion-alumnos") -> logging.Logger:
    """
    Configura el logger con la carpeta 'log/' en la raíz del proyecto
    """
    # Obtener directorio raíz del proyecto (donde está logger_config.py)
    project_root = Path(__file__).parent.resolve()
    log_dir = project_root / "log"
    
    # Crear carpeta log con permisos 755 (si no existe)
    log_dir.mkdir(mode=0o755, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Formato detallado
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler principal (DEBUG y superior)
    main_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    main_handler.setLevel(logging.DEBUG)
    main_handler.setFormatter(formatter)
    
    # Handler de errores (ERROR y superior)
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / "error.log",
        maxBytes=5*1024*1024,   # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # Añadir handlers
    logger.addHandler(main_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger