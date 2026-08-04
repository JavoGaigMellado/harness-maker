---
name: contexto
description: Define y registra las cinco capas del contexto de trabajo de un proyecto con Harness-Maker. Usar cuando la persona invoque $contexto, pida completar la actividad Contexto o quiera decidir qué información carga una sesión y qué conserva al terminar.
---

# Contexto

## Preparar la actividad

1. Trabajar desde la raíz del repositorio actual.
2. Leer por completo `taller/prompts/01_contexto.md` y seguir su doctrina y su contrato de cierre.
3. Resolver el estado objetivo antes de preguntar:
   - usar la ruta indicada explícitamente por la persona, si existe;
   - en caso contrario, leer `.harness-maker.json` y usar la ruta de su clave `estado`;
   - si no existe el puntero, detenerse y pedir `harness-lab init`; no adoptar otro recorrido por
     ser el único encontrado en el repositorio.
4. Explicar brevemente por qué Contexto aparece ahora, citando `regla` y `porque` de su paso.
5. Inspeccionar el repositorio y el estado antes de conversar. No preguntar datos observables.

No modificar `datos/anatomia.json`, sus esquemas ni `diagramas/diagrama_base.html` durante esta
actividad.

## Conducir la conversación

- Mostrar primero una lectura rápida de lo ya definido, separando persona, organización, proyecto,
  tarea actual y sesión anterior. Distinguir hechos, inferencias y desconocidos.
- Reunir todas las decisiones parciales o no definidas y formularlas mediante llamadas consecutivas
  a `request_user_input`, con hasta tres preguntas por ventana y sin máximo total en la ejecución.
  Cada pregunta debe resolver una decisión; no obligar a volver a invocar `$contexto` para recibir
  las restantes.
- No convertir una inferencia en decisión. Registrar únicamente lo confirmado por la persona o lo
  demostrado por una fuente del repositorio.
- Mantener las decisiones legibles con el formato `Etiqueta — contenido`. Fusionar por etiqueta en
  vez de acumular versiones contradictorias de la misma definición.

## Resolver impactos sin otro comando

Después de recibir las respuestas, contrastarlas con las 18 actividades antes de persistir:

1. Si una respuesta abre una decisión en otra actividad, mostrar
   `Impacto detectado · <actividad>` y explicar qué cambió.
2. Resolver sin preguntar lo que ya demuestren el repositorio y las respuestas confirmadas.
3. Preguntar inmediatamente mediante `request_user_input` todo lo nuevo que solo pueda decidir la
   persona. Abrir las ventanas adicionales necesarias dentro de esta misma ejecución.
4. Repetir la revisión si la respuesta adicional abre otro impacto y evitar preguntas duplicadas.

No pedir a la persona que ejecute después el comando de la actividad afectada. Si el impacto queda
resuelto, actualizarla y verificarla sin dejarla abierta. Mantenerla `en_curso` únicamente si exige
trabajo o evidencia externa, falta autoridad, se aplaza expresamente o sigue faltando una respuesta.

## Persistir cada avance confirmado

1. Fusionar `contexto` y las actividades afectadas dentro del estado objetivo sin alterar piezas
   ajenas ni el prefijo realizado de la ruta.
2. Escribir sus registros acumulativos en `<directorio-del-estado>/piezas/`, terminados con un
   bloque cercado `estado-pieza` que contenga el JSON completo de cada pieza modificada.
3. Si existe `<directorio-del-estado>/cobertura.json`, actualizar también los criterios de Contexto
   y mantener coherentes `resultado`, estado y regla de cierre.
4. Regenerar derivados con `python3 -m harness_lab generate` cuando el estado tenga un wrapper
   generado, y validar con:

   ```bash
   python3 -m harness_lab validate --state <ruta-del-estado>
   ```

5. Mantener `en_curso` mientras quede algún criterio parcial o no definido. Marcar `completada`
   solo cuando todos estén `definido` o `no_aplica` y exista evidencia o artefacto verificable.

Al terminar, decir qué se registró, qué impactos se resolvieron y qué queda realmente abierto. Si
las respuestas no permiten escribir nada con seguridad, no modificar archivos.
