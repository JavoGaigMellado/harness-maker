---
name: diagnostico
description: Diagnostica un proyecto para iniciar Harness-Maker, resume lo observado, pregunta solo los datos desconocidos y genera la ruta. Invocar manualmente con /diagnostico.
disable-model-invocation: true
---

<!-- GENERADO por `harness-lab generate`. NO EDITAR A MANO. -->
# Diagnóstico de Harness-Maker

1. Leer por completo `taller/prompts/00_diagnostico.md` y ejecutar su flujo.
2. El proyecto que se diagnostica es el que declara `mi-harness/diagnostico.json`, que `harness-lab
   init --repo` ya fijó; por defecto, este repositorio. Observar solo dentro de esa ruta. **No
   inventariar carpetas ajenas ni proponer como proyecto ninguna que la persona no haya nombrado**,
   aunque el entorno dé acceso a otras rutas: cuál es su proyecto lo dice ella, no un hallazgo del
   sistema de archivos.
   **Y no volver a preguntar cuál es.** Ya está decidido: `init` lo eligió y lo dijo al escribirlo.
   Preguntarlo otra vez convierte en duda algo resuelto y obliga a repetir rutas que la persona no ha
   vuelto a nombrar. Basta con decir en una línea qué carpeta se está observando. Solo si ella dice
   que está mal, indicarle `harness-lab init --reiniciar --repo <ruta>`; ni ofrecer candidatos ni
   buscarlos.
3. Mostrar un **Estado actual** breve con hechos observados, inferencias, desconocidos y la ruta
   donde se guardará el diagnóstico.
4. Contar todos los desconocidos y anunciar `Preguntas: N · ventanas: M`. Formularlos mediante
   llamadas consecutivas a `AskUserQuestion`, con hasta cuatro preguntas por ventana y sin máximo
   total dentro de esta ejecución. Usar `multiSelect` cuando corresponda, ofrecer entre dos y cuatro
   opciones concretas por pregunta y permitir escribir mediante la fila `Other`.
5. Tras recibir todas las ventanas, registrar conjuntamente lo confirmado en el diagnóstico
   sin inventar los valores restantes.
6. Cuando el diagnóstico sea suficiente, generar y validar `mi-harness/estado.json`, confirmar las
   rutas creadas y señalar la primera actividad de la ruta con la estructura de explicación indicada.

No hacer preguntas en texto normal ni preguntar información observable.

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
