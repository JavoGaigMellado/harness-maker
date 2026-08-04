---
name: cierre
description: Revisa el cierre de un recorrido de Harness-Maker, resume pendientes y consolida el estado final. Invocar manualmente con /cierre.
disable-model-invocation: true
---

<!-- GENERADO por `harness-lab generate`. NO EDITAR A MANO. -->
# Cierre de Harness-Maker

1. Leer por completo `taller/prompts/99_cierre_y_replanificacion.md`.
2. Resolver el estado objetivo, inspeccionarlo y mostrar un **Estado actual** breve con piezas
   cerradas, pendientes, deudas y ruta de persistencia.
3. Contar todas las decisiones pendientes y anunciar `Preguntas: N · ventanas: M`. Formularlas con
   llamadas consecutivas a `AskUserQuestion`, hasta cuatro por ventana y sin máximo total en esta
   ejecución; usar entre dos y cuatro opciones, `multiSelect` cuando corresponda y `Other`.
4. Tras recibir todas las ventanas, persistir el avance, regenerar con
   `harness-lab generate`, validar el estado y responder con la estructura indicada.

No cerrar por mera conversación ni hacer preguntas en texto normal.

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
   lenguaje normal.
7. **Impacto en otras partes** — decir `Ninguno` o nombrarlas con una frase práctica por cada una.
8. **Detalles técnicos** — solo si el perfil es técnico, la persona los pide o necesita actuar ante
   un fallo. Resumir rutas, pruebas y riesgos; no narrar refactorizaciones ni decir que «las pruebas
   mentían» en la explicación principal.

No pegar un informe interno largo. Un riesgo que afecte a la persona sí se explica, pero primero en
lenguaje normal y después, si hace falta, con su causa técnica.
