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

def _campos_csv_para(filepath: str) -> List[str]:
    """
    Devuelve los nombres de las columnas que tendrá el archivo CSV
    Determina los campos que se usarán en el CSV.

    En este proyecto solo manejamos 'autores.csv'.

    Args:
        filepath: Ruta del archivo CSV.

    Returns:
        List[str]: Lista de nombres de columnas.
    """
    nombre = os.path.basename(filepath).lower()
    if nombre.endswith("autores.csv"):
        return CAMPOS_AUTORES
    # Fallback genérico: si no es autores.csv, intentamos no fallar.
    return CAMPOS_AUTORES


def _escritura_atomica(path_destino: str, contenido: str, modo_binario: bool = False) \
        -> None:
    """ Escribe un archivo de forma segura.
    Primero crea un archivo temporal y luego lo reemplaza por el final.
    Así evitamos errores si algo falla durante la escritura

    Crea un archivo temporal en el mismo directorio, escribe y reemplaza.

    Args:
        path_destino: Ruta del archivo destino.
        contenido: Contenido a escribir.
        modo_binario: Indica si se escribe en binario.

    Returns:
        None
    """
    _asegurar_directorio(path_destino)
    directorio = os.path.dirname(os.path.abspath(path_destino)) or "."
    suffix = ".tmpjson" if _es_json(path_destino) else ".tmpcsv"
    mode = "wb" if modo_binario else "w"
    encoding = None if modo_binario else "utf-8"

    with tempfile.NamedTemporaryFile(mode=mode, delete=False, dir=directorio,
                                     suffix=suffix, encoding=encoding) as tmp:
        tmp.write(contenido)
        tmp_path = tmp.name

    os.replace(tmp_path, path_destino)


