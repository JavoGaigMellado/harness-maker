# Harness-Maker

Acabas de recibir un taller guiado para construir **el harness de tu proyecto**: las decisiones,
políticas y evidencia que hacen que trabajar con IA sobre él sea repetible en vez de improvisado.

No implementa nada por ti y no se conecta a nada. Te hace las preguntas en el orden correcto,
calcula qué te toca decidir según cómo sea tu proyecto, y deja escrito lo que decidas para que
dentro de tres meses siga sirviendo. Recorre 18 áreas; ninguna se salta, pero muchas se cierran con
un «no aplica» razonado, que también es una decisión.

Requiere Python 3.12 o posterior y, para la experiencia completa, **Claude Code**.

## Empieza aquí

Un comando, desde el clon recién hecho y en cualquier sistema operativo:

```bash
python arrancar.py
```

En Claude Code, el equivalente es **`/start`**.

La primera vez crea el entorno, instala el paquete, **estrena tu recorrido** en `mi-harness/`, activa
el guardián de generados, valida, pasa las pruebas y te abre el mapa en el navegador. Termina
diciéndote cuál es tu siguiente paso, que será `/diagnostico`.

Es idempotente: sirve igual la primera vez que la número treinta y cuatro. Si el entorno ya está
listo, no vuelve a instalar; comprueba, te dice en qué estado está tu copia y abre la vista.

Si tu proyecto vive en otra carpeta, dilo y el diagnóstico mirará ahí:

```bash
python arrancar.py --repo <ruta-de-tu-proyecto>
```

Y si no tienes proyecto de código propio, arranca sin más y responde «no» cuando el diagnóstico te
pregunte si la carpeta que ha mirado es la tuya.

Requiere Python 3.12 o posterior. Se eligió ese suelo porque es la versión que suele estar ya
instalada sin pedir permisos; está comprobada ejecutando toda la batería en 3.12.4. Bajarla más
exige repetir esa comprobación y registrar el resultado, no basta con suponerlo.

Los pasos sueltos, si prefieres hacerlo a mano. En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
harness-lab validate --all
```

En Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
harness-lab validate --all
```

Si prefieres crear el recorrido por separado, sin arrancar todo:

```bash
harness-lab init --repo /ruta/al/proyecto
```

`init` crea `mi-harness/`, escribe allí el diagnóstico observable y deja en la raíz
`.harness-maker.json` declarando cuál es tu recorrido activo. Ese puntero es lo único que dice cuál
es: ninguna actividad va a buscar candidatos por el repositorio, así que sin él se detienen y te
piden `init` en vez de adivinar.

Si reutilizas una copia que ya tiene un recorrido avanzado y quieres empezar de cero:

```bash
harness-lab init --reiniciar
```

Aparta el recorrido anterior como `mi-harness-anterior-<fecha>` y arranca uno limpio. No borra nada, y
solo toca el directorio que está inicializando. `mi-harness/` y sus copias apartadas están excluidos de
git: la doctrina y los comandos viajan, tu trabajo se queda en tu copia.

La frontera de lo que el asistente puede hacer está escrita en `.claude/settings.json` y explicada una
a una en [`docs/harness/harnessdev.md`](docs/harness/harnessdev.md), junto al inventario de mecanismos.


## Tu primer recorrido

El comando solo escribe lo que puede observar y deja los desconocidos explícitos. Abre
[`taller/prompts/00_diagnostico.md`](taller/prompts/00_diagnostico.md) con tu asistente de desarrollo
para completar lo que no pueda responderse mirando el proyecto. Una ventana admite hasta cuatro
preguntas, pero el mismo comando abre todas las ventanas consecutivas que hagan falta.

Después:

```bash
harness-lab validate --diagnostic mi-harness/diagnostico.json
harness-lab plan --diagnostic mi-harness/diagnostico.json --output mi-harness/estado.json
harness-lab validate --state mi-harness/estado.json
```

La ruta incluye siempre las 18 piezas. Una pieza no aplicable aparece con prioridad de descarte y
solo se cierra cuando se registra el motivo. El siguiente prompt se encuentra en
[`taller/prompts/`](taller/prompts/), según el `pieza_id` del primer paso pendiente.

En Claude Code, `harness-lab generate` crea skills de proyecto en `.claude/skills/`: `/diagnostico`,
los 18 comandos de actividad (`/contexto`, `/memoria`, etc.), `/cierre`,
`/incoherencias` y `/auditoria-final`. Cada actividad empieza con un resumen breve y reúne sus decisiones pendientes en selectores interactivos
`AskUserQuestion`; se puede responder clicando opciones o escribiendo en `Other`. Si hacen falta más
de cuatro preguntas, continúa con otra ventana dentro de la misma ejecución: no recorta decisiones
ni obliga a repetir el comando. Antes de preguntar cómo construir algo, comprueba que la necesidad
exista: una API, memoria o automatización innecesaria se marca `no aplica` con evidencia, no se
convierte en trabajo.

Las actividades se recorren de una en una, y es a propósito. Existió un comando que resolvía varias
en la misma ejecución y se retiró el 2026-08-04: contestar dieciocho actividades a ritmo de
cuestionario producía definiciones sobre cómo está organizado el harness en vez de sobre el trabajo
de quien lo usa, que es lo único que sirve dentro de tres meses. El mapa siempre señala la actividad
concreta que toca.

Cuando el recorrido ya no tiene actividades abiertas pero conserva deudas, criterios parciales,
verificaciones pendientes o vistas desfasadas, usa `/incoherencias`. Enseña primero una fotografía
honesta, pregunta todas las decisiones necesarias y resuelve los flecos por rondas dentro del mismo
comando. Una deuda aceptada sigue siendo trabajo pendiente: no cuenta como actividad lista.

Después de cerrar el recorrido con `/cierre`, `/auditoria-final` vuelve a empezar desde las evidencias: inventaría
todo el repositorio, lee código, configuración, documentación, estado, pruebas e historial git y
contrasta, con autorización, los chats del proyecto en Claude y ChatGPT. Reconstruye qué se montó y
por qué antes de buscar errores, contradicciones, riesgos y mejoras. Solo escribe dos entregables
junto al estado activo —`auditorias/auditoria-final.md` y `.json`—; propone cambios, no los aplica.

Para continuar en otro ordenador basta con clonar y ejecutar `python arrancar.py`: el puntero local no
viaja por Git, y el arrancador lo vuelve a declarar sin sobrescribir el recorrido que encuentre. La
guía de traslado que antes explicaba esto a mano se retiró el 2026-08-04, porque describía el paso
entre dos ordenadores concretos y su sitio lo ocupa ese comando.

Las respuestas parten del perfil **Simple y guiado**: explican primero qué se decidió, qué cambia al
usar el harness, qué puede hacer ya y cuál es el siguiente paso. La persona puede pedir `Breve y
directo` o `Técnico y detallado`; la preferencia confirmada se guarda en Contexto. Los archivos,
pruebas y detalles internos no ocupan la conclusión principal salvo que hagan falta o se pidan.

`CLAUDE.md` mantiene durante toda la sesión una regla transversal: cualquier observación de la
persona se contrasta con las 18 actividades, aunque aparezca fuera de un comando. El cierre declara
si afectó a otras actividades. Si el impacto abre una decisión que la persona puede resolver, el
mismo comando la señala y abre las preguntas adicionales necesarias: no deja la actividad en rojo
para que haya que invocarla otra vez. Solo queda abierta si necesita trabajo externo, otra autoridad
o una decisión aplazada. Una inferencia solo se propone para confirmación. También resume qué puede
hacer ya el harness e invita a probarlo con un encargo real.

La experiencia completa que se reparte y se somete al criterio de promoción es la de **Claude
Code**. Codex mantiene de momento el adaptador experimental `$contexto` en
`.agents/skills/contexto/`, fuera de esa promesa: no se exige ni se afirma paridad funcional.


## Actualizaciones

La doctrina y los comandos viajan por git; tu trabajo no. `mi-harness/` y `.harness-maker.json` están
excluidos del repositorio, así que una actualización no puede pisar tu recorrido:

```bash
git pull
python arrancar.py
```

`git pull` trae el arreglo y el arrancador pone al día lo generado. Está comprobado que no hay
conflictos: después de recorrer el taller completo, un clon no tiene ningún archivo versionado
modificado.

Si el arreglo cambia las 18 piezas o la versión de la doctrina, tu recorrido se planificó con la
anterior. El arranque te lo dice con esas palabras —no con un error de esquema— y nombra la salida:

```bash
harness-lab migrate --state mi-harness/estado.json --solo-comprobar
harness-lab migrate --state mi-harness/estado.json --aplicar
```

`--solo-comprobar` enseña qué piezas se renombran, se retiran o aparecen, y no escribe nada.
`--aplicar` deja el recorrido migrado en su sitio y aparta el anterior con su fecha; `--output`
escribe una copia y no toca el original. La migración conserva el prefijo realizado con sus
decisiones y evidencias, recalcula solo el tramo pendiente con las reglas nuevas y anota en
`migraciones` de qué versión a qué versión viene. Una pieza que la doctrina retire se guarda entera
dentro de esa anotación: **no se borra trabajo**.

Un renombre no se puede adivinar —`salida` → `resultados` es indistinguible de «una se retira y otra
aparece» mirando solo las dos doctrinas—, así que se declara: `--renombrar salida=resultados`. Sin
declararlo, la pieza vieja cuenta como retirada y su registro queda guardado igual.

Lo normal es que no te haga falta: una actualización que solo cambia textos, prompts o reglas nuevas
entra sin tocar tu recorrido, y el arranque te lo dice si hace falta migrar. No tienes que
comprobarlo tú.

## Dónde queda tu trabajo

El estado de la persona vive en `mi-harness/estado.json`; el razonamiento acumulativo y recuperable,
en `mi-harness/piezas/<id>.md`. Los artefactos sugeridos pueden vivir en ese repositorio o apuntar al
repositorio diagnosticado. Los Markdown terminan con un bloque `estado-pieza` que permite recuperar
el estado si el JSON queda incompleto:

```bash
harness-lab recover \
  --state mi-harness/estado.json \
  --pieces mi-harness/piezas \
  --output mi-harness/estado.recuperado.json
```

Los estados válidos son `pendiente`, `en_curso`, `completada`, `descartada` y `deuda_aceptada`.
Responder un prompt no completa una pieza. Todo descarte exige motivo; toda deuda, responsable y
condición de revisión.

## Consentimiento

`consentimiento.reutilizacion_anonimizada` empieza en `false`. El taller funciona igual sin dar
consentimiento. Solo una aceptación explícita permite incorporar resultados anonimizados a análisis
futuros; no autoriza copiar secretos, datos personales ni artefactos confidenciales.

## Licencia

Uso interno, todos los derechos reservados. Puedes usarlo, ejecutarlo y adaptarlo dentro de tu
organización; no redistribuirlo fuera. **Lo que escribas con él es tuyo**: las decisiones y el
razonamiento de tu recorrido no están cubiertos por la licencia de la herramienta. El texto completo
está en [`LICENSE`](LICENSE).

## Si mantienes el proyecto

Doctrina, generación, contratos, migraciones y cómo se publica una actualización están en
[`docs/DESARROLLO.md`](docs/DESARROLLO.md). No hace falta leerlo para usar el taller.
