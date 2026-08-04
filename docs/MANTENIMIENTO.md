# Mantenimiento de doctrina, esquemas y migraciones

## Reestructuración del repositorio (2026-08-02)

La separación que este documento ya declaraba por escrito —doctrina viva, derivados, estados de
usuario y procedencia histórica— no existía en el árbol: veinticuatro carpetas colgaban de la raíz
al mismo nivel, y había que leer esta sección para saber que `reports/` era pasado congelado y
`datos/` doctrina vigente. Además `prompts/`, el extractor de dossiers de fase 1, chocaba de nombre
con `taller/prompts/`, que es lo vivo y lo generado.

Lo que cambió:

- **`historia/`** recoge toda la procedencia: `perfiles/` (antes `profiles/`), `informes/` (antes
  `reports/`), `investigacion/` (antes `research/`), `prompts-extraccion/` (antes `prompts/`) y
  `diagramas/`, con las dos vistas propias ya superadas, `anatomia_harness.html` y
  `anatomia_datos_v2.js`.
- **`referencia/diagramas/`** recogió los diagramas de otros proyectos que vivían en `diagramas/`, para
  consultarlos como catálogo de diseño. Se retiró entero el 2026-08-04: eran vistas de proyectos
  propios y de sistemas de una empresa, y el criterio de reparto es que ninguna fuente de proyecto
  propio viaje. El patrón visual que de ahí salió sigue vivo en `diagramas/diagrama_base.html`, que es
  donde tiene que estar.
- **`src/harness_lab/arqueologia/`** aisló `analyze.py` y `propose_template.py`. **Superado el
  2026-08-02**: ese código pasó a `historia/arqueologia/` y su dependencia dejó de ser obligatoria
  —ver «La API sale del producto» más abajo.
- Se retiraron dos carpetas vacías y un perfil duplicado en `diagramas/`.

**No se movió nada de lo que `paths.py` resuelve**: `datos/`, `schema/`, `taller/`, `proyectos/`,
`.claude/skills/` y `.agents/skills/` conservan su ruta, así que el contrato de generación es el
mismo. Las citas de ruta sí se reescribieron en el canónico, en la fase 3 y en la documentación.

**Los documentos de `historia/` conservan sus rutas antiguas a propósito.** Una auditoría del 1 de
agosto que cita `reports/` está describiendo con exactitud el repositorio que auditó; corregirla
sería reescribir el pasado, que es justo lo que este documento prohíbe. Esta nota es el puente entre
ambas nomenclaturas.

El plan aprobado antes de ejecutar está en
`historia/informes/plan_reestructuracion_2026-08-02.md`.

## Migración de doctrina cerrada (2026-08-02)

`historia/informes/auditoria_anatomia_harness_trabajo_2026-08-02.md` cambió el objeto del producto: ya no se
describe lo que rodea a una aplicación LLM, sino **el harness de trabajo con IA de una persona**,
programe o no. Esa anatomía revisada vivió unos días solo en `diagramas/diagrama_base.html`, con sus
datos en línea, mientras `datos/anatomia.json` conservaba la perspectiva anterior.

**Esa duplicidad está resuelta.** El contenido del diagrama se volcó al canónico y el diagrama pasó a
consumirlo: ya no tiene datos propios. Lo que cambió en el volcado:

- **Anatomía**: anillos Orientación / Capacidades / Confianza / Continuidad, centro «Tu trabajo con
  IA», los 18 nombres largos y el ejemplo del ayudante de correo, que hila todas las piezas.
- **Campos nuevos por pieza** (esquema `2.0.0`): `categoria`, `descripcion_html`, `puntos_clave`,
  `que_montar`, `industria`, `casos` y, en cinco piezas, `accion_preparada`.
- **Un solo eje de aplicabilidad**: la categoría del diagrama determina `prioridad_base`
  —`c1`→obligatoria, `c2`→alta, `c3`→media, `c4`→baja— y el suelo pasa a ser exactamente el conjunto
  de piezas marcadas «siempre aplica», siete hoy.
- **Reglas retiradas**: `proveedor.no_code` y `salida.no_code` degradaban esas piezas para quien no
  programa, que es justo el caso por el que el diagrama las marca «siempre aplica».
- **Desempate en el planificador**: a igual prioridad gana la regla específica sobre la base o el
  suelo, para que la ruta explique por qué le toca a esta persona y no solo que es obligatoria.

En caso de conflicto sigue mandando el contenido del diagrama, pero ya no como excepción: el diagrama
es una vista de `datos/anatomia.json`, y editarlo significa editar el canónico y regenerar.

**Pendiente, y es trabajo aparte:** el kit de reparto. La semilla `mi-harness/` la crea
`harness-lab init`, y el mecanismo de actualización quedó resuelto el 2026-08-04 —ver «Cómo llega un
arreglo a una copia ajena». El modo taller citado en el plan ya quedó resuelto en `diagrama_taller.html`. La capa
ejecutable de Claude vive en `.claude/skills/` y se genera para diagnóstico, las 18 actividades, el
cierre, la revisión de incoherencias y la auditoría final. Cada
`/actividad` consume su prompt portable, usa `AskUserQuestion` y persiste antes de continuar. La
experiencia completa y el criterio de promoción cubren solo Claude Code. Codex conserva el piloto
experimental `.agents/skills/contexto/` con invocación `$contexto`, fuera de esa promesa.

## Las entradas visuales (2026-08-02)

- **`diagramas/diagrama_base.html`** es la anatomía y **no se toca para nada del taller**. Es lo que
  tiene que verse y entenderse siempre, y se mantiene limpio a propósito.
- **`diagramas/diagrama_taller.html`** es el mismo diagrama con la capa de recorrido encima:
  interruptor «Mi proyecto / Ver el ejemplo», pestañas `Información` y `Tu proyecto`, estados sobre
  los nodos y anillos como barra de progreso. La clasificación «siempre/según el caso» no se muestra
  en el taller: sigue disponible para planificar, pero no compite con el recorrido de la persona. El
  núcleo toma el nombre y la definición del proyecto del estado activo. El
  primer paso no resuelto de `ruta.pasos` es la recomendación vigente: se muestra con un halo suave y
  una conexión resaltada, sin rótulo adicional, también en la alternativa móvil. El comando de cada
  actividad y su estado aparecen junto al título; los campos empiezan contraídos y las actividades
  completadas usan verde claro. Cada anillo muestra un KPI de actividades resueltas y un resumen de
  lo que sabe el proyecto. La capacidad acumulada aparece una sola vez, bajo el título del producto,
  y cambia cuando se cierra una actividad. Dentro de cada actividad, la lista canónica muestra cada
  punto como definido, parcial, ausente o no aplicable; los dos estados incompletos usan fondo rojizo,
  sin un bloque separado «Por definir». Las relaciones e impactos quedan en su propio desplegable.
  `Instrucciones persistentes` muestra además el inventario de los 22 prompts y el acceso a
  `/incoherencias`. El progreso verde cuenta solo actividades completadas y verificadas: las deudas,
  las verificaciones pendientes y los descartes aparecen por separado y nunca producen un 18/18 falso.
  En el mapa, el ámbar señala deuda de definición o normas pendientes; el azul señala una actividad
  definida que necesita pruebas o evidencia de verificación.
  El ejemplo del correo queda solo en la pestaña `Información`, sin duplicarse en el estado del
  proyecto.

## Lo aprendido de los primeros comandos

Las sesiones reales de Contexto, Herramientas, Seguridad, Plataforma y Resultados dejan dos reglas
de interacción. Primera: agrupar hasta cuatro preguntas funciona cuando cada una pregunta por una
decisión real y el repositorio ya ha resuelto los hechos observables. Segunda: no se ofrece una
solución técnica antes de confirmar la necesidad. En Plataforma se preguntó cómo unificar una API
que el producto no necesitaba; la respuesta de la persona corrigió la premisa y acabó sacando la API
del producto. Las skills generadas tratan ahora «no lo entiendo» o una objeción escrita en `Other`
como corrección del diagnóstico, no como una respuesta que permita cerrar el punto.

La prueba posterior mostró otro límite: una conclusión técnicamente correcta puede resultar
incomprensible para quien empieza si mezcla decisiones, detalles de implementación, pruebas e
impactos internos. Las skills usan ahora `Simple y guiado` por defecto y un cierre estable: resultado
en una frase, decisiones, consecuencia práctica, capacidad actual, trabajo restante e impactos. Los
detalles técnicos quedan al final y solo aparecen cuando el perfil los pide o son necesarios.

`AskUserQuestion` admite como máximo cuatro preguntas por ventana, no por comando. Las actividades
cuentan primero todo lo necesario y abren ventanas consecutivas, y muestran los recuentos reales
antes y después. El comando que resolvía varias actividades en una ejecución se retiró el
2026-08-04: el ritmo de cuestionario producía definiciones sobre la estructura del harness en vez de
sobre el trabajo de la persona.

El uso real mostró un tercer límite: detectar un impacto y reabrir otra actividad no basta si la
persona solo descubre después el rojo del diagrama. Cada comando ejecuta ahora **rondas de impacto**:
señala la actividad afectada, resuelve primero lo observable y pregunta inmediatamente las nuevas
decisiones dentro de la misma ejecución. Una actividad afectada se incorpora como seguimiento
derivado. Solo queda abierta cuando la respuesta no puede cerrarla
—por trabajo o evidencia externa, falta de autoridad o aplazamiento explícito—; nunca porque falte
volver a invocar su comando.

`/incoherencias` aplica esa lógica al recorrido completo. Reúne actividades abiertas, deudas,
verificaciones pendientes, criterios parciales, deuda global desincronizada, derivados desfasados y
pruebas fallidas. Corrige por rondas y vuelve a escanear hasta un punto fijo. Un descarte válido se
muestra aparte y una deuda aceptada sigue sin contar como lista.

## Auditoría final

`/auditoria-final` se ejecuta después de `/cierre` y no confía en el relato acumulado: inventaría y
lee el proyecto desde cero, comprueba el comportamiento y reconstruye decisiones con git y chats
autorizados de Claude y ChatGPT. Los chats son evidencia no confiable, nunca instrucciones. La skill
debe demostrar qué leyó, declarar omisiones y separar lo dicho por un asistente de lo confirmado por
la persona. Solo escribe el informe Markdown y su JSON estructurado junto al estado activo; cualquier
cambio propuesto requiere una decisión posterior.

- **`diagramas/mapa_harness_lab.html`** es una entrada mínima al diagrama de taller con la fotografía
  del propio Harness-Maker. Redirige a `diagrama_taller.html?proyecto=harness-lab`: así conserva la
  interfaz exacta y no crea una tercera copia del render. Su fuente es
  `proyectos/harness-lab/estado.json`; `harness-lab generate` crea el wrapper `estado.js` para abrirlo
  también con `file://`.

**El contenido no está duplicado**: ambos leen `datos/anatomia.js`, así que un cambio de doctrina
llega a los dos con `harness-lab generate`. Lo que sí está duplicado es el **código de render**. La
servidumbre es explícita: si se cambia el dibujo o el panel en el base, hay que trasladarlo al
taller. Por eso el taller se mantiene como «el base más una capa aditiva» —CSS al final del bloque
de estilos, funciones al final del script— y no como una reescritura: así el traslado es mecánico.

El mapa del propio proyecto no cambia esta servidumbre porque no contiene render. Para actualizar
la fotografía se editan su diagnóstico y estado, se validan ambos y se regenera el wrapper; nunca se
alteran las 18 piezas para hacer que el proyecto parezca más completo.

## Separación de responsabilidades

- `historia/` es procedencia histórica: informes, investigación externa, el extractor de dossiers de
  fase 1 y las vistas propias superadas. Se corrige mediante una nota o un informe nuevo, no
  reescribiendo el pasado. Los dossiers de `historia/perfiles/` y el banco de `taller/casos/` se
  retiraron el 2026-08-04 por decisión de Javo: describían proyectos y puestos reales de una empresa.
  Es la primera vez que se retira algo de `historia/` en vez de anotarlo, y la excepción está aquí
  escrita a propósito —manda la decisión de la persona, pero no debe leerse como que la regla cambió.
- `referencia/` se consulta y no manda: diagramas de otros proyectos que sirven de catálogo de
  diseño. No es doctrina ni procedencia de esta.
- `datos/anatomia.json` es doctrina vigente y única fuente editable.
- `datos/anatomia.js`, `datos/indice_piezas.json`, `proyectos/harness-lab/estado.js`,
  `taller/prompts/` y `.claude/skills/` son derivados regenerables.
- `taller/` es fase 2: el producto, sus prompts y su ejemplo pedagógico.
- `.claude/skills/` es fase 2: adaptadores ejecutables de Claude para todo el recorrido.
- `.agents/skills/` es fase 2: adaptadores experimentales de Codex; `contexto` sigue siendo el piloto
  actual y no forma parte de la experiencia completa ni del criterio de promoción.
- `proyectos/` es fase 3: aplicaciones auditables del taller a proyectos concretos; no contiene
  doctrina ni render propios. La autoaplicación de Harness-Maker conserva además `cobertura.json`, que
  enlaza cada criterio canónico con su cobertura y evita cierres basados solo en archivos cercanos.
- `mi-harness/` pertenece a cada recorrido y nunca debe incorporarse a la doctrina.

**`historia/` y `referencia/` no se abren por defecto.** Separarlas del trabajo vivo era condición
necesaria pero no suficiente: siguen a un `grep` de distancia. La regla es que una sesión no las lee
salvo petición expresa, porque leer procedencia por costumbre es la vía por la que una decisión
superada vuelve a sonar a norma. Decisión registrada en `proyectos/harness-lab/piezas/contexto.md`
(2026-08-02).

## Dos reglas que impone el sistema

Las demás reglas de este documento se cumplen leyéndolas. Estas dos no: son las que rompen el
repositorio en silencio, así que están enganchadas en `.claude/settings.json` y se ejecutan solas.

- **`.claude/hooks/proteger_generados.py`** bloquea cualquier `Edit`/`Write` sobre un archivo
  generado —rutas conocidas, más cualquier archivo cuya cabecera diga `NO EDITAR A MANO` o
  `"generated": true`— y explica qué fuente editar en su lugar.
- **`.claude/hooks/validar_al_cerrar.py`** ejecuta `validate --all` y `pytest -q` al terminar el
  turno e impide cerrar si algo está en rojo. Respeta `stop_hook_active` para no encerrar la sesión
  en un bucle.

**Su alcance es el asistente, no el disco.** Un `vim` sobre un generado sigue funcionando: para
cerrar esa puerta haría falta un hook de git, que es otra decisión y no está tomada.

## La API sale del producto (2026-08-02)

El recorrido no llama a ninguna API: el motor lee y escribe disco, y los prompts se ejecutan en el
asistente que elija la persona. Aun así, `anthropic>=0.40` era dependencia **obligatoria**, de modo
que cualquiera que clonase el repositorio se descargaba un SDK de proveedor que nunca iba a usar.
Los dos únicos archivos que lo importaban eran los de arqueología de fase 1.

Lo que cambió:

- **`historia/arqueologia/`** recoge `analyze.py` y `propose_template.py`, que ya no cuelgan del
  paquete instalable. Se ejecutan como scripts desde la raíz, no con `python -m harness_lab...`.
- **`anthropic` pasa a extra opcional** (`pip install -e '.[arqueologia]'`). Las dependencias
  obligatorias quedan en `jsonschema` y nada más.
- `ROOT` en ambos archivos pasa de `parents[3]` a `parents[2]` por la nueva profundidad.

**La regla que queda:** el producto no depende de ningún proveedor. Si algún día algo del recorrido
necesitara una llamada externa, eso reabre Plataforma y modelo antes de escribir la primera línea.

## Fuentes y dudas dentro del documento (2026-08-02)

Todo documento que escriba la IA lleva dentro de dónde sale lo que afirma y qué quedó sin comprobar.
No basta con que el estado lo registre aparte: el documento tiene que sostenerse solo cuando alguien
lo lea suelto, meses después y fuera de su conversación.

La madurez, en cambio, **no** se marca dentro del archivo: la dicen el estado de cada decisión
—`pendiente`, `en_curso`, `completada`, `descartada`, `deuda_aceptada`— y su verificación. Un aviso
de «borrador» dentro del texto crearía una segunda fuente de verdad para lo mismo.

## Revisión de las instrucciones

Al cerrar cada una de las 18 actividades se comprueba si alguna instrucción del proyecto ha quedado
obsoleta, y se retira en el mismo cierre. No hay una fecha en el calendario: el disparador es
terminar una decisión, que es justo el momento en el que se sabe qué ha dejado de ser cierto.
`CLAUDE.md` mantiene esta escucha activa durante toda la sesión: el asistente declara el impacto en
otras actividades y abre en el mismo comando las preguntas que permitan resolverlas. Solo reabre y
deja pendiente lo que no pueda cerrarse en esa ejecución. Las skills generadas repiten el mismo
contrato durante cada comando. Otros asistentes necesitan un adaptador equivalente si no leen
`CLAUDE.md`.

## Flujo de cambio

1. Cambiar `datos/anatomia.json` y, si cambia el contrato, su esquema.
2. Mantener los 18 IDs, anillo, posición e icono salvo migración visual explícita.
3. Cada regla nueva necesita identificador estable, condición, prioridad, motivo y procedencia. No
   se admite una regla solo en el código.
4. Ejecutar `harness-lab generate`.
5. Ejecutar `harness-lab validate --all` y `pytest -q`.

## Versionado

Los contratos usan `MAJOR.MINOR.PATCH`:

- `PATCH`: texto o metadatos que no cambian instancias válidas;
- `MINOR`: campos opcionales o reglas nuevas compatibles;
- `MAJOR`: renombre/eliminación, cambio de semántica o nuevo requisito obligatorio.

La doctrina tiene además `doctrina_version` con fecha. Un estado conserva la versión exacta de la
anatomía con la que se planificó.

## Cómo llega un arreglo a una copia ajena (2026-08-04)

El modelo de reparto, decidido por Javo: él mantiene la fase 1 y la fase 2; los usuarios clonan y
trabajan sobre su copia; cuando aparece un fallo, él lo corrige aguas arriba y el arreglo baja a las
copias sin que nadie reconstruya nada. El canal es `git pull`.

Lo que hace que eso funcione ya estaba en su sitio, y conviene decir por qué: **el trabajo de cada
persona vive en `mi-harness/` y en `.harness-maker.json`, los dos excluidos del repositorio**. Una
actualización no puede pisarlos, y una copia que ha recorrido el taller completo no tiene ningún
archivo versionado modificado, así que el `pull` entra sin conflictos. Comprobado sobre un clon
limpio, no supuesto.

Lo que faltaba era el caso incómodo: un arreglo de fase 1 que cambie el conjunto de piezas o la
versión de la doctrina deja inválido el recorrido de otra persona —«referencia a pieza inexistente»—
y ningún commit puede arreglarlo, porque `mi-harness/` es justo lo que no viaja. Dos piezas nuevas lo
cierran:

- **`harness-lab migrate`** ejecuta la estrategia de la sección siguiente. Antes existía escrita y no
  existía como código, que es la peor combinación: una promesa que nadie puede cumplir.
- **El arranque lo detecta y lo nombra.** Compara la versión del recorrido con la vigente y, si no
  cuadran, explica que la actualización trae piezas distintas y da el comando, en vez de enseñar un
  error de esquema que dice qué falla pero no qué hacer.

**Servidumbre para quien mantiene la doctrina:** un cambio de piezas obliga a migrar también los
estados que viajan dentro del repositorio —`taller/ejemplo/` y `proyectos/harness-lab/`— y a
actualizar las pruebas acopladas al conjunto de piezas, en el mismo cambio. El mismo comando sirve.

## Estrategia de migración

Implementada en `src/harness_lab/migrate.py` desde el 2026-08-04; hasta entonces esta sección era
política sin mecanismo. No se modifica un estado antiguo en sitio. El migrador debe:

1. leer y validar tanto como permita la versión anterior;
2. copiar el estado a una salida nueva;
3. preservar decisiones, evidencias, Markdown y el prefijo realizado;
4. transformar solo claves conocidas;
5. añadir una entrada a `migraciones` con `de`, `a` y fecha;
6. recalcular únicamente el tramo pendiente con reglas de la nueva anatomía;
7. validar la salida con el esquema nuevo.

La migración inicial desde el plan v0 no es automática: aquel documento no era un contrato y usaba
`tipo_proyecto` excluyente, cuatro estados y cierres sin deuda estructurada. Debe importarse como
evidencia, completar los ejes desconocidos y generar un estado 1.0.0 nuevo. Los Markdown acumulativos
son la vía de recuperación si el JSON de origen está incompleto.

Una futura incompatibilidad debe incluir fixture antes/después y una función explícita de migración;
nunca se resuelve relajando silenciosamente el validador.

Dos decisiones del migrador que conviene tener escritas, porque no se deducen de los siete pasos:

- **Un renombre se declara, no se adivina.** `salida` → `resultados` es indistinguible de «una se
  retira y otra aparece» comparando solo las dos anatomías. Con `--renombrar viejo=nuevo` el registro
  viaja al nombre nuevo; sin declararlo, la pieza vieja se aparta como retirada y su trabajo queda
  guardado dentro de la entrada de `migraciones`.
- **El `orden` se reasigna en todos los pasos.** Cuando cambia el conjunto de piezas, las posiciones
  exactas no se pueden conservar y arrastrar ordinales del reparto anterior produciría repetidos o
  huecos. Lo que el prefijo realizado conserva es su razonamiento —prioridad, regla y porqué—, que es
  lo que hace auditable una decisión ya tomada. Si la regla citada dejó de estar declarada, la nueva
  queda en el paso y la anterior, dentro de `migraciones`.
- **`ruta.motivo` sigue siendo `replanificacion`.** Una migración es una replanificación por causa
  externa; no se añade un valor al enum para que quepa el caso propio.
