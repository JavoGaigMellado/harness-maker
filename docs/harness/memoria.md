# Qué guarda Harness-Maker

Página de relevo: si llegas nuevo al proyecto, o vuelves después de un tiempo, esto es lo que hay
guardado, dónde vive y quién puede tocarlo.

Es un resumen escrito a mano. **La fuente de verdad es `proyectos/harness-lab/estado.json`**; si esta
página y el estado no coinciden, manda el estado.

## Las cinco cosas, separadas a propósito

No se guardan todas en el mismo sitio. Si compartieran archivo competirían por espacio y se pisarían.

| Qué es | Dónde vive | Quién lo edita |
|---|---|---|
| **Memoria** — preferencias y hechos sobre la persona y el proyecto | `proyectos/harness-lab/estado.json`, en la actividad `contexto` | La IA escribe; Javo aprueba lo doctrinal |
| **Estado** — por dónde va cada actividad | `proyectos/harness-lab/estado.json` y `cobertura.json` | La IA, al cerrar cada actividad |
| **Conocimiento** — de dónde sale lo que se afirma | `datos/anatomia.json` (doctrina) y `historia/` (procedencia congelada) | Javo la doctrina; la IA solo los derivados regenerados |
| **Instrucciones** — cómo se trabaja aquí | `CLAUDE.md`, `README.md`, `docs/MANTENIMIENTO.md` y las skills generadas | Javo las reglas; la IA regenera las skills desde la doctrina |
| **Historial** — qué pasó y cuándo | `git` y los Markdown acumulativos de `proyectos/harness-lab/piezas/` | La IA escribe; nadie reescribe lo pasado |

## Qué sobrevive de una sesión a la siguiente

Cuatro cosas, y con eso basta para retomar sin reconstruir nada a mano:

1. Quién eres y qué organización hay detrás.
2. Qué es el proyecto y cuál es su doctrina vigente.
3. La tarea en curso.
4. El cierre de la sesión anterior: qué se decidió y con qué evidencia, cuál es la siguiente pregunta
   abierta, qué se probó y se descartó con su motivo, y el commit del hito.

Al arrancar se carga solo el punto del recorrido (`estado.json`, `cobertura.json` y `git status`).
Las reglas fijas no se precargan: viven en `README.md` y `docs/MANTENIMIENTO.md` y se consultan cuando
hacen falta. `historia/` y `referencia/` no se abren salvo que alguien lo pida.

## Quién puede cambiar qué

- **La IA** escribe y actualiza el recorrido: estado, cobertura, los Markdown de cada actividad y los
  derivados generados.
- **Javo** aprueba cualquier cambio de doctrina o de contrato: `datos/anatomia.json`, los esquemas y
  `diagramas/diagrama_base.html` no se tocan como efecto lateral.
- Los archivos que empiezan por `GENERADO` o `NO EDITAR A MANO` no se editan: se cambia su fuente y se
  regeneran con `python3 -m harness_lab generate`.

## Qué se repasa y qué se borra

Lo guardado se repasa **al cerrar cada actividad**, no por calendario.

**No se borra nada, y no hay fecha de caducidad.** Eso es la política completa, no un hueco por
rellenar: lo que queda superado se marca como superado y se conserva como procedencia, para que
siempre se pueda ver de dónde salió una decisión.

## Si el estado se corrompe

Cada Markdown de `proyectos/harness-lab/piezas/` termina con un bloque cercado `estado-pieza` que
contiene el JSON de esa actividad. `src/harness_lab/recover.py` recupera el último bloque válido sin
pisar un JSON más reciente, y hay una prueba automática que lo cubre
(`tests/test_acceptance.py::test_recovery_from_accumulative_markdown`).

## Lo que todavía no está comprobado

- **Que esta página funcione.** Que otra persona entienda el estado leyendo y pueda continuar no se ha
  demostrado. Se comprobará con la batería de usuarios simulados de la actividad de pruebas, que
  incluirá al menos un recorrido que retome un proyecto a medias. Es una verificación pendiente, no
  una norma por definir.
- **Que el arranque funcione para otra persona.** El remoto privado y la copia sincronizada ya
  existen; falta observar a una persona ajena clonando y arrancando sin ayuda.
- **Que esta página siga al día.** Está escrita a mano y puede desfasarse respecto al estado. Se repasa
  al cerrar cada actividad, como el resto de lo guardado.

---

**Fuentes:** `proyectos/harness-lab/estado.json` (actividades `memoria`, `contexto`, `conocimiento`,
`historial` y `eval`), `proyectos/harness-lab/piezas/memoria.md` y `CLAUDE.md`.
**Decidido por:** Javo, el 2026-08-02 y el 2026-08-03.
