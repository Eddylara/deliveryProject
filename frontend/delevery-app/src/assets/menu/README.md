Carpeta para imágenes del menú

Coloca aquí las imágenes que usará la aplicación Angular.

Ruta (desde la raíz del proyecto Angular):
`src/assets/menu/`

Cómo referenciarlas en `menu.component.ts`:
- En el objeto `MenuItem` asigna `imageUrl: 'assets/menu/imagen-...jpg'`.
- Angular sirve todo lo que esté en `src/assets` bajo la ruta `/assets/`, por eso la referencia no debe llevar `src/` al usarla en el código.

Formato y nombres sugeridos
- Usa extensiones comunes como `.jpg` o `.png`.
- El componente `menu.component.ts` incluye una función `getSuggestedFilename(sectionTitle, index)` que genera rutas del tipo `assets/menu/imagen-<safe>-<n>.jpg`.

Nombres sugeridos generados desde `menu.component.ts` (aplicar exactamente estos nombres si quieres usar la función tal cual):

Sección: 🍣 SUSHI
- `assets/menu/imagen-sushi-1.jpg` — California Roll
- `assets/menu/imagen-sushi-2.jpg` — Philadelphia Roll
- `assets/menu/imagen-sushi-3.jpg` — Kani Roll (cangrejo)

Sección: 🍔 Hamburguesas
- `assets/menu/imagen-hamburgues-1.jpg` — Clásica con queso
- `assets/menu/imagen-hamburgues-2.jpg` — Doble carne/doble queso
- `assets/menu/imagen-hamburgues-3.jpg` — BBQ Bacon

Sección: Perros calientes
- `assets/menu/imagen-perros-cal-1.jpg` — Perro americano
- `assets/menu/imagen-perros-cal-2.jpg` — Perro costeño (con papitas y cebolla)

Sección: Pizzas personales
- `assets/menu/imagen-pizzas-per-1.jpg` — Margarita
- `assets/menu/imagen-pizzas-per-2.jpg` — Hawaiana
- `assets/menu/imagen-pizzas-per-3.jpg` — Pepperoni

Sección: 🥤 BEBIDAS
- `assets/menu/imagen-bebidas-1.jpg` — Gaseosas
- `assets/menu/imagen-bebidas-2.jpg` — Jugos naturales
- `assets/menu/imagen-bebidas-3.jpg` — Limonada de coco
- `assets/menu/imagen-bebidas-4.jpg` — Té frío

Sección: 🍰 POSTRES
- `assets/menu/imagen-postres-1.jpg` — Cheesecake
- `assets/menu/imagen-postres-2.jpg` — Rollo de banana frito
- `assets/menu/imagen-postres-3.jpg` — Helado artesanal

Consejos finales
- Si no tienes las imágenes ahora, deja los `imageUrl` vacíos en `menu.component.ts` (como está actualmente). Cuando subas la imagen con uno de los nombres sugeridos, actualiza la entrada correspondiente poniendo, por ejemplo:
  `imageUrl: 'assets/menu/imagen-sushi-1.jpg'`.
- Evita espacios en los nombres de archivo y usa minúsculas para mantener consistencia.
- Si quieres que yo también rellene `imageUrl` automáticamente en `menu.component.ts` con estos nombres sugeridos, dímelo y lo hago.

