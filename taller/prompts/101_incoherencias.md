<!-- GENERADO desde datos/anatomia.json por `harness-lab generate`. NO EDITAR A MANO. -->
# Resolver incoherencias y trabajo pendiente

Revisa el recorrido entero y resuelve en una sola ejecución todos los flecos que puedan cerrarse
ahora. El objetivo no es conseguir un 18/18 aparente: es hacer coincidir estado, evidencia,
cobertura, documentos, derivados y comportamiento real.

## Qué cuenta como pendiente

- actividades `pendiente`, `en_curso` o `deuda_aceptada`;
- actividades `completada` cuya verificación no sea `verificada`;
- criterios `parcial` o `no_definido` en `cobertura.json`;
- una actividad, deuda o riesgo cuyo estado contradiga su cobertura, su Markdown o la evidencia;
- deuda global que no coincida con la deuda de su actividad;
- wrappers, auditoría legible o derivados desfasados;
- validación o pruebas en rojo;
- afirmaciones de cierre que el repositorio no pueda demostrar.

Una actividad `descartada` con motivo, cobertura `no_aplica` y verificación `no_aplica` está
evaluada y no es un fallo, pero se muestra separada: nunca cuenta como capacidad implementada.
Una `deuda_aceptada` es una decisión válida, pero sigue siendo trabajo pendiente y tampoco cuenta
como actividad lista.

## Ejecución

1. Resolver el estado únicamente mediante `.harness-maker.json`. Leer completos el estado,
   `cobertura.json`, los últimos bloques `estado-pieza` de los Markdown, `AUDITORIA.md`, los
   wrappers generados y las reglas de `datos/anatomia.json`.
2. Ejecutar las comprobaciones no destructivas disponibles, incluido
   `harness-lab validate --all` y `pytest -q`. Separar fallo real de vista desfasada.
3. Mostrar una fotografía honesta: `Listas y verificadas | Abiertas | Con deuda | Por verificar |
   Descartadas | Incoherencias estructurales`. Añadir una tabla breve por actividad con el motivo y
   la evidencia que falta. `Con deuda` significa que aún faltan normas, criterios o decisiones;
   `Por verificar` significa que la definición ya existe y faltan pruebas o evidencia.
4. Clasificar cada punto como `Automático`, `Necesita decisión` o `Necesita trabajo/evidencia`.
   Resolver por observación lo automático y no volver a preguntar decisiones ya confirmadas.
5. Reunir todas las decisiones de la persona y preguntarlas en bloques consecutivos dentro de esta
   misma ejecución. No imponer un máximo total ni pedir que invoque después otra actividad.
6. Trabajar por rondas de dependencias. Antes de modificar una actividad, leer su prompt portable.
   La invocación autoriza correcciones locales, reversibles y necesarias para cumplir decisiones ya
   confirmadas. Pedir confirmación para doctrina, acciones destructivas, escritura externa o una
   elección nueva que cambie el producto.
7. Tras cada ronda, sincronizar estado, cobertura, Markdown y deuda global; regenerar derivados,
   validar y volver a escanear desde cero. Si una corrección abre otro punto, incorporarlo a la
   siguiente ronda sin terminar el comando.
8. Continuar hasta un punto fijo: no queda nada solucionable en esta ejecución. No convertir una
   deuda o una verificación ausente en `completada` para mejorar el contador.

## Cierre

Informar de cuánto había, cuánto se resolvió y qué sigue pendiente. Para cada resto indicar el
bloqueo real, responsable y condición de revisión. Solo declarar `Recorrido listo` cuando todas las
actividades aplicables estén completadas y verificadas, no haya criterios parciales ni pruebas en
rojo y los derivados coincidan con sus fuentes.
