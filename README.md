# Sistema Hostelería · 7 herramientas con IA para tu restaurante

Siete herramientas que cualquier dueño de un bar o restaurante puede montar por su cuenta, con una hoja de cálculo y un asistente de IA (Claude, ChatGPT o el que uses). Sin programar.

Cada herramienta tiene su checklist: qué datos necesitas, de dónde los sacas, qué pasos das y cómo sabes que quedó bien.

> **Estado (21-nov-2026).** Las 7 herramientas tienen su checklist; las hojas de cálculo tienen las fórmulas verificadas sobre datos inventados. Las herramientas 6 y 7 traen además una habilidad para Claude Code. **Nada está probado todavía en un restaurante real**: ese es el siguiente paso.

## Las 7 herramientas

| Nº | Herramienta | Qué te da | Tiempo de montaje (estimado, sin probar) | Archivo |
|---|---|---|---|---|
| 1 | **Panel del restaurante** | Tus números en una página: ventas, ticket medio, comensales, coste de producto, coste de personal, margen y resultado | 2-3 h | [01-panel.md](01-panel.md) |
| 2 | **Cerebro de costes** | El margen real de cada plato, con los precios de proveedor al día | 3-5 h (según el tamaño de la carta) | [02-cerebro-de-costes.md](02-cerebro-de-costes.md) |
| 3 | **Revisión de los lunes** | Cada lunes, dónde se te fue el dinero la semana pasada y qué hacer | 1 h + 20 min cada lunes | [03-revision-de-los-lunes.md](03-revision-de-los-lunes.md) |
| 4 | **Kit de marca** | Una ficha única con tus datos, tu tono y tus textos, igual en Google, web y redes | 1-2 h | [04-kit-de-marca.md](04-kit-de-marca.md) |
| 5 | **Biblioteca de reseñas** | Todas tus reseñas juntas, los problemas que se repiten y las respuestas | 2 h + 20 min cada semana | [05-biblioteca-de-resenas.md](05-biblioteca-de-resenas.md) |
| 6 | **La carta que vende** | Qué platos destacar, cuáles subir, cuáles mover y cuáles quitar, según lo que dejan y lo que se venden; y la carta reescrita | 1-2 h + 20 min cada mes | [06-la-carta-que-vende.md](06-la-carta-que-vende.md) |
| 7 | **Asistente de redes** | El plan de publicaciones de la semana en tu tono, empujando los platos que te convienen, y ayuda para responder comentarios | 30 min + 20 min cada lunes | [07-asistente-de-redes.md](07-asistente-de-redes.md) |

## Las hojas

| Hoja (en `plantillas/`) | Herramienta | Pestañas |
|---|---|---|
| `panel.xlsx` | 1 y 3 | Panel · Lunes · Ajustes · Ventas · Compras · Mes · Decisiones |
| `costes.xlsx` | 2 y 6 | Platos · Carta · Ajustes · Ingredientes · Escandallos |
| `marca-canales.xlsx` + `ficha-de-marca.md` | 4 | Comprobación · Canales |
| `resenas.xlsx` | 5 | Resumen · Ajustes · Reseñas |
| `plan-de-redes.md` | 7 | El plan de la semana y los resultados del mes |

En todas: **celdas amarillas, las rellenas tú; el resto se calcula solo.** Se abren con Excel o subiéndolas a Google Drive.

Los CSV de `plantillas/` son las mismas tablas sueltas, por si prefieres montar tu propia hoja.

## Por dónde empezar

1. Lee [00-antes-de-empezar.md](00-antes-de-empezar.md): qué necesitas y cómo proteger tus datos.
2. Monta las herramientas **en este orden**. Cada una usa datos de la anterior:
   - El **Panel (1)** te obliga a reunir ventas, compras y personal.
   - El **Cerebro de costes (2)** usa las compras del panel.
   - La **Revisión de los lunes (3)** lee el panel y el cerebro de costes.
   - El **Kit de marca (4)** y la **Biblioteca de reseñas (5)** son independientes: puedes hacerlas cuando quieras. Si solo tienes una tarde, empieza por la 4: es la más rápida.
3. La **Carta que vende (6)** usa el Cerebro de costes, y el **Asistente de redes (7)** usa el Kit de marca, las reseñas y la carta: déjalas para el final.
4. **Con Claude Code** puedes hacer la 6 y la 7 conversando: abre Claude Code en esta carpeta y pídele «analiza mi carta» o «prepárame el plan de redes de la semana».
5. Si tu negocio es distinto (bar de copas, cafetería, comida para llevar, varios locales), mira en cada checklist el apartado **«Adáptalo a tu negocio»**.

## Qué es igual para todos y qué cambia

- **Igual para todos:** las 7 herramientas, las fórmulas, las plantillas y el orden.
- **Cambia en cada negocio:** de dónde salen los datos (cada programa de caja exporta distinto), tus objetivos de coste, tu carta y tu tono.

## Qué NO es

- No es un programa que se instala. Son plantillas, pasos e instrucciones para tu asistente de IA.
- No sustituye a tu gestor ni a tu contable. Los números del panel son de gestión, no fiscales.
- La IA se equivoca. Cada checklist termina con una comprobación a mano. No te la saltes.

## Contenido

```
00-antes-de-empezar.md
01-panel.md
02-cerebro-de-costes.md
03-revision-de-los-lunes.md
04-kit-de-marca.md
05-biblioteca-de-resenas.md
06-la-carta-que-vende.md
07-asistente-de-redes.md
CLAUDE.md               ← instrucciones para Claude Code
.claude/skills/         ← habilidades: carta-del-restaurante y asistente-de-redes
REFERENCIAS.md          ← de dónde salen las cifras orientativas
plantillas/             ← las hojas vacías, con las fórmulas hechas
ejemplo/                ← las mismas hojas rellenas con datos INVENTADOS (un restaurante que no existe)
herramientas/           ← crear_*.py (generan las hojas) y comprobar_*.py (verifican las fórmulas)
```

## Para quien quiera tocar las hojas

Las hojas se generan con los programas de `herramientas/` (Python con `openpyxl`):

```
python herramientas/crear_panel.py
python herramientas/crear_costes.py
python herramientas/crear_marca.py
python herramientas/crear_resenas.py
```

Los `comprobar_*.py` recalculan las hojas de ejemplo con un motor de fórmulas (`pip install formulas`) y comparan cada cifra con la misma cuenta hecha aparte. Si cambias una fórmula, pásalos antes de dar la hoja por buena.
