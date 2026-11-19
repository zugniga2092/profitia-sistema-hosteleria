# 3 · Revisión de los lunes

**Qué es:** cada lunes, tu asistente de IA repasa la semana pasada con los datos del panel y te dice dónde se fue el dinero.
**Para qué sirve:** convertir los números en una decisión por semana, en 20 minutos.

**Necesitas tener montados** el [Panel (1)](01-panel.md) y, si puedes, el [Cerebro de costes (2)](02-cerebro-de-costes.md).

## Qué revisa

| Bloque | Qué mira | Contra qué lo compara |
|---|---|---|
| Ventas | Total, por día y por turno | Semana anterior y misma semana del mes pasado |
| Comensales y ticket medio | Cuánta gente y cuánto gasta | Semana anterior |
| Coste de producto % | Compras o consumo sobre ventas | Tu objetivo |
| Coste de personal % | Coste y horas sobre ventas | Tu objetivo |
| Rotación de mesas | Comensales ÷ plazas, por servicio | Semana anterior |
| Platos | Los 5 más vendidos y los 5 menos | Su margen en el cerebro de costes |

**Los límites los pones tú.** En el Panel fijaste tu objetivo de coste de producto y de personal. La revisión avisa cuando los superas. Los rangos del sector están en [REFERENCIAS.md](REFERENCIAS.md), pero son orientativos.

## Checklist

### Paso 1 · Prepara la revisión (30 min, una sola vez)
- [ ] En la carpeta `3-lunes`, crea un documento `Objetivos.md` con tus cifras:

```
Objetivo de coste de producto: [  ] %
Objetivo de coste de personal: [  ] %
Objetivo de ticket medio: [  ] €
Plazas del local: [  ]
Servicios por semana: [  ]
```

- [ ] Súbelo a tu proyecto de IA.
- [ ] Guarda esta instrucción en un documento `Revision-lunes.md` y súbela también:

```
REVISIÓN DE LOS LUNES

Te paso los datos de la semana pasada: ventas por día, comensales, compras de la semana,
coste de personal y horas, y ventas por plato. Tienes mis objetivos en Objetivos.md.

Hazme el informe con esta estructura exacta:

1. LA SEMANA EN UNA FRASE.
2. NÚMEROS: tabla con ventas, comensales, ticket medio, coste de producto %,
   coste de personal % y rotación. Columnas: esta semana, semana anterior, objetivo, diferencia.
3. DÓNDE SE FUE EL DINERO: solo lo que supera mi objetivo. Para cada punto,
   cuántos euros supone la diferencia y la causa más probable según los datos.
   Si no puedes saber la causa con los datos que tienes, dilo y dime qué dato te falta.
4. LO QUE FUE BIEN: una o dos cosas.
5. TRES ACCIONES para esta semana, concretas, con quién y para cuándo.
6. UNA PREGUNTA que debería hacerme.

Reglas: no inventes cifras ni causas. Enséñame las cuentas. Importes sin IVA.
Si falta un dato para algún apartado, déjalo en blanco y dime cuál falta.
```

### Paso 2 · Cada lunes (20 min)
La hoja del Panel ya trae la pestaña **Lunes** hecha: no hay que montar nada.

- [ ] Pasa al panel las ventas del domingo y las facturas de la semana.
- [ ] En **Ajustes**, escribe la fecha del lunes de la semana que quieres revisar.
- [ ] Abre la pestaña **Lunes**. Te da, sin tocar nada:
  - Esta semana frente a la anterior: ventas, comensales, ticket medio y rotación.
  - Tus objetivos y la **diferencia en euros**: cuánto has gastado de más en género y en personal, y cuánto ingresas de más o de menos por el ticket medio.
  - La tendencia de las últimas 4 semanas.
- [ ] Exporta del TPV las ventas por plato de la semana.
- [ ] Copia la tabla entera de la pestaña Lunes, pégala en tu proyecto de IA junto con las ventas por plato y escribe: «Haz la revisión de los lunes».

En `ejemplo/panel-ejemplo.xlsx` tienes la pestaña Lunes rellena con **datos inventados**.
- [ ] Lee el informe. **Comprueba dos cifras a mano** con el panel.
- [ ] Elige **una** acción de las tres y hazla esta semana.
- [ ] Guarda el informe en `3-lunes/informes` con la fecha.

### Paso 3 · Lleva el registro de decisiones (2 min)
- [ ] Usa la pestaña **Decisiones** de la hoja del Panel.
- [ ] Cada lunes apunta: fecha, qué viste, qué decidiste y, a la semana siguiente, qué pasó.

Sin este registro repites los mismos lunes. Con él sabes qué cambios funcionaron.

### Paso 4 · Comprueba que está bien (primera vez)
- [ ] El informe no incluye ninguna cifra que no esté en tus datos.
- [ ] Las diferencias en euros cuadran con una cuenta a mano.
- [ ] Las causas que propone tienen sentido para alguien que estuvo en el local esa semana. Si dice que subió la carne y no compraste carne, corrígelo y dile por qué.

## Cómo leer los avisos

| Aviso | Lo primero que hay que mirar |
|---|---|
| Coste de producto por encima del objetivo | Precios de proveedor que subieron, raciones más grandes, mermas, invitaciones y género tirado |
| Coste de personal por encima del objetivo | Horas en turnos flojos, horas extra, cuadrante que no sigue a las ventas |
| Ticket medio a la baja | Menos entrantes, postres o bebida por mesa; más menú que carta |
| Menos comensales | Días concretos, tiempo, reservas, reseñas recientes |
| Rotación baja con el local lleno | Tiempos de cocina, cobro lento, mesas mal aprovechadas |

## Errores frecuentes

- **Hacer las tres acciones a la vez** y no saber cuál funcionó.
- **Juzgar el coste de producto de una semana con el método sencillo.** Una compra grande lo dispara. Mira la tendencia de 4 semanas.
- **Creerse la causa sin comprobarla.** La IA propone; tú, que estuviste allí, confirmas.

## Adáptalo a tu negocio

- **Locales con mucha estacionalidad:** compara con la misma semana del año pasado, no con la anterior.
- **Bares sin comensales registrados:** usa tickets en lugar de comensales y quita la rotación.
- **Varios locales:** una revisión por local y un resumen que los compare.

## Cuando ya lo uses: automatizar

Si tu asistente admite tareas programadas y tu panel está en una hoja conectada, puedes dejar la revisión lista cada lunes a primera hora. Hazlo solo después de 4 lunes a mano: antes no sabrás si el informe automático es bueno.

Siguiente: [04-kit-de-marca.md](04-kit-de-marca.md).
