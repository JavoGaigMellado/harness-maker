# Dónde vive el harness de Harness-Maker

Inventario único de los mecanismos que hacen funcionar este proyecto. Si buscas dónde tocar una regla,
está aquí; si añades una nueva, dile a esta página en qué mecanismo la pusiste y por qué.

La regla práctica que se sigue: **orientación** en instrucciones, **capacidad** en comandos,
**obligación** en vigilantes, **frontera** en permisos. Una regla vive en un solo sitio; duplicarla
crea dos verdades que se separan en cuanto una cambia.

## Los siete mecanismos

| Mecanismo | Dónde | Para qué | Hasta dónde llega |
|---|---|---|---|
| **Instrucciones** | `CLAUDE.md` | Cómo se trabaja aquí: cómo responder, dónde se cambia cada cosa, qué se comprueba al terminar | Orienta en toda la sesión. No obliga: es texto que la IA lee y sigue |
| **Comandos** | `.claude/skills/` (23) | Una capacidad por comando: las 18 actividades, más diagnóstico, cierre, incoherencias y auditoría final | Se invocan a mano con `/nombre`. Se generan desde la doctrina; no se editan a mano |
| **Vigilantes** | `.claude/hooks/` (2) | Lo que no puede saltarse: `proteger_generados.py` impide editar un archivo generado; `validar_al_cerrar.py` valida antes de terminar la sesión | Se ejecutan solos, sin que nadie los invoque. Pueden bloquear una acción. Solo alcanzan a este asistente |
| **Guardián de git** | `.githooks/pre-commit` | Comprueba antes de cada commit que los generados estén al día y para si no lo están | Alcanza a cualquiera —asistente, editor, script—, porque todo commit pasa por git. Se salta a propósito con `--no-verify` |
| **Permisos** | `.claude/settings.json` | La frontera: qué se bloquea, qué se pregunta y qué se permite sin interrumpir | Los aplica el asistente antes de actuar. Viajan con el repositorio |
| **Puntero** | `.harness-maker.json` | Cuál es el recorrido activo en esta copia | Local: excluido de git. Sin él, ninguna actividad adivina destino |
| **Programa** | `src/harness_lab/` + `taller/prompts/` | Las siete órdenes de línea de comandos y los prompts portables para asistentes que no son Claude Code | Se instala con `pip install -e .` y funciona sin ningún asistente |

## Los permisos, uno a uno

JSON no admite comentarios, así que el porqué de cada regla está aquí. Precedencia: **bloquear** gana
a **preguntar**, y **preguntar** gana a **permitir**.

**Bloqueado, sin preguntar** — daño que no se arregla contestando bien a un aviso:

- `.env`, `.env.*`, `*.pem`, `*.key`, `~/.ssh/`, `~/.aws/` — secretos y credenciales. Ni se leen.
- `sudo` — nada de este proyecto necesita permisos de administrador.
- `rm -rf` — borrado masivo.
- `git push --force` — reescribir historia publicada.
- `WebFetch`, `WebSearch` — leer de internet. Bloqueado desde el 2026-08-03 por dos motivos, y el
  segundo es el que lo hizo urgente. Uno: el taller funciona solo con disco y no necesita la red para
  nada, así que permitirlo abría una puerta sin caso de uso. Dos: **un recorrido del banco que
  resuelva algo buscando fuera deja de decir si el taller bastaba.** `curl` y `wget` ya preguntaban,
  pero estas dos herramientas no pasaban por ningún control. Si alguna vez hace falta comprobar la
  documentación de un proveedor, lo afloja una persona a mano: el asistente no toca sus propias reglas
  de permiso, y esa división viene del incidente 5.

**Se pregunta antes** — son las cuatro acciones que Herramientas y Límites y seguridad ya habían
decidido que exigen confirmación (gasto, escritura externa, borrado o movimiento, subida a remoto):

- `git push`, `git remote`, `gh` — sacar algo de esta máquina.
- `rm`, `mv`, `git reset --hard`, `git clean` — borrar o mover trabajo.
- `pip install`, `npm install` — cambiar las dependencias de la máquina.
- `curl`, `wget` — salir a la red.

**Permitido sin interrumpir** — solo lectura y las comprobaciones del propio taller, que son las que
más se repiten y no cambian nada:

- `harness-lab validate`, `harness-lab generate`, `pytest`.
- `git status`, `git diff`, `git log`, `git show`.

Todo lo demás sigue el comportamiento normal: se pregunta la primera vez. **`additionalDirectories`
está vacío a propósito**: la IA trabaja dentro de este repositorio y se detiene en su borde.

## Qué viaja y qué se queda

| Viaja con el repositorio | Se queda en tu copia |
|---|---|
| Doctrina (`datos/anatomia.json`), esquemas y diagramas | El puntero `.harness-maker.json` |
| Las 23 skills y los 22 prompts portables | Tu recorrido en `mi-harness/` |
| Los vigilantes, el guardián de git y los permisos | Los recorridos apartados `mi-harness-anterior-*` |
| El programa y sus pruebas | Tus preferencias personales del asistente |
| El banco de casos de `taller/casos/` | |

## Empezar de cero

Quien reutilice una copia con un recorrido ya avanzado:

```
harness-lab init --reiniciar
```

Aparta el recorrido anterior con su fecha (`mi-harness-anterior-<fecha>`) y arranca uno limpio.
**No borra nada**, en coherencia con la política de memoria del proyecto. Solo toca el directorio que
se está inicializando: si el puntero apuntaba a otro recorrido, ese no se mueve.

Sin `--reiniciar`, `init` se niega a pisar un puntero existente y explica qué hacer.

## Traer mejoras del taller

No hay comando propio para eso, y es deliberado: la doctrina y los comandos viajan por git y el
recorrido de cada persona vive aparte y está excluido, así que `git pull` trae las mejoras sin tocar
el trabajo de nadie. Si algún día el reparto deja de ser un clon de git, habrá que revisarlo.

## El guardián de git

Los hooks de git no viajan por sí solos, así que vive versionado en `.githooks/` y se activa con una
línea por copia:

```
git config core.hooksPath .githooks
```

`harness-lab init` lo hace solo, de modo que quien clone no arranque sin la comprobación. Si un
generado está desincronizado, el commit se detiene y dice cuál y qué ejecutar.

## Lo que no está resuelto

- **El nivel de organización no aplica**: en Contexto está decidido que Harness-Maker es un proyecto
  personal, sin políticas de terceros que cumplir. Se reabrirá si eso cambia.
- **Los permisos no cubren todo lo que la frontera dice.** Bloquean y preguntan por comandos concretos;
  la regla general de «no salir del repositorio» sigue viviendo en `CLAUDE.md` como orientación. Un
  comando raro que no coincida con ninguna regla se resolverá preguntando, no bloqueando.
- **Esta página se escribe a mano** y puede desfasarse de `.claude/settings.json`. Se repasa al cerrar
  cada actividad, como el resto de lo guardado.

---

**Fuentes:** `.claude/settings.json`, `.claude/hooks/`, `.gitignore`, `src/harness_lab/workspace.py`,
`CLAUDE.md` y `proyectos/harness-lab/estado.json` (actividades `harnessdev`, `tools`, `guardrails`,
`contexto` y `memoria`).
**Decidido por:** Javo, el 2026-08-02 y el 2026-08-03.
