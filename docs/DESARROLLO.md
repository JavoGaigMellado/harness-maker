# Harness-Maker · desarrollo y mantenimiento

Esto es para quien mantiene la doctrina y el taller, no para quien lo usa. Si acabas de recibir el
repositorio y quieres montar tu harness, el sitio es [`README.md`](../README.md).

Aquí vive lo que hay que entender para **cambiar** Harness-Maker: cómo está organizado, de dónde sale
cada prompt, qué valida qué, y cómo llega un arreglo a las copias de otras personas sin romperles el
trabajo.

## Cómo está organizado

El repositorio separa tres vidas del proyecto, y el árbol lo dice sin necesidad de leer nada más:

```
datos/        doctrina viva: anatomia.json y sus derivados generados
schema/       contratos de anatomía, diagnóstico y estado
taller/       el producto: prompts generados y ejemplo pedagógico
diagramas/    las tres vistas vivas: base, taller y mapa del propio proyecto
proyectos/    aplicaciones auditables del taller a proyectos concretos
src/          la CLI del taller: solo disco, sin red y sin dependencias de proveedor
tests/  docs/
historia/     procedencia: recopilación externa y las dos vistas propias ya superadas
```

Solo `datos/anatomia.json` es editable como doctrina. `historia/` no se reescribe. Lo demás se genera
o se deriva de ahí.

El 2026-08-04 salieron del árbol las fuentes de proyectos propios: los dossiers de los cuatro casos
que destilaron la doctrina, el banco de usuarios simulados, los informes internos que los citaban, el
catálogo de diagramas de otros proyectos y la herramienta de arqueología que los leía. Con ellos se fue
la única dependencia de proveedor que quedaba, así que **ninguna instalación descarga un SDK de pago**.
Lo que queda de procedencia es material externo o del propio taller.

## Diagnóstico y planificación

El diagnóstico no tiene un único `tipo_proyecto`. Mantiene independientes, entre otros, estos ejes:
forma de código, llamada/workflow/agente, urgencia, madurez, corpus cerrado/entrada externa, datos
sensibles, herramientas de lectura y escritura, reversibilidad, coste de prueba, capacidad de
decisión y horizonte de vida. Así, por ejemplo, un proyecto puede tener código propio **y** ser
urgente.

Toda prioridad incluye `regla` y `porque`. Las reglas viven en
[`datos/anatomia.json`](../datos/anatomia.json), no en el modelo ni ocultas en Python. Las peticiones de
la persona quedan diferenciadas como `peticion_del_usuario`. Una replanificación conserva el prefijo
ya realizado y solo sustituye el tramo pendiente.

La IA no elige el siguiente paso por intuición libre. En el diagnóstico interpreta el repositorio y
completa los ejes observables; el planificador aplica después las reglas declaradas. Al cerrar cada
actividad, la skill revisa todo el estado: si una respuesta confirmada cambia un eje del diagnóstico,
lo actualiza con evidencia y recalcula únicamente el tramo pendiente. El mapa ilumina el primer paso
no resuelto de esa ruta. Así, Contexto aporta información a las decisiones posteriores, pero no
puede saltarse dependencias ni inventar prioridades sin una regla trazable.

No hace falta construir las 18 actividades, pero sí evaluarlas y cerrarlas: una puede quedar
completada, descartada con motivo o aceptada como deuda. Las dependencias estrictas son pocas:
Contexto → Instrucciones; Herramientas → Seguridad; Plataforma → Coste de comprobar; Resultados →
Flujos; Instrucciones + Coste de comprobar → Casos de éxito → Revisor; y Registro → Alcance. El
resto puede trabajarse por lotes en la misma ejecución.

El suelo declarado consta de las siete piezas marcadas como «Siempre aplica»:

- Contexto e instrucciones persistentes;
- seguridad, datos y límites;
- plataforma y modelo;
- resultados y artefactos;
- coste de comprobar;
- alcance y ciclo de vida.

Las demás piezas pueden subir o bajar por una regla específica. En la fotografía actual de
Harness-Maker, por ejemplo, Herramientas e integraciones sube a obligatoria porque el proyecto escribe
archivos y ejecuta acciones con impacto.

Secretos, privacidad, identidad y supply chain no se esconden dentro de “historial”: son subáreas
transversales activadas por los datos y capacidades del diagnóstico.

## Fuente canónica y generación

[`datos/anatomia.json`](../datos/anatomia.json) es la única fuente doctrinal vigente. Genera el wrapper
compatible con `file://`, el índice y los 22 prompts del taller:

```bash
harness-lab generate
harness-lab validate --generated
```

Los derivados llevan una cabecera de generado y no deben editarse manualmente:

- `datos/anatomia.js` (`window.ANATOMIA = {...}`);
- `datos/indice_piezas.json`;
- `proyectos/harness-lab/estado.js` (fotografía navegable del propio proyecto);
- `taller/prompts/00_diagnostico.md`;
- un prompt autónomo por pieza;
- `taller/prompts/99_cierre_y_replanificacion.md`.

`historia/diagramas/` conserva las dos vistas propias ya superadas: `anatomia_harness.html`, que
`diagrama_taller.html` sustituye, y `anatomia_datos_v2.js`, procedencia histórica y no doctrina
vigente. Ninguna de las dos se toma como referencia para trabajo nuevo.

## Validación y pruebas

```bash
harness-lab validate --all
pytest -q
```

La validación cubre esquemas, referencias, IDs y posiciones estables, reglas citadas, las 18 piezas
en cada ruta, cierres semánticos y sincronía de generados. Las fixtures incluyen una app single-call
con corpus cerrado, un agente que escribe sobre datos externos, un proyecto sin código, un proyecto
de dos días y un estado parcialmente corrupto.

## Contratos y migraciones

- [`schema/anatomia.schema.json`](../schema/anatomia.schema.json): doctrina y reglas.
- [`schema/diagnostico.schema.json`](../schema/diagnostico.schema.json): observación y ejes del proyecto.
- [`schema/estado_taller.schema.json`](../schema/estado_taller.schema.json): ruta, decisiones y progreso.
- [`docs/MANTENIMIENTO.md`](MANTENIMIENTO.md): versionado, cambios y migraciones.

Migrar un recorrido a una doctrina nueva es `harness-lab migrate`, descrito arriba en
[Actualizaciones](#actualizaciones). Conserva el prefijo realizado, recalcula el tramo pendiente y anota
en `migraciones` de dónde viene.

La herramienta de arqueología de fase 1 se retiró el 2026-08-04 con los dossiers que leía. Era lo único
del repositorio que llamaba a una API de pago, así que ahora **no hay ninguna dependencia de proveedor,
ni obligatoria ni opcional**: instalar el taller trae `jsonschema` y nada más.

El taller añade subcomandos a una única CLI, no una segunda interfaz.

## Procedencia y límites

De lo que sostiene la doctrina sin ser doctrina queda en `historia/` la recopilación externa de
`historia/investigacion/` y las dos vistas propias ya superadas de `historia/diagramas/`. No se
reescribe para que parezca que siempre sostuvo la doctrina actual; por eso sus documentos citan rutas
anteriores a la reestructuración del 2026-08-02, tal como estaba el repositorio que describieron. La
doctrina canónica etiqueta referencias como evidencia interna, observación, recomendación, estándar,
predicción o resultado medido, además de su calidad.

**La procedencia primaria salió del árbol el 2026-08-04.** Decidido por Javo: nada que sea fuente de un
proyecto propio se reparte. Se retiraron los cuatro dossiers que destilaron la doctrina, el banco de
usuarios simulados, los informes internos que los citaban, el catálogo de diagramas de otros proyectos
y la herramienta que analizaba los dossiers. Describían proyectos, puestos y sistemas reales de una
empresa, con identificadores de tickets internos e incidentes de seguridad concretos. Las referencias
externas —investigación publicada, documentación de proveedores— se conservan: el criterio es la
procedencia, no el tema.

**Retirarlos del árbol no los borra de la historia de git.** Es el motivo por el que repartir exige
crear un repositorio nuevo desde el árbol limpio, no limpiar este: `git log` de esta copia sigue
conteniéndolo todo. El procedimiento está en `docs/REPARTO.md`, que no viaja al reparto: por eso se
nombra sin enlazarlo, o el único enlace roto del árbol repartido sería este.

La evidencia interna sigue siendo **n=4 no independiente**: los cuatro casos compartían autor,
asistente y en parte organización. Sirve para formular preguntas e hipótesis de diseño, no para
demostrar causalidad ni leyes del sector. Las cifras cuya trazabilidad cuestionó la auditoría no forman
parte de la doctrina. Retirar los dossiers no cambia ese límite y conviene decirlo así: la doctrina que
salió de ellos sigue siendo la que hay, y ahora su procedencia primaria **ya no es consultable en el
árbol**. Quien reciba esto no puede auditar de dónde vino cada afirmación; solo leerla y juzgarla.

## El taller aplicado a sí mismo

Harness-Maker se recorre con su propio taller: es la mejor prueba de que la doctrina aguanta,
porque un producto que no puede describirse con sus propias 18 piezas está afirmando algo que no
sostiene.

Ese recorrido vive en `proyectos/harness-lab/` y **no viaja al reparto**. Quien recibe la base no
debe heredar decisiones ajenas ni un «siguiente trabajo» que no es suyo, así que la copia de reparto
llega sin fase 3 y estrena la de quien arranca. Las pruebas que lo miran se saltan solas cuando la
carpeta no está: comprueban ese recorrido, no el producto.

La fotografía y su lectura están en `docs/REPARTO.md`, que tampoco viaja.

## Cómo se publica una actualización

Decidido el 2026-08-04: **dos repositorios**. Este conserva la historia completa del desarrollo y se
queda privado. El de reparto recibe solo el árbol limpio, y es el que clonan las personas.

Son dos porque retirar algo del árbol no lo retira de `git log`: subir esta historia entregaría todo
lo que se decidió no repartir. Y el de reparto necesita **historia continua**, porque lo que hace que
un arreglo llegue es el `git pull` de cada persona; exportar de cero cada vez la rompería.

```bash
python publicar.py --destino ../harness-maker-reparto
```

Copia el árbol de la rama actual sobre ese repositorio, commitea allí y no toca nada más. Antes de
copiar exige que este repositorio esté limpio, que `validate --all` pase y que las pruebas estén en
verde: publicar desde un árbol a medias es la forma más fácil de repartir un fallo. La primera vez crea
el repositorio si no existe; después solo añade un commit. Con `--solo-comprobar` dice qué publicaría y
no escribe nada.

Lo que no viaja está declarado con `export-ignore` en `.gitattributes`, el mismo mecanismo que usa
`git archive`, para que no haya una lista paralela que envejezca aparte.

**Servidumbre al cambiar las 18 piezas.** Un cambio de doctrina que renombre o retire una pieza deja
inválidos los recorridos ya empezados de otras personas. El mecanismo para eso es `harness-lab migrate`,
descrito en el README; además hay que migrar los estados que viajan dentro del repositorio y actualizar
las pruebas acopladas al conjunto de piezas, en el mismo cambio.

## Cómo llega de vuelta un fallo

Decidido el 2026-08-04: **por el canal interno**, sin mecanismo. Si a alguien se le atasca el taller lo
cuenta por Teams, por correo o de viva voz, y el arreglo se hace aguas arriba en fase 1 o fase 2.

Se elige así a sabiendas de sus dos límites, escritos para que no se descubran por sorpresa:

- **Llegará lo que la persona recuerde**, no lo que pasó. Su recorrido vive en `mi-harness/`, que no
  viaja por git, así que nadie más puede reconstruirlo después.
- **Deja de valer en cuanto crezca.** Sirve para dos o tres personas de confianza. Con más, los fallos
  que nadie cuente no existirán, y el taller parecerá mejor de lo que es.

La alternativa evaluada y no elegida hoy: un comando que escribiera un informe local del recorrido para
que la persona decidiera si enviarlo. Queda anotada por si el canal informal se queda corto.
