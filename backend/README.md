# Backend de prueba — Sabor y Mar Cartagena

Este pequeño backend usa FastAPI para exponer una API REST de prueba con el menú.

Instalación y ejecución (PowerShell):

```powershell
cd "c:/Users/USUARIO/Documents/Proyectos/ 2025-2/deliveryProject/backend"
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Lanzar la app (ejecutar DESDE la carpeta `backend`):
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Nota: no ejecutes `uvicorn main:app` desde dentro de `backend/app` cuando uses importaciones relativas (por ejemplo `from .menu_data import MENU`). El comando correcto apunta al paquete `app` como `app.main:app` y debe ejecutarse desde la carpeta `backend`.

Puntos finales disponibles:

- `GET /` — estado de la API
- `GET /menu` — devuelve todo el menú
- `GET /menu/{section}` — devuelve una sección específica (ej: `/menu/SUSHI` o `/menu/BEBIDAS`)

Notas:
- CORS está habilitado para pruebas locales.
- Este backend es una API de prueba sin persistencia; los datos están en `app/menu_data.py`.
