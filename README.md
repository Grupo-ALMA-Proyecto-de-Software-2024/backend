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
  