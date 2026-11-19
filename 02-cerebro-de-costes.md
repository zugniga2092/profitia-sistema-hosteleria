# 2 · Cerebro de costes

**Qué es:** un sitio único con los precios de tus proveedores y tus recetas, al que le preguntas cuánto deja cada plato.
**Para qué sirve:** saber el margen real de cada plato hoy, no el del día que hiciste el escandallo.

**El problema que resuelve:** el escandallo se queda viejo. El proveedor sube el precio, cambia el formato de la caja o la ración que sale de cocina pesa más que la de la receta, y tú sigues creyendo que el plato deja lo mismo.

## Las dos tablas

**Ingredientes** (una fila por ingrediente):

| Columna | Qué es | Ejemplo |
|---|---|---|
| Ingrediente | Nombre, siempre escrito igual | Lomo de ternera |
| Proveedor | Quién te lo vende | — |
| Formato de compra | Cómo viene | Pieza de 4 kg |
| Precio del formato | Sin IVA | 72,00 € |
| Unidad de uso | kg, litro o unidad | kg |
| Precio por unidad | Precio ÷ cantidad del formato | 18,00 €/kg |
| Merma % | Lo que se pierde al limpiar y cocinar | 20 % |
| Precio real por unidad | Precio por unidad ÷ (1 − merma) | 22,50 €/kg |
| Fecha del precio | Última factura | 12/11/2026 |

**Escandallos** (una fila por ingrediente de cada plato):

| Columna | Qué es |
|---|---|
| Plato | Nombre como en la carta |
| Ingrediente | Igual que en la tabla de ingredientes |
| Cantidad por ración | Lo que llega al plato, ya limpio, en la unidad de uso |
| Coste | Cantidad × precio real por unidad |

**Por plato:**
- **Coste de la ración** = suma de los costes de sus ingredientes.
- **Precio sin IVA** = precio de carta ÷ 1,10 (la restauración tributa, con carácter general, al 10 %; confírmalo con tu gestor).
- **Margen en euros** = precio sin IVA − coste de la ración.
- **Coste de producto %** = coste de la ración ÷ precio sin IVA × 100.

## Checklist

### Paso 1 · Elige por dónde empezar (15 min)
No hagas toda la carta de golpe.
- [ ] Saca del TPV las ventas por plato del último mes.
- [ ] Elige los **10 platos más vendidos**. Suelen ser la mayor parte de tus ventas.
- [ ] Añade los 3 platos que sospeches que dejan poco.

### Paso 2 · Rellena los ingredientes (1-2 h)
La hoja ya está hecha: `plantillas/costes.xlsx`. Las celdas grises se calculan solas.

- [ ] Copia `plantillas/costes.xlsx` a tu carpeta `2-costes` con el nombre `Costes - [tu local]`.
- [ ] Abre antes `ejemplo/costes-ejemplo.xlsx` para ver una hoja completa. **Sus datos son inventados.**
- [ ] Pestaña **Ajustes**: nombre, tu objetivo de coste de producto y la fecha de hoy.
- [ ] Pestaña **Ingredientes**: una fila por ingrediente de esos 13 platos, incluidos aceite, sal, guarnición, pan y salsas. Rellena proveedor, formato, precio del formato sin IVA, cantidad del formato, unidad y fecha, **con la última factura, no de memoria**. El precio por unidad y el precio real salen solos.

Para ir más rápido, sube fotos o PDF de las facturas a tu proyecto de IA y pega:

```
Te paso facturas de proveedores. Saca una tabla con: ingrediente, proveedor,
formato de compra, precio del formato sin IVA, cantidad del formato, unidad (kg, litro o unidad)
y fecha de la factura.
Si un dato no se lee bien, márcalo con «REVISAR» en vez de suponerlo.
No inventes ningún precio.
```

- [ ] Revisa una a una las filas marcadas con «REVISAR» antes de pegarlas en la hoja.
- [ ] **Mide tus mermas.** Para cada ingrediente principal, pesa antes de limpiar y después de cocinar, una vez, y apunta el porcentaje. Mientras no la midas, deja la celda vacía: la hoja pone el aviso «Falta medir la merma» y calcula sin merma. No copies una merma de internet.
- [ ] Mira la columna **Aviso**: te dice si falta un dato o si un precio tiene más de 60 días.

### Paso 3 · Rellena los escandallos (1-2 h)
- [ ] Pestaña **Escandallos**: una fila por cada ingrediente de cada plato. El ingrediente se elige de un desplegable, así siempre se escribe igual.
- [ ] En «Cantidad por ración» pon lo que llega al plato, ya limpio, en la unidad del ingrediente (0,300 para 300 g).
- [ ] Si un ingrediente sale en rojo como «SIN PRECIO», falta en la pestaña Ingredientes o le falta el precio.
- [ ] Pestaña **Platos**: escribe el nombre de cada plato **exactamente igual** que en Escandallos, su precio de carta con IVA y, si lo sabes, las raciones vendidas al mes.
- [ ] La hoja te da, por plato: precio sin IVA, coste de la ración, margen en euros, coste de producto %, si cumple tu objetivo y el margen que deja al mes.

### Paso 4 · La prueba de las 5 raciones (30 min, en un servicio)
Es lo que separa el coste de papel del coste real.
- [ ] Para tus 5 platos más vendidos, pesa el ingrediente principal de **5 raciones reales** tal como salen al pase.
- [ ] Calcula la media y compárala con la cantidad del escandallo.
- [ ] Si la media real es mayor, tienes dos caminos: corregir el escandallo o corregir la ración en cocina. Decide cuál y apúntalo.

### Paso 5 · Pregúntale (15 min)
- [ ] Sube la hoja a tu proyecto de IA y prueba estas preguntas:

```
1. Ordena mis platos de mayor a menor margen en euros.
2. ¿Qué platos superan mi objetivo de coste de producto del [tu objetivo] %?
3. Si [ingrediente] sube un [X] %, ¿qué platos cambian y cuánto margen pierdo al mes
   con las ventas del último mes?
4. ¿Qué plato vendo mucho y me deja poco? ¿Y cuál deja mucho y vendo poco?
Enséñame la cuenta de cada respuesta.
```

### Paso 6 · Comprueba que está bien (20 min)
- [ ] Elige **3 platos** y calcula su coste a mano, con calculadora. Debe coincidir con la hoja.
- [ ] Comprueba que todos los precios están sin IVA.
- [ ] Mira que no haya ingredientes escritos de dos formas («tomate» y «tomates»): se cuentan como dos.

## Mantenimiento

| Cuándo | Qué | Tiempo |
|---|---|---|
| Cada vez que llega una factura con un precio distinto | Actualizar precio y fecha | 2 min |
| Cada mes | Revisar precios con más de 60 días; añadir 5 platos nuevos | 30 min |
| Cada cambio de carta | Escandallo del plato nuevo antes de ponerle precio | 15 min |
| Cada 3 meses | Repetir la prueba de las 5 raciones | 30 min |

## Errores frecuentes

- **Olvidar lo pequeño:** aceite, pan, salsas, decoración y envases de reparto. Sumados pesan.
- **Usar el peso bruto como ración.** La ración es lo que llega al plato.
- **No cambiar el precio por unidad cuando cambia el formato.** La caja cuesta lo mismo pero trae menos.
- **Mirar solo el porcentaje.** Un plato con coste del 40 % puede dejar más euros que uno del 25 %. Mira las dos cosas.

## Adáptalo a tu negocio

- **Bar de copas y coctelería:** el escandallo es por copa (centilitros de cada botella). La merma es el derrame y las invitaciones.
- **Cafetería:** incluye leche, azúcar, vaso y tapa en cada café para llevar.
- **Menú del día:** haz el escandallo del menú completo (primero, segundo, postre, pan y bebida), no plato a plato.
- **Reparto:** suma el envase y la comisión de la plataforma al coste.

Siguiente: [03-revision-de-los-lunes.md](03-revision-de-los-lunes.md).
