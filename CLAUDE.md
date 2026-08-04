# Harness-Maker · instrucciones persistentes

Estas reglas se aplican durante toda la sesión, también fuera de las actividades `/contexto`,
`/prompts` y equivalentes.

## Escucha transversal

- Lee cada mensaje completo como una posible señal sobre el proyecto, aunque sea una observación
  informal o aparezca mientras se trabaja en otra cosa.
- Antes de cerrar una tarea, contrasta lo confirmado con las 18 actividades del mapa. Informa
  siempre `Impacto en el resto: ninguno` o enumera las actividades afectadas y el motivo.
- Un impacto confirmado no se limita a pintar otra actividad en rojo. Si abre una decisión que la
  persona puede resolver, señala `Impacto detectado · <actividad>` y pregunta inmediatamente lo
  necesario dentro del mismo comando, usando ventanas adicionales. No le pidas volver a ejecutar
  el comando de la actividad afectada.
- Resuelve primero por observación lo que ya demuestren el repositorio y las respuestas. Repite la
  revisión si la respuesta adicional afecta a otra actividad. Si todo queda resuelto, actualiza y
  verifica las actividades sin dejarlas abiertas; solo persiste `en_curso` cuando haga falta trabajo
  o evidencia externa, falte autoridad, la persona lo posponga o siga faltando una respuesta real.
- Una inferencia o contradicción posible se señala para confirmación; nunca se guarda como decisión
  de la persona sin confirmarla.
- Antes de preguntar cómo construir algo, confirma que la necesidad exista. Una objeción o un «no
  lo entiendo» corrige el diagnóstico; no cuenta como respuesta ni autoriza a cerrar el punto.
- Al cerrar, resume en una frase qué puede hacer ahora el harness e invita a probarlo con un encargo
  real que permita pulirlo.

## Cómo responder a la persona

- Busca en Contexto `Perfil de interacción`. Si no existe, responde como **Simple y guiado**: primero
  el resultado práctico y la siguiente acción, con palabras cotidianas.
- Los niveles disponibles son `Simple y guiado`, `Breve y directo` y `Técnico y detallado`. Son una
  preferencia de presentación, no una valoración de la capacidad de la persona. Solo se persiste un
  cambio cuando la persona lo pide expresamente.
- Tras un comando usa siempre: estado de la actividad; una frase de resultado; decisiones de la
  persona; qué cambia para ella; capacidad actual; cuántas actividades quedan y cuál sigue; impacto
  en otras partes. Los archivos, pruebas y detalles de implementación van al final y solo cuando el
  perfil sea técnico, se pidan o hagan falta para actuar ante un fallo.
- No conviertas la conclusión principal en una crónica de refactorizaciones ni uses frases internas
  como «las pruebas mentían». Separa con claridad lo decidido por la persona de lo observado o
  implementado automáticamente.

## Dónde se cambia cada cosa

- Fase 1 · base: `datos/anatomia.json`, esquemas y `diagramas/diagrama_base.html`. Es la doctrina.
  No se toca como efecto lateral: si trabajando se ve que debería cambiar, se propone y se espera
  la confirmación de la persona.
- Fase 2 · taller: generador, prompts, skills y `diagramas/diagrama_taller.html`. Aquí viven la
  interacción y la forma de mostrar cualquier proyecto. En la copia de desarrollo —la que tiene
  `proyectos/harness-lab/`— cuando al usar el taller se ve algo que arreglar en él, se arregla en el
  momento y se informa al cerrar: destilarlo es el objetivo de la fase 3, no una distracción.
  En una copia recibida, no: el taller llega por `git pull`, y editarlo allí deja archivos
  versionados modificados que chocan con la siguiente actualización, que es justo el mecanismo que
  hace llegar los arreglos. Ahí la mejora se propone, se anota en el recorrido y se traslada a quien
  mantiene el proyecto; misma regla que la fase 1. Lo que siempre se puede tocar en cualquier copia
  es el recorrido de la persona.
- Fase 3 · el recorrido de quien usa el taller: `estado.json`, `cobertura.json` y `piezas/` dentro
  del directorio que declare el puntero, normalmente `mi-harness/`. Aquí viven las decisiones
  concretas de ese proyecto, y **no se tocan como efecto lateral de arreglar el taller**. En la copia
  de desarrollo existe además `proyectos/harness-lab/`, el recorrido del propio Harness-Maker, que no
  viaja al reparto: quien recibe la base no hereda decisiones ajenas.
- El recorrido activo lo declara `.harness-maker.json` en la raíz, y es la única forma de saber cuál
  es. Ninguna actividad busca candidatos por el repositorio: sin puntero se detiene y pide
  `harness-lab init`. Un clon recién hecho estrena el suyo al arrancar; adoptar otro es explícito.
- `/auditoria-final` es deliberadamente de solo lectura sobre el producto: puede ejecutar pruebas
  no destructivas y escribir sus dos informes, pero no implementa las mejoras que proponga.
- Cuando la ruta no tenga actividades abiertas pero queden deudas, verificaciones, criterios
  parciales o derivados desfasados, usa `/incoherencias`: resuelve todo lo posible por rondas y no
  declares el recorrido listo hasta que lo aplicable esté completado y verificado.

## Persistencia y comprobación

- No edites a mano archivos que indiquen `GENERADO` o `NO EDITAR A MANO`; cambia su fuente.
- Conserva hechos, inferencias y desconocidos separados. No cierres una actividad por haberla
  comentado: necesita decisión y evidencia o un descarte/deuda explícitos.
- Tras cambiar una actividad, ejecuta `harness-lab generate`,
  `harness-lab validate --all` y `pytest -q`.
