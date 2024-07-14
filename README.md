# Backend de ALMA

This is the backend for the ALMA data repository.

## Getting Started

### Prerequisitos

- Python 3.11
- [Poetry](https://python-poetry.org/docs/#installation)

### Instalación

Para instalar las dependencias del proyecto, ejecutar el siguiente comando:

```bash
poetry install
```

### Uso

Este proyecto utiliza un Makefile para gestionar las tareas del backend. Aquí están los comandos disponibles:

- `make run`: Inicia el servidor de desarrollo.
- `make test`: Ejecuta los tests del proyecto.
- `make quality-check`: Ejecuta las herramientas de calidad de código.
- `make format`: Formatea el código del proyecto.
- `make migrate`: Ejecuta las migraciones de la base de datos.
- `make superuser`: Crea un superusuario para acceder al admin de Django.
- `make delete-database`: Elimina la base de datos actual.
- `make collectstatic`: Recolecta los archivos estáticos del proyecto.

## Documentación

### API

La documentación de la API se encuentra está hecha con swagger y se puede acceder a través de la ruta `/docs`. (Ej: `http://localhost:8000/docs`).

### BackOffice

El backoffice está hecho con Django Admin y se puede acceder a través de la ruta `/admin`. (Ej: `http://localhost:8000/admin`). Para más información, ver la documentación del [BackOffice](./docs/BACKOFFICE.md).
