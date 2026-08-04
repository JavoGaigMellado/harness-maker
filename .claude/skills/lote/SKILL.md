---
name: lote
description: Resuelve varias actividades abiertas de Harness-Maker en una sola ejecución, pregunta todo lo necesario en ventanas consecutivas, respeta dependencias y muestra cuántas intentará y cuántas quedarán. Invocar manualmente con /lote.
disable-model-invocation: true
---

<!-- GENERADO por `harness-lab generate`. NO EDITAR A MANO. -->
# Avance por lote

1. Resolver el estado objetivo e inspeccionar `datos/anatomia.json`, `cobertura.json` y el
   repositorio. No modificar la anatomía, los esquemas ni el diagrama base.
2. Fijar el alcance:
   - `/lote` sin argumentos intenta resolver **todas las actividades abiertas**.
   - `/lote 3` toma las tres primeras abiertas según `ruta.pasos`.
   - `/lote memoria flujo` limita el trabajo a las actividades nombradas.
3. Antes de preguntar, mostrar un **Estado actual · Plan del lote** con cifras exactas:
   `Abiertas antes | Objetivo de este lote | Listas en la primera ronda | Bloqueadas por dependencias |
   Quedarían si todas cierran`. Añadir una tabla breve `Actividad | Ya definido | Falta decidir |
   Depende de`. Una previsión no es un cierre garantizado: decirlo de forma sencilla.
4. Trabajar por rondas de dependencias dentro de la misma ejecución. En cada ronda incluir solo
   actividades objetivo cuyas dependencias ya estén resueltas; leer completos sus prompts y contar
   todas las preguntas necesarias. No preguntar por una actividad descendiente antes de persistir y
   replanificar la que la desbloquea.
5. Anunciar en cada ronda `Actividades: N · preguntas: Q · ventanas: M`. `AskUserQuestion` admite
   hasta cuatro preguntas por ventana, pero el lote **no tiene máximo total**: abrir tantas ventanas
   consecutivas como sean necesarias sin pedir que la persona vuelva a ejecutar `/lote`.
6. Preguntar por necesidades y decisiones del trabajo, no por soluciones técnicas supuestas ni por
   la estructura de Harness-Maker. Usar lenguaje normal, opciones concretas y `multiSelect` solo
   cuando varias respuestas puedan coexistir. No omitir decisiones para reducir ventanas.
7. Si `Other` cuestiona una pregunta, dice que no se entiende o rechaza su premisa, no tratarlo como
   una elección. Terminar las preguntas independientes de la ronda, reinspeccionar la necesidad y
   añadir otra ventana si hace falta reformular; no cerrar el punto por descarte automático.
8. Al recibir cada ronda, revisar las 18 actividades antes de escribir. Toda actividad que resulte
   afectada se incorpora al alcance como seguimiento derivado, aunque no figurase entre los nombres
   o el número inicial. Mostrar el impacto y resolver sus preguntas mediante las rondas de impacto
   dentro de esta misma ejecución.
9. Al terminar las rondas principal y de impacto, fusionar solo lo confirmado en todas las
   actividades incluidas, sus
   Markdown y `cobertura.json`; regenerar, validar y recalcular el tramo pendiente. Si existe
   `AUDITORIA.md` junto al estado, sincronizar su recuento, las filas afectadas y la siguiente
   actividad sin tratarla como fuente. Registrar los impactos confirmados.
10. Continuar automáticamente con la siguiente ronda desbloqueada hasta cubrir todo el alcance o
   encontrar una decisión que realmente necesite trabajo externo o autoridad adicional. No asumir
   que responder equivale a cerrar: una actividad puede quedar en curso, descartada o con deuda.
11. Al finalizar, mostrar cifras reales: actividades intentadas del objetivo inicial, revisadas por impacto,
    completadas, descartadas, con deuda, todavía en curso y total que queda abierto.
    Explicar cuál es el siguiente paso si queda alguno.

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
   lenguaje normal. En `/lote`, añadir cuántas se intentaron y cuántas se cerraron realmente.
7. **Impacto en otras partes** — decir `Ninguno` o nombrarlas con una frase práctica por cada una.
8. **Detalles técnicos** — solo si el perfil es técnico, la persona los pide o necesita actuar ante
   un fallo. Resumir rutas, pruebas y riesgos; no narrar refactorizaciones ni decir que «las pruebas
   mentían» en la explicación principal.

No pegar un informe interno largo. Un riesgo que afecte a la persona sí se explica, pero primero en
lenguaje normal y después, si hace falta, con su causa técnica.
