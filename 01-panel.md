# 1 · Panel del restaurante

**Qué es:** una sola página con los números que mandan en tu negocio.
**Para qué sirve:** saber cada semana y cada mes si ganas o pierdes, y por qué.

## Los 8 números del panel

| Número | Cómo se calcula | Qué te dice |
|---|---|---|
| **Ventas** | Suma de ventas sin IVA | Cuánto entra |
| **Comensales** | Personas atendidas | Cuánta gente viene |
| **Ticket medio** | Ventas ÷ comensales | Cuánto gasta cada persona |
| **Coste de producto %** | Consumo de género ÷ ventas × 100 | Cuánto de cada euro se va en comida y bebida |
| **Coste de personal %** | Coste total de personal ÷ ventas × 100 | Cuánto de cada euro se va en el equipo |
| **Margen bruto** | Ventas − coste de producto | Lo que queda después de pagar el género |
| **Coste principal %** | Coste de producto % + coste de personal % | Los dos gastos grandes juntos |
| **Resultado de explotación (EBITDA)** | Ventas − producto − personal − gastos generales | Lo que deja el negocio antes de amortizaciones, intereses e impuestos |

**Consumo de género.** Hay dos formas de calcularlo:
- **Sencilla (para empezar):** compras del periodo. Vale para ver el mes, no para una semana suelta, porque una compra grande lo descuadra.
- **Exacta:** inventario inicial + compras − inventario final. Necesita contar el almacén al empezar y al acabar el periodo.

## Checklist

### Paso 1 · Reúne los datos (1 h)
- [ ] Saca del TPV las ventas diarias sin IVA de los **últimos 3 meses**, con comensales y número de tickets. Si tu TPV no registra comensales, usa tickets y anótalo.
- [ ] Reúne todas las facturas de proveedores de esos 3 meses. Separa **comida**, **bebida** y **otros** (limpieza, menaje, envases).
- [ ] Pide a tu gestoría el **coste total de personal** de cada mes: sueldos brutos más la seguridad social a cargo de la empresa.
- [ ] Apunta tus gastos generales del mes: alquiler, suministros, seguros, gestoría, cuotas, comisiones de reparto y de tarjetas, mantenimiento, marketing.

### Paso 2 · Monta la hoja (30 min)
La hoja ya está hecha: solo tienes que rellenarla.

- [ ] Copia `plantillas/panel.xlsx` a tu carpeta `1-panel` y ponle el nombre `Panel - [tu local]`. Se abre con Excel; para Google Sheets, súbela a Drive y ábrela desde allí.
- [ ] Antes de rellenar nada, abre `ejemplo/panel-ejemplo.xlsx` para ver cómo queda un panel completo. **Sus datos son inventados**: es un restaurante que no existe.
- [ ] Pestaña **Ajustes**: rellena las celdas amarillas (nombre, plazas, objetivos, el lunes de la semana que quieres ver y el día 1 del mes).
- [ ] Pestaña **Ventas**: una fila por día y turno, con fecha, ventas sin IVA, comensales y tickets.
- [ ] Pestaña **Compras**: una fila por factura. En «Categoría» elige `comida`, `bebida` u `otros` del desplegable. Solo comida y bebida cuentan como género.
- [ ] Pestaña **Mes**: una fila por concepto y mes. La fecha es siempre el día 1 del mes. En «Tipo» elige `personal` o `gasto general`.
- [ ] Pestaña **Panel**: no escribas nada. Se calcula sola y te avisa abajo si falta algún dato.

**Cómo leer la columna «Semana».** Ventas, comensales y ticket medio son exactos. El coste de producto de la semana es orientativo (una compra grande lo descuadra) y el de personal es una estimación: reparte el coste del mes por días. Para decidir, fíate de la columna «Mes».

Si prefieres hojas sueltas, tienes las mismas tablas en CSV: `ventas-diarias.csv`, `compras.csv` y `personal-y-gastos.csv`.

### Paso 3 · Fija tus objetivos (15 min)
- [ ] Calcula tus porcentajes reales de los últimos 3 meses. **Ese es tu punto de partida.**
- [ ] Pon tu objetivo al lado de cada número. Mira los rangos orientativos de [REFERENCIAS.md](REFERENCIAS.md), pero decide con tus cifras: un asador y un bar de tapas no tienen el mismo coste de producto.
- [ ] Colorea: verde si cumples el objetivo, rojo si no.

### Paso 4 · El resumen de la mañana (15 min)
Empieza a mano. Automatizarlo viene después, cuando ya uses el panel.

- [ ] Cada mañana, pega en tu proyecto de IA el cierre de caja de ayer y esto:

```
Este es el cierre de ayer. Dame el resumen de la mañana en 5 líneas:
1. Ventas de ayer y comparación con el mismo día de la semana pasada.
2. Comensales y ticket medio.
3. Cómo va la semana frente a la anterior.
4. Lo que más llama la atención, bueno o malo.
5. Una cosa que revisar hoy.
```

- [ ] Guarda el resumen en la carpeta `1-panel/resumenes`.

### Paso 5 · Comprueba que está bien (15 min)
- [ ] Elige un día y suma sus ventas a mano con el cierre de caja. Debe coincidir con la hoja.
- [ ] Compara las ventas del mes de la hoja con las de tu gestoría. Si no cuadran, busca la diferencia antes de seguir (lo habitual: IVA mezclado, propinas o un día sin pasar).
- [ ] Revisa que ningún porcentaje sea absurdo (coste de producto del 5 % o del 80 %). Si lo es, falta o sobra una factura.

## Mantenimiento

| Cuándo | Qué | Tiempo |
|---|---|---|
| Cada día | Pasar ventas y comensales de ayer | 3 min |
| Cada semana | Pasar las facturas de la semana | 15 min |
| Cada mes | Pasar personal y gastos generales; revisar el mes | 30 min |

## Errores frecuentes

- **Mezclar importes con y sin IVA.** Es el fallo más común.
- **Contar como coste de personal solo el sueldo neto.** Falta la seguridad social y las pagas extra prorrateadas.
- **Olvidar tu propio sueldo.** Si trabajas en el local y no te pones sueldo, el resultado sale mejor de lo que es.
- **Mirar una semana suelta con el método sencillo.** Una compra grande la distorsiona.

## Adáptalo a tu negocio

- **Bar de copas o cafetería:** separa bebida y comida. Sus márgenes son muy distintos.
- **Reparto y comida para llevar:** añade las comisiones de las plataformas como gasto y mira el ticket medio por canal.
- **Menú del día:** separa las ventas de menú de las de carta.
- **Varios locales:** una hoja por local y una pestaña que las sume.

## Cuando ya lo uses: automatizar

Solo cuando lleves un mes usándolo a mano. Opciones, de menos a más trabajo: exportación programada del TPV a la hoja, conexión del TPV con Google Sheets, o un informe automático por correo. Depende de tu TPV: pregunta a su soporte si exporta ventas diarias de forma automática.

Siguiente: [02-cerebro-de-costes.md](02-cerebro-de-costes.md).
