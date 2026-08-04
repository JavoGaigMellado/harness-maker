---
name: observabilidad
description: Facilita la actividad Registro, feedback y coste de Harness-Maker, resume su estado, recoge decisiones y actualiza el mapa. Invocar manualmente con /observabilidad.
disable-model-invocation: true
---

<!-- GENERADO desde datos/anatomia.json por `harness-lab generate`. NO EDITAR A MANO. -->
# Actividad · Registro, feedback y coste

1. Leer por completo `taller/prompts/13_observabilidad.md` y cumplir su doctrina, criterios y persistencia.
2. Resolver el estado objetivo como indica el prompt e inspeccionar el repositorio antes de preguntar.
3. Mostrar un bloque breve **Estado actual** que incluya:
   - `Ya definido`: respuestas reales y útiles, sin repetir marcadores vacíos;
   - `Falta decidir`: las decisiones todavía pendientes, expresadas en lenguaje normal;
   - `Guardado en`: ruta donde se registrará cada respuesta.
4. Separar hechos observados, inferencias y desconocidos sin convertir esa distinción en un informe largo.
5. No abrir `AskUserQuestion` hasta que ese resumen sea visible.

## Interacción obligatoria

- Contar antes todas las preguntas necesarias y anunciar `Preguntas: N · ventanas: M`, donde cada
  ventana admite hasta cuatro preguntas. No imponer un máximo total.
- Formularlas mediante llamadas consecutivas a `AskUserQuestion`, con hasta cuatro preguntas por
  ventana, dentro de la misma ejecución del comando. No hacer preguntas en texto normal ni obligar
  a la persona a volver a invocar la actividad para recibir las restantes.
- Recoger todas las decisiones necesarias para cerrar la actividad. Reducirlas con lo observado en
  el repositorio, nunca omitiendo una decisión para acortar el cuestionario.
- Usar `multiSelect: true` cuando puedan ser válidas varias opciones de una misma pregunta y
  `multiSelect: false` cuando haya que escoger una sola.
- Preguntar por un hecho o una preferencia del proyecto, nunca por la estructura interna de
  Harness-Maker. No usar en la interfaz palabras como `capa`, `criterio`, `pieza` o `artefacto`.
- Usar un encabezado cercano de dos o tres palabras (`Tu papel`, `Tu equipo`, `Ahora`), no
  uno técnico como `Capa persona`.
- Formular la pregunta en segunda persona, con el nombre del proyecto y sin superar aproximadamente
  140 caracteres.
- Ofrecer entre dos y cuatro opciones breves, concretas y mutuamente distinguibles. Cada título debe
  tener como máximo cinco palabras y su explicación, una sola frase sencilla. La persona también
  puede escribir su respuesta mediante la fila `Other` del selector.
- Resolver una sola decisión por pregunta. No unir el papel de la persona, su autoridad y su forma
  de trabajar dentro de una opción.
- Confirmar la necesidad antes de ofrecer soluciones técnicas. No preguntar cómo construir una API,
  memoria, integración o automatización que el proyecto quizá no necesite.
- No preguntar lo que pueda observarse en el repositorio ni ejecutar cambios antes de recibir todas
  las ventanas del cuestionario.

## Qué cuenta como pendiente

Una etiqueta existente no equivale a una respuesta. Tratar como pendiente todo texto que indique
`no está definido`, `no existe`, `parcial`, `pendiente` o `por decidir`, además de los campos ausentes.
Mostrarlo bajo `Falta decidir`, nunca bajo `Ya definido`.



## Rondas de impacto dentro del mismo comando

Después de cada bloque de respuestas, contrastar lo confirmado con las 18 actividades antes de
cerrar o regenerar:

1. Si aparece un impacto que invalida o deja incompleta otra actividad, mostrar primero
   `Impacto detectado · <actividad>` y explicar en una frase qué cambió y qué falta decidir.
2. Inspeccionar esa actividad y resolver sin preguntar lo que demuestren el repositorio y las
   respuestas ya confirmadas. No volver a preguntar decisiones vigentes.
3. Si quedan decisiones que solo puede tomar la persona, anunciar
   `Preguntas adicionales por impacto: N · ventanas: M` y formularlas inmediatamente mediante
   llamadas consecutivas a `AskUserQuestion`, dentro de esta misma ejecución.
4. Volver a revisar las respuestas adicionales contra las 18 actividades. Repetir la ronda si
   abren otro impacto confirmable; agrupar los impactos relacionados y evitar preguntas duplicadas.

No pedir que se ejecute después `/<actividad-afectada>`. Si el impacto queda resuelto ahora,
actualizar y volver a verificar esa actividad sin dejarla en rojo. Solo dejarla `en_curso` cuando
requiera trabajo o evidencia externa, falte autoridad, la persona decida posponerlo o una respuesta
siga realmente pendiente; registrar y explicar la causa concreta.

## Alcance de la actividad

- Las respuestas definen el resultado; no autorizan por sí solas una refactorización. Sí se permite
  actualizar otra actividad cuando una afirmación confirmada cambie directamente su definición.
- Sin una acción preparada por el prompt y aceptada expresamente en el cuestionario, limitar las
  escrituras al estado, `cobertura.json`, el Markdown de la actividad y sus derivados generados.
- Si al hacer la actividad se ve que el taller mismo debería cambiar —los prompts de
  `taller/prompts/`, las skills, el generador o `diagramas/diagrama_taller.html`—, mirar antes de qué
  copia se trata. En la copia de desarrollo, la que tiene `proyectos/harness-lab/`, cambiarlo en el
  momento y decir al cerrar qué se tocó y por qué: es la fase 2, y mejorarla mientras se usa es el
  objetivo, no un efecto lateral. En una copia recibida, no: el taller llega por `git pull`, y
  editarlo allí deja archivos versionados modificados que chocan con la siguiente actualización, que
  es justo lo que hace llegar los arreglos. Proponer la mejora, anotarla en el recorrido y decir que
  se traslade a quien mantiene el proyecto.
- No modificar `datos/anatomia.json`, los esquemas ni `diagramas/diagrama_base.html`, que son la
  doctrina. Si se descubre que debería cambiar, proponerlo en el mismo cuestionario y esperar la
  confirmación de la persona antes de tocarlos.
- Si el prompt contiene una acción que requiere confirmación, incluir `¿Quieres que lo deje
  implementado ahora?` entre las preguntas del cuestionario.

## Tras recibir el cuestionario

1. Preparar conjuntamente solo lo confirmado, sin escribir todavía el cierre definitivo.
   Si una respuesta escrita mediante `Other` cuestiona la pregunta, dice que no se entiende o
   rechaza su premisa, tratarla como corrección del diagnóstico: no convertirla en una elección ni
   cerrar el punto. Reinspeccionar la necesidad y explicar el nuevo encuadre.
2. Mantener las decisiones como `Etiqueta — contenido` y sustituir la etiqueta existente en vez de
   acumular definiciones contradictorias.
3. Revisar cada respuesta completa contra las 18 actividades, no solo contra la actividad abierta.
   Informar siempre `Impacto en el resto: ninguno` o enumerar las actividades afectadas y el motivo.
   Aplicar las rondas de impacto anteriores antes de persistir. Una posible relación todavía no
   confirmada se explica, pero no se persiste como hecho.
4. Fusionar entonces la actividad original y las afectadas en el estado y en sus Markdown sin
   destruir claves ajenas. Añadir o sustituir en `decisiones_globales` una entrada estable
   `impacto-<origen>-<destino>` cuyo `pieza_id` sea el destino. Reabrir una actividad cerrada solo
   cuando la ronda no haya podido resolver el impacto, vaciando su fecha de cierre y marcando como
   parciales únicamente los criterios afectados.
5. Actualizar `cobertura.json` cuando exista junto al estado, tanto para la actividad abierta como
   para cualquier actividad afectada.
   Si junto al estado existe `AUDITORIA.md`, sincronizar también su recuento, el resumen legible de
   las actividades modificadas y la siguiente actividad; sigue siendo una vista, nunca una fuente.
6. Revisar el estado completo. Si lo aprendido cambia un eje del diagnóstico, actualizar ese eje
   con su evidencia y ejecutar `harness-lab plan --state <ruta-del-estado>
   --output <ruta-del-estado>` para recalcular únicamente el tramo pendiente con reglas declaradas.
7. Ejecutar `harness-lab generate` para refrescar wrappers y, después,
   `harness-lab validate --state <ruta-del-estado>`.
8. Responder con la estructura de explicación indicada abajo, incluyendo qué se guardó, qué puede
   hacer ahora el harness, el impacto y la siguiente actividad. Invitar a probarlo con un encargo
   real cuando aporte una comprobación útil.

## Explicación adaptada a la persona

Buscar en Contexto una decisión `Perfil de interacción`. Si no existe, usar **Simple y guiado**:

- `Simple y guiado` — explicar el resultado y la próxima acción con palabras cotidianas. No poner
  rutas, nombres de funciones, pruebas ni detalles de implementación en la conclusión principal.
- `Breve y directo` — dar estado, decisiones, capacidad y siguiente paso sin explicación didáctica.
- `Técnico y detallado` — incluir además archivos, implementación, comprobaciones y riesgos.

El nivel describe cómo presentar la información, no la capacidad de la persona. Cambiarlo cuando lo
pida explícitamente y guardar entonces la preferencia confirmada en Contexto; no convertir una sola
pregunta técnica en un cambio de perfil.

Cerrar siempre con esta estructura y en este orden:

1. `Actividad completada: <nombre>` o `Actividad en curso: <nombre>`.
2. **En una frase** — qué se acaba de conseguir, sin jerga.
3. **Lo que decidiste** — lista breve; separar lo confirmado por la persona de lo observado o
   implementado automáticamente.
4. **Qué cambia para ti** — consecuencia práctica al usar el harness.
5. **Tu harness ahora puede** — una sola frase acumulativa y comprensible.
6. **Qué queda** — número de actividades resueltas y abiertas, y siguiente actividad explicada en
   lenguaje normal. En `/lote`, añadir cuántas se intentaron y cuántas se cerraron realmente.
7. **Impacto en otras partes** — decir `Ninguno` o nombrarlas con una frase práctica por cada una.
8. **Detalles técnicos** — solo si el perfil es técnico, la persona los pide o necesita actuar ante
   un fallo. Resumir rutas, pruebas y riesgos; no narrar refactorizaciones ni decir que «las pruebas
   mentían» en la explicación principal.

No pegar un informe interno largo. Un riesgo que afecte a la persona sí se explica, pero primero en
lenguaje normal y después, si hace falta, con su causa técnica.

No marcar la actividad como completada hasta satisfacer todos los criterios del prompt.
