# 5 · Biblioteca de reseñas

**Qué es:** todas tus reseñas en una sola tabla, ordenadas por tema.
**Para qué sirve:** ver qué problemas se repiten, arreglarlos y responder a todo el mundo.

**El problema que resuelve:** tus clientes ya te dijeron qué falla. Está repartido entre Google, TripAdvisor y las plataformas de reservas y reparto, y nadie lo ha leído todo junto.

## La tabla

| Columna | Qué es |
|---|---|
| Fecha | Día de la reseña |
| Plataforma | Google, TripAdvisor, reservas, reparto, redes |
| Estrellas | De 1 a 5 |
| Texto | La reseña, copiada tal cual |
| Tema principal | Uno de la lista de abajo |
| Tema secundario | Si lo hay |
| Sentimiento | Positiva, negativa o mixta |
| Respondida | Sí o no |
| Acción | Qué se hizo, si procede |

**Temas** (usa siempre los mismos):
comida · servicio · tiempo de espera · precio · ambiente y ruido · limpieza · reservas · reparto · otros

## Checklist

### Paso 1 · Recoge las reseñas (45 min)
- [ ] Lista las plataformas donde tienes reseñas.
- [ ] Copia las reseñas de los **últimos 12 meses**. Si tienes más de 200, empieza por los últimos 6 meses.
- [ ] Formas de hacerlo, de más fácil a menos:
  - Copiar y pegar el texto de cada plataforma en un documento.
  - Desde el panel de gestión de cada plataforma, si permite exportar.
  - Capturas de pantalla, y que tu asistente de IA las pase a texto.
- [ ] **Copia el texto, la fecha y las estrellas. No hace falta el nombre de quien escribe.**

### Paso 2 · Monta la tabla (30 min)
- [ ] Copia `plantillas/resenas.xlsx` a la carpeta `5-resenas` con el nombre `Reseñas - [tu local]`. En **Ajustes** pon la fecha de hoy.
- [ ] Abre antes `ejemplo/resenas-ejemplo.xlsx` para ver cómo queda. **Sus reseñas son inventadas.**
- [ ] Sube las reseñas a tu proyecto de IA y pega:

```
Te paso las reseñas de mi restaurante. Pásalas a una tabla con estas columnas:
fecha, plataforma, estrellas, texto, tema principal, tema secundario, sentimiento.

Temas permitidos, solo estos: comida, servicio, tiempo de espera, precio,
ambiente y ruido, limpieza, reservas, reparto, otros.
Sentimiento: positiva, negativa o mixta.

Reglas: copia el texto tal cual, sin resumir ni corregir. No añadas reseñas.
Quita los nombres de las personas. Si no sabes el tema, pon «otros».
Al final dime cuántas reseñas has procesado, para comprobar que no falta ninguna.
```

- [ ] Comprueba que el número de reseñas coincide con las que copiaste.
- [ ] Pega la tabla en la pestaña **Reseñas**. Tema, sentimiento y «respondida» tienen desplegable: revisa que cada valor sea uno de la lista.
- [ ] Abre la pestaña **Resumen**. Sin tocar nada te da:
  - Total de reseñas, media de estrellas y cuántas están sin responder.
  - Por tema: cuántas reseñas, cuántas con problema, su puesto (1, 2 y 3 son tus tres problemas principales) y si **va a más o a menos** en los últimos 90 días.
  - Por plataforma: reseñas, media y sin responder.

### Paso 3 · Encuentra lo que se repite (20 min)
La hoja ya te dice **cuáles** son los problemas. El asistente de IA te ayuda a ver **qué dicen exactamente** los clientes.

- [ ] Apunta los temas con puesto 1, 2 y 3 del Resumen.
- [ ] Con la tabla subida al proyecto, pide:

```
Con mi tabla de reseñas:
1. Cuántas reseñas hay por tema y cuántas son negativas o mixtas en cada uno.
2. Los 3 problemas que más se repiten, cada uno con 3 frases literales de clientes y sus fechas.
3. Las 3 cosas que más elogian, con frases literales.
4. ¿Algún problema ha empezado o empeorado en los últimos 3 meses?
5. ¿Qué días de la semana concentran las quejas, si se puede saber?
Cita siempre frases reales de la tabla. No inventes ninguna.
```

- [ ] Busca en la tabla dos de las frases citadas. Tienen que existir tal cual.
- [ ] Escribe tus **3 problemas principales** y, para cada uno, una acción con responsable y fecha.
- [ ] Apunta esas acciones en el registro de decisiones de la [Revisión de los lunes](03-revision-de-los-lunes.md).

### Paso 4 · Responde a todas (30-60 min la primera vez)
- [ ] Sube tu [ficha de marca](04-kit-de-marca.md) al proyecto para que use tu tono.
- [ ] Guarda esta instrucción:

```
Escribe una respuesta para cada reseña sin responder, con mi tono de la ficha de marca.

Reglas:
- Corta: de 2 a 4 frases.
- Menciona algo concreto de lo que dice la persona.
- Si es negativa: agradece, reconoce lo ocurrido sin excusas y di qué vamos a hacer
  o invita a escribirnos a [correo o teléfono].
- No prometas compensaciones ni des datos que yo no te haya dado.
- No discutas ni culpes al cliente ni al equipo.
- No repitas la misma fórmula en dos respuestas seguidas.
- Si la reseña habla de una intoxicación, una alergia, un accidente o un trato
  discriminatorio, NO escribas respuesta: márcala como «REVISAR EN PERSONA».
```

- [ ] **Lee cada respuesta antes de publicarla.** Corrige lo que no sea verdad.
- [ ] Publica y marca «Respondida: sí» en la tabla.
- [ ] Las marcadas «REVISAR EN PERSONA» las contestas tú, con calma y, si hace falta, con asesoramiento.

### Paso 5 · Comprueba que está bien (10 min)
- [ ] El total de reseñas de la tabla coincide con lo recogido.
- [ ] Abre 10 reseñas al azar: el tema asignado es correcto en al menos 8.
- [ ] No queda ninguna reseña de los últimos 30 días sin responder.

## Mantenimiento

| Cuándo | Qué | Tiempo |
|---|---|---|
| Cada semana | Añadir las reseñas nuevas, clasificarlas y responderlas | 20 min |
| Cada mes | Repetir el análisis del paso 3 y ver si los 3 problemas mejoran | 20 min |
| Cada 3 meses | Enseñar al equipo los elogios y los problemas, con frases reales | 30 min |

## Lo que no se hace

- **No escribas reseñas falsas** ni pidas a conocidos que las escriban.
- **No ofrezcas regalos o descuentos a cambio de reseñas.** Las plataformas lo prohíben y puede traerte problemas.
- **No publiques respuestas sin leerlas.**
- **No reveles datos del cliente** en la respuesta (lo que pidió, con quién vino, cuánto pagó).

## Errores frecuentes

- **Responder solo a las malas.** Quien te elogia también espera respuesta.
- **Copiar la misma respuesta en todas.** Se nota y queda peor que no responder.
- **Leer las reseñas y no cambiar nada.** El valor está en las 3 acciones del paso 3.

## Adáptalo a tu negocio

- **Pocas reseñas (menos de 30):** no te fíes de los porcentajes ni de «va a más»: con tan pocas, una sola reseña cambia el resultado. Lee todas y agrupa a mano.
- **Reparto:** añade los temas «temperatura del pedido» y «pedido incompleto».
- **Varios locales:** añade la columna «local» y compara los temas entre ellos.

Has terminado las 5 herramientas. Vuelve al [README](README.md).
