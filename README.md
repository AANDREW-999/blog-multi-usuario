<!-- Encabezado con badges y estilo centrado -->

<h1 align="center">📝 Sistema de Blog Multi‑usuario — Dependencias: rich · pytest · ruff</h1>

<p align="center">
  Blog de consola multi‑autor en <b>Python</b> con <b>rich</b>, <b>pytest</b> y <b>ruff</b>. Minimalista, rápido y listo para extender.
</p>
<p align="center">
  <img src="https://img.shields.io/badge/Proyecto-Sistema%20de%20Blog%20Multi--usuario-6A5ACD" alt="Proyecto"/>
  <br/>
  <img src="https://img.shields.io/badge/Dependencias-rich%20|%20pytest%20|%20ruff-2E8B57" alt="Dependencias"/>
  <br/>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://docs.astral.sh/uv/"><img src="https://img.shields.io/badge/Entorno-uv-7F52FF" alt="uv"/></a>
  <a href="https://github.com/Textualize/rich"><img src="https://img.shields.io/badge/rich-CLI%20UI-4E9A06" alt="rich"/></a>
  <a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/tests-pytest-0A9EDC" alt="pytest"/></a>
  <a href="https://docs.astral.sh/ruff/"><img src="https://img.shields.io/badge/lint-ruff-000000" alt="ruff"/></a>
</p>
<hr/>

## 🚀 Ejecución rápida
- Ejecutar la app:
```bash
python src/Modulo/main.py
```

- Ejecutar pruebas:
```bash
pytest -v
```

- Revisar estilo/lint:
```bash
ruff check
```

---

## 🧱 Datos y Entidades
- Autores (autores.csv): id_autor, nombre_autor, email.
- Publicaciones (posts.json): id_post, id_autor, titulo, contenido, fecha_publicacion, tags (p. ej. ["python", "desarrollo"]).
- Comentarios (reto): lista anidada dentro de cada post.

---

## 🔑 Funcionalidades Clave
- CRUD completo para Autores.
- Crear una nueva Publicación y asignarla al autor en sesión (simulada).
- Ver todas las publicaciones de un autor específico.
- Buscar publicaciones por tag.
- Modificar y eliminar solo publicaciones del autor propietario.
- Reto adicional: comentarios anidados por publicación (en JSON).

---

## 👥 Autores
- Andres Gonzalez — andresfelipegonzalez5a@gmail.com  
- Erika Pesca — epescaalfonso@gmail.com  
- David Pedraza — pedrazadavidleonardo@gmail.com  
- Alison Ruiz — ruizhernandezallisonmichele@gmail.com  

---

<!-- Arranque rápido con uv (comandos corregidos) -->
<div align="center"><b>✨ Arranque ultra‑rápido con uv ✨</b></div>

```bash
# Inicializa proyecto (pyproject.toml, etc.)
uv init

# Crea el entorno virtual .venv
uv venv

# Activa el entorno
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# Windows cmd
.venv\Scripts\activate.bat
# Linux/Mac
source .venv/bin/activate

# Instala dependencias
uv add rich pytest ruff
```

---

## 📦 Instalación
Usando uv (recomendado):
```bash
uv init
uv venv
# Activar:
# PowerShell:  . .venv/Scripts/Activate.ps1
# cmd:         .venv\Scripts\activate.bat
# Linux/Mac:   source .venv/bin/activate
uv add rich pytest ruff
```

<details>
<summary>Alternativa con pip (opcional)</summary>

```bash
python -m venv .venv
# Activar:
# PowerShell:  . .venv/Scripts/Activate.ps1
# cmd:         .venv\Scripts\activate.bat
# Linux/Mac:   source .venv/bin/activate
pip install rich pytest ruff
```
</details>

---