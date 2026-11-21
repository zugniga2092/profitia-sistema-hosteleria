---
name: carta-del-restaurante
description: >
  Analiza la carta de un restaurante con sus números (lo que deja y lo que se vende cada plato), la clasifica en
  cuatro grupos por sección y ayuda a rediseñarla: qué destacar, qué subir, qué mover, qué quitar, cómo ordenarla
  y cómo describir los platos. Úsala cuando la persona hable de su carta, su menú, sus platos, precios de la carta,
  qué plato quitar o poner, o pida mejorar la carta o «ingeniería de menú».
---

# La carta que vende

Herramienta 6 del Sistema Hostelería. La lista de pasos completa está en `06-la-carta-que-vende.md`; esta
habilidad es para hacerlo con la persona, conversando.

## Qué necesitas de la persona
1. Su hoja de costes (`Costes - [su local].xlsx`, hecha con `plantillas/costes.xlsx`) con, por plato: precio de
   carta con IVA, escandallo y **raciones vendidas al mes**. Si no la tiene, empieza por `02-cerebro-de-costes.md`:
   sin margen real no hay análisis, y no se inventa.
2. La **sección** de cada plato (columna amarilla de la pestaña Carta). Si no la ha puesto, pregúntala.
3. Su ficha de marca (`4-marca`), para escribir las descripciones en su tono.

## Cómo leer la hoja
No leas los resultados de las fórmulas con openpyxl: si la hoja no se ha abierto en Excel, vienen vacíos. Ejecuta:

```
python herramientas/leer_carta.py "ruta/a/su hoja.xlsx"
```

Hace las mismas cuentas que la hoja a partir de los datos escritos y devuelve, por plato: sección, precio, raciones,
coste, margen, coste % y grupo. Si sale un aviso (sin escandallo, sin precio), díselo antes de seguir.

## Los cuatro grupos (método de Kasavana y Smith, 1982, por sección)
- **Muy vendido:** su parte de las ventas de la sección ≥ 70 % de 1 / nº de platos de la sección.
- **Deja mucho:** margen por ración ≥ margen medio de la sección ponderado por raciones.

| Grupo | Acción |
|---|---|
| Estrella | Protegerlo: buen sitio, misma ración y calidad |
| Muy vendido, deja poco | Mejorar margen: ración, coste o subida pequeña y gradual |
| Deja mucho, se vende poco | Visibilidad: posición, descripción, recomendación en sala |
| Se vende poco y deja poco | Cambiarlo o quitarlo, salvo motivo (vegano, niños, sin gluten) |

## Cómo trabajar con la persona
1. **Enséñale el cuadro** por secciones, en una tabla, con una frase por plato que explique su grupo con sus números.
2. **Propón como máximo 3 cambios para este mes**, los de más impacto en euros. Para cada uno, la cuenta:
   «si subes 0,50 € el secreto, con 240 raciones al mes son 109 € más de margen (0,50 / 1,10 × 240)».
   Recuerda que el precio de carta lleva IVA: el margen sube el precio sin IVA.
3. **Pregunta antes de quitar** un plato: puede tener un motivo que los números no ven.
4. **Rediseño de la carta**, si lo pide:
   - Cada sección empieza por una estrella o un plato que deja mucho.
   - Uno o dos «recomendados» por sección, como máximo.
   - Precios al final de la descripción, no en columna; siempre con IVA incluido.
   - Descripciones de máximo 20 palabras, en su tono: origen y elaboración solo si están en sus datos. Nada de
     «delicioso», «exquisito», «el mejor». Lo que falte, `[PREGUNTAR]`.
   - Recuerda los alérgenos: informar de los 14 es obligatorio (Reglamento UE 1169/2011); en la carta o en un
     documento a disposición del cliente. Que lo confirme con su asesor.
5. **Que lo apunte**: cada cambio, en la pestaña Decisiones del Panel, con fecha. Al mes, se vuelve a mirar.

## Reglas
- Nunca inventes precios, costes, raciones, ingredientes, orígenes ni alérgenos.
- No compares platos de secciones distintas.
- Un plato con menos de un mes en carta aún no tiene datos fiables: dilo.
- Palabras claras, sin jerga. Si dices «margen», explica que es lo que le queda por ración después de pagar los
  ingredientes y el IVA.
