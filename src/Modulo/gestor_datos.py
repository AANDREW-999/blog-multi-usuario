# -- coding: utf-8 --
"""
Módulo de Persistencia de Datos.
archivo que se encarga de guardar y leer datos
"""
import csv  # Lectura/escritura de archivos CSV
import json  # Manejo de estructuras y archivos JSON
import os  # Orabajar con rutas y carpetas
import tempfile  # Crear archivos temporales (para guardar datos de forma segura)
from io import StringIO #StringIO Guardar texto en memoria antes de escribirlo en el disco
from typing import Any, Dict, List  # Anotaciones de tipos para claridad

# Constantes de cabeceras para CSV de autores
CAMPOS_AUTORES = ["id_autor", "nombre_autor", "email", "password_hash"]



def _es_csv(filepath: str) -> bool:
    """verifica si el archivotermina en archivo CSV.

    Args:
        filepath: Ruta del archivo.

    Returns:
        bool: True si termina en .csv; False en caso contrario.
    """
    return filepath.lower().endswith(".csv")


def _es_json(filepath: str) -> bool:
    """verifica si la ruta corresponde a un archivo JSON.

    Args:
        filepath: Ruta del archivo.

    Returns:
        bool: True si termina en .json; False en caso contrario.
    """
    return filepath.lower().endswith(".json")


def _asegurar_directorio(filepath: str) -> None:
    """Crea la carpeta donde se guarda el archivo si no existe todavia.

    Args:
        filepath: Ruta del archivo objetivo.

    Returns:
        None
    """
    directorio = os.path.dirname(os.path.abspath(filepath))
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio, exist_ok=True)

