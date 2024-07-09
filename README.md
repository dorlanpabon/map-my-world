# Map My World API

Map My World es una aplicación destinada a explorar y revisar diferentes ubicaciones y categorías del mundo, como restaurantes, parques y museos. Esta API proporciona endpoints para gestionar ubicaciones, categorías y generar recomendaciones basadas en las combinaciones de ubicación-categoría.

## Requisitos

- Python 3.9
- PostgreSQL

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/dorlanpabon/map-my-world.git
cd map-my-world
```

2. Crea un entorno virtual e instala las dependencias:

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:

Copia el archivo `.env.example` a `.env` y modifica las variables de entorno según tu configuración.

# Ejecutar la aplicación

Para ejecutar la aplicación, utiliza el siguiente comando:

Desarrollo:
```bash
fastapi dev app.main:app 
o
fastapi dev .\app\main.py
```

Producción:
```bash
fastapi run app.main:app
o
fastapi run .\app\main.py
```

# Estrucutra de archivos

```
map_my_world/
├── app/
│   ├── config/            # Configuraciones de la base de datos
│   ├── services/          # Servicios y operaciones CRUD
│   ├── models/            # Modelos de datos
│   ├── routers/           # Rutas de la API
│   ├── schemas/           # Esquemas de Pydantic
│   ├── __init__.py
│   ├── main.py            # Punto de entrada de la aplicación
├── .env.example           # Archivo de ejemplo de variables de entorno
├── requirements.txt       # Dependencias del proyecto
├── README.md              # Documentación del proyecto
```

# TODO: Mejoras pendientes

- [ ] Implementar pruebas unitarias y de integración para los servicios y rutas de la API.
- [ ] Aumentar exactitud en la respuesta de errores de la API.
- [ ] Normalizar la tabla location_category_rewieweb para evitar duplicidad de datos, creando una tabla aparte para relacionar las tablas location y category, seguido de una tabla para las reviews.