"""Configuración centralizada del registro de eventos y errores."""
import logging
from pathlib import Path

RUTA_LOG = Path(__file__).resolve().parent / "logs.txt"

def obtener_logger():
    logger = logging.getLogger("SoftwareFJ")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        archivo = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        archivo.setFormatter(formato)
        consola = logging.StreamHandler()
        consola.setFormatter(formato)
        logger.addHandler(archivo)
        logger.addHandler(consola)
    return logger

logger = obtener_logger()
