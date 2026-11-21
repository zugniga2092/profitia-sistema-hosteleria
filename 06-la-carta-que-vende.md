# 6 · La carta que vende

**Qué es:** tu carta ordenada según lo que deja y lo que se vende cada plato, y reescrita para que el cliente elija lo que te conviene.
**Para qué sirve:** ganar más con los mismos clientes, sin subir todos los precios ni cambiar la cocina entera.

**El problema que resuelve:** la carta se hace una vez y se queda así. Hay platos que se venden mucho y casi no dejan nada, platos que dejan mucho y nadie pide, y platos que ocupan sitio sin aportar. Sin datos, se decide por intuición.

**Necesitas antes:** el Cerebro de costes (herramienta 2) con el margen de cada plato y las raciones vendidas al mes.

## Los cuatro grupos

La pestaña **Carta** de `costes.xlsx` compara cada plato con los de **su misma sección** (entrantes con entrantes, principales con principales). Usa el método de ingeniería de menús de Kasavana y Smith (1982), el más usado en hostelería:

- **Muy vendido:** su parte de las ventas de la sección llega al 70 % de lo que le tocaría si todos se vendieran igual.
- **Deja mucho:** su margen por ración llega al margen medio de la sección, contando cuánto se vende cada plato.

| Grupo | Qué es | Qué hacer |
|---|---|---|
| **Estrella** | Muy vendido y deja mucho | Protégelo: buen sitio en la carta, misma ración, misma calidad. No lo toques por tocar. |
| **Muy vendido, deja poco** | Lo piden mucho, pero gana poco | Mejora su margen: revisa ración y coste, o súbelo poco a poco. Gusta, así que aguanta subidas pequeñas. |
| **Deja mucho, se vende poco** | Ganas mucho con él, pero casi nadie lo pide | Dale visibilidad: mejor sitio, mejor descripción, que el equipo lo recomiende. |
| **Se vende poco y deja poco** | Ni se pide ni deja | Cámbialo o quítalo, salvo que tenga un motivo para estar (por ejemplo, la opción vegana). |

## Checklist

### Paso 1 · Prepara los datos (15 min)
- [ ] Abre tu `Costes - [tu local].xlsx` y comprueba en la pestaña **Platos** que cada plato tiene precio, escandallo y **raciones vendidas al mes** (del TPV, último mes completo).
- [ ] Si tu hoja es anterior a la pestaña **Carta**, copia tus pestañas a la plantilla nueva `plantillas/costes.xlsx`.
- [ ] Pestaña **Carta**: en la columna amarilla escribe la **sección** de cada plato, igual que en tu carta (Entrantes, Principales, Postres…). Si la dejas vacía, la hoja compara toda la carta junta.
- [ ] Abre `ejemplo/costes-ejemplo.xlsx` para ver los cuatro grupos con un restaurante inventado.

### Paso 2 · Lee los grupos (20 min)
- [ ] Mira la columna **Grupo** y apunta en una lista cuántos platos tienes de cada uno.
- [ ] Una sección con un solo plato no se puede comparar: la hoja lo avisa. Júntala con otra parecida si quieres verla.
- [ ] Ojo con los platos nuevos: con menos de un mes en carta, sus ventas aún no dicen nada.

### Paso 3 · Decide qué hacer con cada plato (30 min)
Con la hoja subida a tu proyecto de IA, pega:

```
Te paso mi hoja de costes con la pestaña Carta. Para cada plato, dime:
1. Su grupo y por qué (con sus números).
2. Una acción concreta según su grupo, pensada para mi restaurante.
3. Para los «Muy vendido, deja poco»: cuánto margen ganaría al mes si subo 0,50 € o 1 €,
   o si bajo su coste un 10 %, con las raciones actuales. Enséñame la cuenta.
No propongas cambios en platos que no estén en la hoja. No inventes datos.
```

- [ ] Elige **3 cambios como máximo** para este mes. Si cambias todo a la vez, no sabrás qué funcionó.
- [ ] Apunta cada cambio en la pestaña **Decisiones** del Panel, con la fecha.

### Paso 4 · Reescribe la carta (1 h)
La carta se lee deprisa y no entera. Ordénala para que lo primero que se vea sea lo que te conviene:
- [ ] **Cada sección empieza por una estrella o por un plato que deja mucho**, no por el más barato.
- [ ] **Los que dejan mucho y se venden poco**, con un recuadro, una marca de «recomendado» o una descripción más rica. Uno o dos por sección; si destacas todo, no destaca nada.
- [ ] **Descripciones que abren el apetito y dicen la verdad:** origen, cómo se cocina, qué lo hace distinto. Nada de «delicioso» ni «exquisito».
- [ ] **Precios con el IVA incluido**, como exige la normativa de consumo.
- [ ] **No pongas los precios en una columna alineada:** invita a elegir por precio. Ponlos al final de la descripción.
- [ ] **Alérgenos:** la información de los 14 alérgenos es obligatoria (Reglamento UE 1169/2011). Puede ir en la carta o en un documento a disposición del cliente; confírmalo con tu asesor.

Para los textos, pega:

```
Con mi ficha de marca (tono) y estos platos, escribe una descripción de máximo 20 palabras para cada uno.
Di de dónde viene el producto y cómo se cocina, solo si está en mis datos.
Nada de «delicioso», «exquisito» ni «el mejor». Si te falta un dato, pon [PREGUNTAR].
Platos: [pega la lista con lo que sepas de cada uno].
```

### Paso 5 · Comprueba que funcionó (un mes después, 20 min)
- [ ] Pon las raciones del nuevo mes en la hoja y mira si los platos cambiaron de grupo.
- [ ] Compara el margen total al mes (pestaña Platos) con el del mes anterior.
- [ ] Si un cambio no movió nada en un mes, prueba otro distinto.

## Mantenimiento

| Cuándo | Qué | Tiempo |
|---|---|---|
| Cada mes | Raciones vendidas en la hoja y mirar los grupos | 20 min |
| Cada cambio de carta | Escandallo y sección de los platos nuevos | 15 min |
| Cada 3 meses | Revisión completa: qué platos quitar, cuáles destacar | 1 h |

## Errores frecuentes

- **Quitar un plato solo por el número.** Algunos están por un motivo: la opción sin gluten, el plato de los niños.
- **Comparar platos de secciones distintas.** Un postre siempre deja menos euros que un principal.
- **Subir de golpe un plato muy vendido.** Mejor poco a poco, o revisar la ración y el coste.
- **Cambiarlo todo a la vez.** Tres cambios, un mes, y mirar.

## Adáptalo a tu negocio

- **Bar de copas:** las secciones son tus tipos de bebida (cócteles, vinos, cervezas).
- **Cafetería:** separa bebidas y comida; el café suele ser una estrella.
- **Menú del día:** analízalo como un solo plato, y los platos a la carta aparte.
- **Reparto:** usa el margen después de la comisión de la plataforma.

Siguiente: [07-asistente-de-redes.md](07-asistente-de-redes.md).
