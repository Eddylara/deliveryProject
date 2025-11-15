-- ======================================================
--   CREACIÓN DE TABLA CATEGORÍA
-- ======================================================

CREATE TABLE IF NOT EXISTS categoria (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- ======================================================
--   CREACIÓN DE TABLA COMIDA
-- ======================================================

CREATE TABLE IF NOT EXISTS comida (
    id SERIAL PRIMARY KEY,
    categoria_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio INT NOT NULL,
    foto VARCHAR(255),

    CONSTRAINT fk_categoria
        FOREIGN KEY (categoria_id) REFERENCES categoria(id)
        ON DELETE CASCADE
);

-- ======================================================
--   CREACIÓN DE TABLAS PEDIDO Y DETALLE_PEDIDO
-- ======================================================

CREATE TABLE IF NOT EXISTS pedido (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento VARCHAR(30) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    apto VARCHAR(50),
    telefono VARCHAR(20) NOT NULL,
    notas TEXT,
    fecha TIMESTAMP DEFAULT NOW(),
    estado VARCHAR(20) NOT NULL,
    total INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS detalle_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL,
    comida_id INT NOT NULL,
    cantidad INT NOT NULL,
    subtotal INT NOT NULL,

    CONSTRAINT fk_pedido
        FOREIGN KEY (pedido_id) REFERENCES pedido(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_comida
        FOREIGN KEY (comida_id) REFERENCES comida(id)
        ON DELETE CASCADE
);

-- ======================================================
--   INSERTS DE LAS CATEGORÍAS
-- ======================================================

INSERT INTO categoria (nombre) VALUES
('sushi'),
('hamburguesa'),
('perro'),
('pizza'),
('bebida'),
('postre')
ON CONFLICT DO NOTHING;

-- ======================================================
--   INSERTS DE COMIDAS (ya usando categoria_id)
-- ======================================================

-- 🍣 SUSHI  (categoria_id = 1)
INSERT INTO comida (categoria_id, nombre, precio, foto) VALUES
(1, 'California Roll', 22000, 'assets/menu/imagen-sushi-1.jpg'),
(1, 'Philadelphia Roll', 24000, 'assets/menu/imagen-sushi-2.jpg'),
(1, 'Kani Roll (cangrejo)', 23000, 'assets/menu/imagen-sushi-3.jpg')
ON CONFLICT DO NOTHING;

-- 🍔 HAMBURGUESAS  (categoria_id = 2)
INSERT INTO comida (categoria_id, nombre, precio, foto) VALUES
(2, 'Clásica con queso', 18000, 'assets/menu/imagen-hamburgues-1.jpg'),
(2, 'Doble carne/doble queso', 26000, 'assets/menu/imagen-hamburgues-2.jpg'),
(2, 'BBQ Bacon', 24000, 'assets/menu/imagen-hamburgues-3.jpg')
ON CONFLICT DO NOTHING;

-- 🌭 PERROS CALIENTES  (categoria_id = 3)
INSERT INTO comida (categoria_id, nombre, precio, foto) VALUES
(3, 'Perro americano', 15000, 'assets/menu/imagen-perros-cal-1.jpg'),
(3, 'Perro costeño (con papitas y cebolla)', 17000, 'assets/menu/imagen-perros-cal-2.jpg')
ON CONFLICT DO NOTHING;

-- 🍕 PIZZAS (categoria_id = 4)
INSERT INTO comida (categoria_id, nombre, precio, foto) VALUES
(4, 'Margarita', 20000, 'assets/menu/imagen-pizzas-per-1.jpg'),
(4, 'Hawaiana', 22000, 'assets/menu/imagen-pizzas-per-2.jpg'),
(4, 'Pepperoni', 24000, 'assets/menu/imagen-pizzas-per-3.jpg')
ON CONFLICT DO NOTHING;

-- 🥤 BEBIDAS (categoria_id = 5)
INSERT INTO comida (categoria_id, nombre, precio, foto) VALUES
(5, 'Gaseosas', 5000, 'assets/menu/imagen-bebidas-1.jpg'),
(5, 'Jugos naturales', 7000, 'assets/menu/imagen-bebidas-2.jpg'),
(5, 'Limonada de coco', 8000, 'assets/menu/imagen-bebidas-3.jpg'),
(5, 'Té frío', 6000, 'assets/menu/imagen-bebidas-4.jpg')
ON CONFLICT DO NOTHING;

-- 🍰 POSTRES (categoria_id = 6)
INSERT INTO comida (categoria_id, nombre, precio, foto) VALUES
(6, 'Cheesecake', 15000, 'assets/menu/imagen-postres-1.jpg'),
(6, 'Rollo de banana frito', 12000, 'assets/menu/imagen-postres-2.jpg'),
(6, 'Helado artesanal', 10000, 'assets/menu/imagen-postres-3.jpg')
ON CONFLICT DO NOTHING;
