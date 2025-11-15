from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app import db
import os
import mimetypes
import re
from pydantic import BaseModel
from fastapi import UploadFile, File, Form
from pathlib import Path
from typing import Optional
from typing import Literal

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
            "categoria_id": r["categoria_id"],
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
        "foto": r["foto"],
        "categoria_id": r["categoria_id"],
    } for r in rows]

    return {categoria: items}


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post('/admin/login')
async def admin_login(payload: LoginRequest):
    """Verifica credenciales simples para el panel de administración.

    Requisitos: usuario == 'admin' y password == 'sushi'. No usa la base de datos.
    """
    if payload.username == 'admin' and payload.password == 'sushi':
        return {"authorized": True}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")


# ==============================
#   Pedido (órdenes)
# ==============================

class PedidoItemPayload(BaseModel):
    comida_id: int
    cantidad: int


class PedidoCreatePayload(BaseModel):
    nombre: str
    apellido: str
    documento: str
    direccion: str
    apto: Optional[str] = None
    telefono: str
    notas: Optional[str] = None
    items: list[PedidoItemPayload]


@app.post('/pedido')
async def crear_pedido(payload: PedidoCreatePayload):
    # Validaciones básicas
    if not payload.items:
        raise HTTPException(400, 'El pedido debe contener al menos un ítem')
    for it in payload.items:
        if it.cantidad <= 0:
            raise HTTPException(400, f'Cantidad inválida para comida_id {it.comida_id}')

    # Traer precios desde BD para evitar manipulación de cliente
    ids = tuple(set(it.comida_id for it in payload.items))
    placeholders = ','.join(['%s'] * len(ids))
    try:
        rows = db.query(f"SELECT id, precio FROM comida WHERE id IN ({placeholders})", ids)
    except Exception as e:
        raise HTTPException(500, f'Error consultando comidas: {e}')
    precios = {r['id']: int(r['precio']) for r in rows}

    # Validar que todas las comidas existan
    faltantes = [it.comida_id for it in payload.items if it.comida_id not in precios]
    if faltantes:
        raise HTTPException(400, f'Comida(s) no encontrada(s): {faltantes}')

    # Calcular subtotales y total
    total = 0
    detalles = []
    for it in payload.items:
        pr = precios[it.comida_id]
        sub = pr * it.cantidad
        total += sub
        detalles.append({
            'comida_id': it.comida_id,
            'cantidad': it.cantidad,
            'subtotal': sub,
        })

    # Insertar pedido + detalles en transacción
    try:
        conn = db.get_connection()
        cur = conn.cursor()
        sql_ped = (
            "INSERT INTO pedido (nombre, apellido, documento, direccion, apto, telefono, notas, estado, total) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, fecha, estado"
        )
        cur.execute(sql_ped, (
            payload.nombre, payload.apellido, payload.documento,
            payload.direccion, payload.apto, payload.telefono,
            payload.notas, 'pendiente', total
        ))
        ped_row = cur.fetchone()
        pedido_id = ped_row[0]

        for d in detalles:
            cur.execute(
                "INSERT INTO detalle_pedido (pedido_id, comida_id, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
                (pedido_id, d['comida_id'], d['cantidad'], d['subtotal'])
            )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        raise HTTPException(500, f'Error creando el pedido: {e}')

    return {"id": pedido_id, "total": total, "estado": "pendiente"}


@app.get('/pedido/{pedido_id}')
async def obtener_pedido(pedido_id: int):
    try:
        ped = db.query("SELECT * FROM pedido WHERE id = %s", (pedido_id,))
        if not ped:
            raise HTTPException(404, 'Pedido no encontrado')
        det = db.query(
            """
            SELECT d.id, d.comida_id, d.cantidad, d.subtotal, c.nombre AS comida, c.precio
            FROM detalle_pedido d
            JOIN comida c ON c.id = d.comida_id
            WHERE d.pedido_id = %s
            ORDER BY d.id
            """,
            (pedido_id,)
        )
        return {"pedido": ped[0], "detalles": det}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f'Error consultando el pedido: {e}')


# ==============================
#   Admin: gestión de pedidos
# ==============================

EstadoPedido = Literal['pendiente', 'preparando', 'enviado', 'entregado', 'cancelado']


@app.get('/admin/pedidos')
async def admin_list_pedidos(estado: Optional[EstadoPedido] = None):
    """Lista pedidos con información básica y cantidad de ítems.

    Parámetro opcional `estado` para filtrar.
    """
    try:
        params = []
        where = ""
        if estado:
            where = "WHERE p.estado = %s"
            params.append(estado)
        rows = db.query(
            f"""
            SELECT p.id, p.fecha, p.nombre, p.apellido, p.telefono, p.direccion, p.apto, p.estado, p.total,
                   COALESCE(SUM(d.cantidad), 0) AS items_count
            FROM pedido p
            LEFT JOIN detalle_pedido d ON d.pedido_id = p.id
            {where}
            GROUP BY p.id
            ORDER BY p.fecha DESC, p.id DESC
            """,
            tuple(params) if params else None
        )
        return rows
    except Exception as e:
        raise HTTPException(500, f"Error listando pedidos: {e}")


class PedidoEstadoPayload(BaseModel):
    estado: EstadoPedido


@app.put('/admin/pedidos/{pedido_id}/estado')
async def admin_update_pedido_estado(pedido_id: int, payload: PedidoEstadoPayload):
    try:
        affected = db.execute("UPDATE pedido SET estado = %s WHERE id = %s", (payload.estado, pedido_id))
        if affected == 0:
            raise HTTPException(404, 'Pedido no encontrado')
        return {"updated": True, "id": pedido_id, "estado": payload.estado}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error actualizando estado: {e}")


@app.get('/admin/categories')
async def list_categories():
    try:
        rows = db.query("SELECT id, nombre FROM categoria ORDER BY id")
        return rows
    except Exception as e:
        raise HTTPException(500, f"Error consultando categorías: {e}")


# Directorio donde el backend buscará las imágenes
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "images")
ALLOWED_IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp", ".gif"]


def _safe_image_path(name: str) -> str:
    # Permitir sólo nombres simples (evitar traversal)
    if not re.match(r'^[A-Za-z0-9_.-]+$', name):
        return ""
    return os.path.join(IMAGES_DIR, name)


def _resolve_image_path(name: str) -> str | None:
    """Resuelve una imagen por nombre, con o sin extensión.

    - Si `name` tiene extensión y existe, devuelve esa ruta.
    - Si no tiene extensión, intenta encontrar un archivo con cualquiera de ALLOWED_IMAGE_EXTS.
    - La búsqueda no es recursiva y respeta el nombre base exacto (sin mayúsc./minúsc. especiales).
    """
    base = Path(name).name  # sanitize y tomar sólo el nombre
    if not base or not re.match(r'^[A-Za-z0-9_.-]+$', base):
        return None

    direct = os.path.join(IMAGES_DIR, base)
    if os.path.isfile(direct):
        return direct

    # Si no hay extensión, probar variantes
    if Path(base).suffix == "":
        stem = Path(base).stem
        for ext in ALLOWED_IMAGE_EXTS:
            candidate = os.path.join(IMAGES_DIR, f"{stem}{ext}")
            if os.path.isfile(candidate):
                return candidate
    return None


def _sanitize_filename(filename: str) -> str:
    """Normaliza el nombre de archivo para evitar traversal y caracteres peligrosos.

    - Conserva sólo letras, números, guiones, guion bajo y punto.
    - Reemplaza espacios por guiones.
    - Extensión en minúsculas y validada contra ALLOWED_IMAGE_EXTS.
    """
    base = Path(filename).name
    stem = Path(base).stem
    suffix = Path(base).suffix.lower()

    # Validar extensión
    if suffix not in ALLOWED_IMAGE_EXTS:
        raise HTTPException(400, f"Extensión no permitida: {suffix or '(sin extensión)'}")

    # Normalizar el stem: letras/números/_/./- y espacios→-
    stem = stem.replace(" ", "-")
    stem = re.sub(r"[^A-Za-z0-9_.-]", "", stem)
    stem = re.sub(r"-+", "-", stem).strip("-._") or "img"

    return f"{stem}{suffix}"


def _unique_path(directory: str, filename: str) -> str:
    """Devuelve una ruta única dentro de `directory` para `filename`.

    Si ya existe, añade sufijos -1, -2, ... antes de la extensión.
    """
    p = Path(directory) / filename
    if not p.exists():
        return str(p)
    stem = p.stem
    suffix = p.suffix
    i = 1
    while True:
        candidate = p.with_name(f"{stem}-{i}{suffix}")
        if not candidate.exists():
            return str(candidate)
        i += 1


@app.get("/assets/menu/{image_name}")
async def serve_menu_asset(image_name: str):
    """Sirve imágenes desde /assets/menu/{image_name} (compatibilidad con frontend)."""
    path = _resolve_image_path(image_name)
    if not path:
        raise HTTPException(404, "Imagen no encontrada")
    mime, _ = mimetypes.guess_type(path)
    return FileResponse(path, media_type=mime or "application/octet-stream")


@app.get("/{image_name}")
async def serve_root_image(image_name: str):
    """Sirve imágenes directamente en /{image_name} tal como solicitaste.

    Nota: esta ruta está definida al final para no chocar con las rutas '/menu' y '/menu/{section}'.
    """
    path = _resolve_image_path(image_name)
    if not path:
        raise HTTPException(404, "Imagen no encontrada")
    mime, _ = mimetypes.guess_type(path)
    return FileResponse(path, media_type=mime or "application/octet-stream")


@app.post('/admin/menu')
async def create_menu_item(
    nombre: str = Form(...),
    precio: int = Form(...),
    categoria_id: int = Form(...),
    foto: UploadFile | None = File(None),
):
    """Crea un nuevo registro en la tabla `comida`.

    - Si se envía un archivo `foto`, se guarda en `app/images` y en la BD se guarda sólo el nombre del archivo.
    - Si no se envía archivo, se puede enviar el nombre en el campo `foto` (como texto) — no obligatorio aquí.
    """
    # Asegurarse de que el directorio exista
    Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)

    filename = None
    if foto is not None:
        # normalizar nombre y validar extensión
        orig = Path(foto.filename).name
        try:
            safe_name = _sanitize_filename(orig)
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(400, "Nombre de archivo inválido")
        dest = _unique_path(IMAGES_DIR, safe_name)
        try:
            with open(dest, 'wb') as f:
                content = await foto.read()
                f.write(content)
        except Exception as e:
            raise HTTPException(500, f"Error guardando la imagen: {e}")
        filename = Path(dest).name

    # Insertar en la BD; almacenamos sólo el nombre del archivo (o NULL)
    foto_db = filename if filename else None
    try:
        sql = "INSERT INTO comida (categoria_id, nombre, precio, foto) VALUES (%s, %s, %s, %s) RETURNING id"
        # execute no devuelve el id; abrir una conexión manual para obtener el id
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute(sql, (categoria_id, nombre, precio, foto_db))
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        raise HTTPException(500, f"Error insertando en la BD: {e}")

    return {"id": new_id, "nombre": nombre, "precio": precio, "foto": foto_db, "categoria_id": categoria_id}


@app.put('/admin/menu/{item_id}')
async def update_menu_item(
    item_id: int,
    nombre: Optional[str] = Form(None),
    precio: Optional[int] = Form(None),
    categoria_id: Optional[int] = Form(None),
    foto: UploadFile | None = File(None),
):
    # Guardar nueva foto si viene
    new_filename = None
    if foto is not None:
        Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)
        orig = Path(foto.filename).name
        try:
            safe_name = _sanitize_filename(orig)
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(400, "Nombre de archivo inválido")
        dest = _unique_path(IMAGES_DIR, safe_name)
        try:
            with open(dest, 'wb') as f:
                content = await foto.read()
                f.write(content)
        except Exception as e:
            raise HTTPException(500, f"Error guardando la imagen: {e}")
        new_filename = Path(dest).name

    # Construir UPDATE dinámico
    sets = []
    params = []
    if nombre is not None:
        sets.append("nombre = %s")
        params.append(nombre)
    if precio is not None:
        sets.append("precio = %s")
        params.append(precio)
    if categoria_id is not None:
        sets.append("categoria_id = %s")
        params.append(categoria_id)
    if new_filename is not None:
        sets.append("foto = %s")
        params.append(new_filename)

    if not sets:
        raise HTTPException(400, "No se enviaron campos para actualizar")

    params.append(item_id)
    sql = f"UPDATE comida SET {', '.join(sets)} WHERE id = %s"
    try:
        affected = db.execute(sql, tuple(params))
        if affected == 0:
            raise HTTPException(404, "Elemento no encontrado")
        return {"updated": True, "id": item_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error actualizando el elemento: {e}")


@app.delete('/admin/menu/{item_id}')
async def delete_menu_item(item_id: int):
    try:
        affected = db.execute("DELETE FROM comida WHERE id = %s", (item_id,))
        if affected == 0:
            raise HTTPException(404, "Elemento no encontrado")
        return {"deleted": True, "id": item_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error eliminando el elemento: {e}")
