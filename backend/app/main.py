from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app import db
import os
import mimetypes
import re

app = FastAPI(
    title="Sabor y Mar Cartagena API",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Sabor y Mar Cartagena API - OK"}


@app.get("/menu")
async def get_menu():
    try:
        rows = db.query("""
            SELECT 
                c.id AS comida_id, 
                c.nombre AS comida, 
                c.precio, 
                c.foto,
                cat.id AS categoria_id, 
                cat.nombre AS categoria
            FROM comida c
            JOIN categoria cat ON c.categoria_id = cat.id
            ORDER BY cat.id, c.id
        """)
    except Exception as e:
        raise HTTPException(500, f"Error consultando la BD: {e}")

    menu = {}
    for r in rows:
        categoria = r["categoria"]
        menu.setdefault(categoria, []).append({
            "id": r["comida_id"],
            "nombre": r["comida"],
            "precio": r["precio"],
            "foto": r["foto"],
        })

    return menu


@app.get("/menu/{section}")
async def get_menu_section(section: str):
    try:
        rows = db.query(
            """
            SELECT 
                c.id AS comida_id, 
                c.nombre AS comida, 
                c.precio, 
                c.foto,
                cat.id AS categoria_id, 
                cat.nombre AS categoria
            FROM comida c
            JOIN categoria cat ON c.categoria_id = cat.id
            WHERE LOWER(cat.nombre) = LOWER(%s)
            ORDER BY c.id
            """,
            (section,)
        )
    except Exception as e:
        raise HTTPException(500, f"Error consultando la BD: {e}")

    if not rows:
        raise HTTPException(404, "Sección no encontrada")

    categoria = rows[0]["categoria"]
    items = [{
        "id": r["comida_id"],
        "nombre": r["comida"],
        "precio": r["precio"],
        "foto": r["foto"]
    } for r in rows]

    return {categoria: items}


# Directorio donde el backend buscará las imágenes
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")


def _safe_image_path(name: str) -> str:
    # Permitir sólo nombres simples (evitar traversal)
    if not re.match(r'^[A-Za-z0-9_.-]+$', name):
        return ""
    return os.path.join(IMAGES_DIR, name)


@app.get("/assets/menu/{image_name}")
async def serve_menu_asset(image_name: str):
    """Sirve imágenes desde /assets/menu/{image_name} (compatibilidad con frontend)."""
    path = _safe_image_path(image_name)
    if not path or not os.path.isfile(path):
        raise HTTPException(404, "Imagen no encontrada")
    mime, _ = mimetypes.guess_type(path)
    return FileResponse(path, media_type=mime or "application/octet-stream")


@app.get("/{image_name}")
async def serve_root_image(image_name: str):
    """Sirve imágenes directamente en /{image_name} tal como solicitaste.

    Nota: esta ruta está definida al final para no chocar con las rutas '/menu' y '/menu/{section}'.
    """
    path = _safe_image_path(image_name)
    if not path or not os.path.isfile(path):
        raise HTTPException(404, "Imagen no encontrada")
    mime, _ = mimetypes.guess_type(path)
    return FileResponse(path, media_type=mime or "application/octet-stream")
