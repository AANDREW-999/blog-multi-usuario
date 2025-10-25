"""
Módulo de Lógica de Negocio (Modelo) — Sistema de Blog Multi-usuario.
"""
from __future__ import annotations  # Anotaciones diferidas para tipos

import re  #validaremail


ErrorDeDominio = Exception
ValidacionError = ErrorDeDominio
EmailDuplicado = ErrorDeDominio
AutorNoEncontrado = ErrorDeDominio
PostNoEncontrado = ErrorDeDominio
AccesoNoAutorizado = ErrorDeDominio


_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
def _ahora_str() -> str:
    """Obtiene la fecha y hora actual formateada.

    Returns:
        str: Marca de tiempo en formato 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _es_str_no_vacio(valor: Any) -> bool:
    """Indica si el valor es una cadena no vacía tras strip().

    Args:
        valor: Valor a evaluar.

    Returns:
        bool: True si es str y no está vacío; False en caso contrario.
    """
    return isinstance(valor, str) and valor.strip() != ""

def _validar_email(email: str) -> None:
    """Valida el formato del email.

       Args:
           email: Correo a validar.

       Raises:
           ValidacionError: Si el email está vacío o no cumple el formato.
       """
    if not _es_str_no_vacio(email) or not _EMAIL_RE.match(email):
        raise ValidacionError("El email no tiene un formato válido.")
def _normalizar_tags(tags: Sequence[str]) -> List[str]:
    """Normaliza y deduplica tags preservando el orden.

       Convierte a minúsculas, aplica strip() y elimina duplicados.

       Args:
           tags: Secuencia de cadenas (tags).

       Returns:
           List[str]: Lista de tags normalizados sin duplicados.

       Raises:
           ValidacionError: Si algún elemento no es cadena.
       """
    vistos = set()
    normalizados: List[str] = []
    for t in tags:
        if not isinstance(t, str):
            raise ValidacionError("Todos los tags deben ser cadenas de texto.")
        tt = t.strip().lower()
        if tt and tt not in vistos:
            vistos.add(tt)
            normalizados.append(tt)
    return normalizados

def _parsear_tags(tags: Any) -> List[str]:
    """Convierte la entrada de tags a una lista normalizada.

        Admite lista/tupla de strings o una cadena separada por comas.

        Args:
            tags: Lista/tupla de strings, cadena separada por comas o None.

        Returns:
            List[str]: Lista de tags normalizados.

        Raises:
            ValidacionError: Si el formato no es soportado.
        """
    if tags is None:
        return []
    if isinstance(tags, (list, tuple)):
        return _normalizar_tags(list(tags))
    if isinstance(tags, str):
        separados = [p.strip() for p in tags.split(",")]
        return _normalizar_tags(separados)
    raise ValidacionError("Formato de 'tags' no soportado. Use lista o cadena separada "
                          "por comas.")

def _generar_id(items: List[Dict[str, Any]], clave_id: str) -> int:
    """Genera un ID entero autoincremental.

    Busca el máximo valor de 'clave_id' y retorna el siguiente.

    Args:
        items: Lista de diccionarios fuente.
        clave_id: Nombre de la clave que contiene el ID.

    Returns:
        int: ID siguiente (1 si la lista está vacía o inválida).
    """
    if not items:
        return 1
    try:
        max_id = max(int(it.get(clave_id, 0)) for it in items)
    except ValueError:
        max_id = 0
    return max_id + 1
def _generar_id_comentario(post: Dict[str, Any]) -> int:
    """Genera un ID autoincremental para comentarios de un post.

    Args:
        post: Diccionario del post (con su lista 'comentarios').

    Returns:
        int: Siguiente ID de comentario.
    """
    comentarios = post.get("comentarios") or []
    if not comentarios:
        return 1
    try:
        max_id = max(int(c.get("id_comentario", 0)) for c in comentarios)
    except ValueError:
        max_id = 0
    return max_id + 1


def crear_autor(autores_filepath: str, nombre_autor: str, email: str, password_hash: str
= "") -> Dict[str, Any]:
    """Crea un nuevo autor.

        Valida el email y su unicidad, y persiste el registro en CSV.

        Args:
            autores_filepath: Ruta al CSV de autores.
            nombre_autor: Nombre a mostrar del autor.
            email: Correo electrónico único.
            password_hash: Hash de la contraseña del autor (opcional).

        Returns:
            Dict[str, Any]: Autor creado.

        Raises:
            ValidacionError: Si faltan datos o el formato es inválido.
            EmailDuplicado: Si el email ya existe.
        """
    if not _es_str_no_vacio(nombre_autor):
        raise ValidacionError("El nombre del autor es obligatorio.")
    _validar_email(email)

    autores = gestor_datos.cargar_datos(autores_filepath)

    if any(a.get("email", "").strip().lower() == email.strip().lower()
           for a in autores):
        raise EmailDuplicado(f"El email '{email}' ya se encuentra registrado.")

    nuevo_id = _generar_id(autores, "id_autor")
    autor = {
        "id_autor": str(nuevo_id),
        "nombre_autor": nombre_autor.strip(),
        "email": email.strip().lower(),
        "password_hash": str(password_hash or "").strip(),
    }
    autores.append(autor)
    gestor_datos.guardar_datos(autores_filepath, autores)
    return autor
def leer_todos_los_autores(autores_filepath: str) -> \
        (List)[Dict[str, Any]]:
    """Obtiene la lista completa de autores.

        Args:
            autores_filepath: Ruta al CSV de autores.

        Returns:
            List[Dict[str, Any]]: Lista de autores.
        """
    return gestor_datos.cargar_datos(autores_filepath)
def buscar_autor_por_id(autores_filepath: str, id_autor: str | int) \
        -> Optional[Dict[str, Any]]:
    """Busca un autor por su ID.

       Args:
           autores_filepath: Ruta al CSV de autores.
           id_autor: ID del autor.

       Returns:
           Optional[Dict[str, Any]]: Autor encontrado o None.
       """
    autores = gestor_datos.cargar_datos(autores_filepath)
    id_str = str(id_autor)
    for a in autores:
        if a.get("id_autor") == id_str:
            return a
    return None
def buscar_autor_por_email(autores_filepath: str, email: str) \
        -> Optional[Dict[str, Any]]:
    """Busca un autor por email (insensible a mayúsculas).

       Args:
           autores_filepath: Ruta al CSV de autores.
           email: Correo a buscar.

       Returns:
           Optional[Dict[str, Any]]: Autor encontrado o None.

       Raises:
           ValidacionError: Si el email no es válido.
       """
    _validar_email(email)
    autores = gestor_datos.cargar_datos(autores_filepath)
    email_l = email.strip().lower()
    for a in autores:
        if a.get("email", "").strip().lower() == email_l:
            return a
    return None
def actualizar_autor(
    autores_filepath: str,
    id_autor: str | int,
    datos_nuevos: Dict[str, Any],
) -> Dict[str, Any]:
    """Actualiza campos de un autor.

       Reglas:
       - Si se cambia el email, validar formato y unicidad.
       - Convierte todos los valores a str para consistencia.

       Args:
           autores_filepath: Ruta al CSV de autores.
           id_autor: ID del autor a actualizar.
           datos_nuevos: Campos a modificar (nombre_autor, email, password_hash).

       Returns:
           Dict[str, Any]: Autor actualizado.

       Raises:
           AutorNoEncontrado: Si el autor no existe.
           EmailDuplicado: Si el nuevo email ya está en uso.
           ValidacionError: Si algún campo es inválido.
       """
    autores = gestor_datos.cargar_datos(autores_filepath)
    id_str = str(id_autor)

    idx = -1
    for i, a in enumerate(autores):
        if a.get("id_autor") == id_str:
            idx = i
            break
    if idx == -1:
        raise AutorNoEncontrado(f"No existe autor con id_autor='{id_str}'.")

    autor = dict(autores[idx])  # copia

    if "nombre_autor" in datos_nuevos:
        if not _es_str_no_vacio(datos_nuevos["nombre_autor"]):
            raise ValidacionError("El nombre del autor no puede estar vacío.")
        autor["nombre_autor"] = str(datos_nuevos["nombre_autor"]).strip()

    if "email" in datos_nuevos:
        nuevo_email = str(datos_nuevos["email"]).strip().lower()
        _validar_email(nuevo_email)
        # verificar unicidad
        for a in autores:
            if (a.get("id_autor") != id_str and a.get("email", "").strip().lower()
                    == nuevo_email):
                raise EmailDuplicado(f"El email '{nuevo_email}"
                                     f"' ya está en uso por otro autor.")
        autor["email"] = nuevo_email

    if "password_hash" in datos_nuevos:
        autor["password_hash"] = str(datos_nuevos["password_hash"] or "").strip()

    autores[idx] = autor
    gestor_datos.guardar_datos(autores_filepath, autores)
    return autor

def eliminar_autor(autores_filepath: str, id_autor: str | int) -> bool:
    pass
def crear_post(
        posts_filepath: str,
        id_autor_en_sesion: str | int,
        titulo: str,
        contenido: str,
        tags: Any,
        **opciones,
) -> Dict[str, Any]:
    pass
def leer_todos_los_posts(posts_filepath: str) -> List[Dict[str, Any]]:
    pass
def listar_posts_por_autor(posts_filepath: str, id_autor: str | int) \
        -> List[Dict[str, Any]]:
    pass
def buscar_posts_por_tag(posts_filepath: str, tag: str) -> List[Dict[str, Any]]:
    pass
def buscar_post_por_id(posts_filepath: str, id_post: str | int) \
        -> Optional[Dict[str, Any]]:
    pass
def actualizar_post(
    posts_filepath: str,
    id_post: str | int,
    id_autor_en_sesion: str | int,
    datos_nuevos: Dict[str, Any],
) -> Dict[str, Any]:
    pass
def eliminar_post(
    posts_filepath: str,
    id_post: str | int,
    id_autor_en_sesion: str | int,
) -> bool:
    pass
def agregar_comentario_a_post(
    posts_filepath: str,
    id_post: str | int,
    autor: str,
    contenido: str,
    *,
    id_autor: Optional[str | int] = None,
) -> Dict[str, Any]:
    pass
def listar_comentarios_de_post(posts_filepath: str, id_post: str | int) \
            -> List[Dict[str, Any]]:
    pass
def eliminar_comentario_de_post(
    posts_filepath: str,
    id_post: str | int,
    id_comentario: str | int,
    *,
    id_autor_en_sesion: Optional[str | int] = None,
) -> bool:
    pass
def actualizar_comentario_de_post(
    posts_filepath: str,
    id_post: str | int,
    id_comentario: str | int,
    datos_nuevos: Dict[str, Any],
    *,
    id_autor_en_sesion: Optional[str | int] = None,
) -> Dict[str, Any]:
    pass
__all__ = [
    # Excepciones
    "ErrorDeDominio",
    "ValidacionError",
    "EmailDuplicado",
    "AutorNoEncontrado",
    "PostNoEncontrado",
    "AccesoNoAutorizado",
    # Autores
    "crear_autor",
    "leer_todos_los_autores",
    "buscar_autor_por_id",
    "buscar_autor_por_email",
    "actualizar_autor",
    "eliminar_autor",
    # Posts
    "crear_post",
    "leer_todos_los_posts",
    "listar_posts_por_autor",
    "buscar_posts_por_tag",
    "buscar_post_por_id",
    "actualizar_post",
    "eliminar_post",
    # Comentarios
    "agregar_comentario_a_post",
    "listar_comentarios_de_post",
    "eliminar_comentario_de_post",
    "actualizar_comentario_de_post",
]
