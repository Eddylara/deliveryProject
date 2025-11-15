from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app import db

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
