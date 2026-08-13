---
name: incoherencias
description: Revisa y resuelve de una vez las actividades con deuda, verificaciones pendientes, criterios parciales, derivados desfasados y contradicciones de Harness-Maker. Invocar manualmente con /incoherencias cuando el mapa parezca completo pero conserve avisos o trabajo pendiente.
disable-model-invocation: true
---

<!-- GENERADO por `harness-lab generate`. NO EDITAR A MANO. -->
# Resolver incoherencias

1. Leer por completo `taller/prompts/101_incoherencias.md` y cumplir su definición de pendiente y
   de recorrido listo.
2. Resolver el estado mediante `.harness-maker.json`; no buscar candidatos alternativos.
3. Inspeccionar estado, cobertura, Markdown, auditoría, derivados, código y pruebas antes de
   preguntar. Mostrar **Estado actual** con estas cifras exactas:
   `Listas y verificadas | Abiertas | Con deuda | Por verificar | Descartadas | Incoherencias`.
   Separar por causa: `Con deuda` requiere normas, criterios o decisiones; `Por verificar` requiere
   pruebas o evidencia sobre una definición ya completa.
   Revisar además **las decisiones caducadas**: una decisión no puede caducar sola, así que hay que
   buscarlas. Las que declaren `condicion_revision` cumplida y las que lleven la caducidad escrita
   dentro del texto sin declararla. Preguntar por cada una si su premisa sigue en pie.
4. Añadir una tabla `Actividad | Qué falla | Qué falta | Cómo se resuelve` y un plan por rondas de
   dependencias. No llamar incoherencia a un descarte válido, pero tampoco contarlo como capacidad.
5. Resolver sin preguntar lo observable. Contar todas las decisiones humanas restantes y anunciar
   `Preguntas: N · ventanas: M`. Formularlas mediante llamadas consecutivas a `AskUserQuestion`,
   hasta cuatro por ventana y sin máximo total dentro de esta ejecución. No pedir después otro
   comando de actividad.
6. Tras las respuestas, ejecutar todas las correcciones locales y reversibles autorizadas. Leer el
   prompt de cada actividad afectada y mantener sus criterios. Confirmar doctrina, destrucción,
   escritura externa o nuevas decisiones de producto antes de actuar.
7. Sincronizar conjuntamente estado, `cobertura.json`, los Markdown y la deuda global. Ejecutar
   `harness-lab generate`, `harness-lab validate --all` y `pytest -q`.
8. Volver a escanear desde cero. Si aparece otro punto solucionable, incorporarlo y continuar en la
   misma ejecución; repetir preguntas solo cuando surja una decisión nueva.
9. Terminar únicamente al alcanzar un punto fijo o un bloqueo real externo. Nunca cerrar una deuda
   o inventar una verificación para obtener 18/18.

## Respuesta final

Adaptar la explicación al `Perfil de interacción` de Contexto y mostrar, en este orden:

1. **Resultado** — cifra inicial, resuelta y restante.
2. **Qué quedó arreglado** — lista breve y práctica.
3. **Qué sigue pendiente** — solo bloqueos reales, cada uno con responsable y condición.
4. **Estado honesto del mapa** — listas y verificadas, abiertas, con deuda, por verificar y
   descartadas.
5. **Detalles técnicos** — archivos y pruebas solo si el perfil los pide o hace falta actuar.

No declarar `Recorrido listo` mientras quede una actividad aplicable sin verificar, un criterio
parcial, una deuda, una prueba en rojo o un derivado desfasado.
