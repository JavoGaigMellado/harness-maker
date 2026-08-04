"""Lleva el recorrido de una persona a la anatomía vigente sin perder su trabajo.

Existía la política y no el mecanismo. `docs/MANTENIMIENTO.md` describe siete pasos de
migración desde el 2026-08-02 y nada los ejecutaba. Mientras el repositorio fue de una
sola persona no se notaba, porque quien cambiaba la doctrina era quien tenía el recorrido
delante. Con copias ajenas que se ponen al día por `git pull`, un cambio de piezas deja el
recorrido de otro inválido —«referencia a pieza inexistente»— y sin salida: `mi-harness/`
es justo la carpeta que ninguna actualización puede alcanzar.

Dos reglas que no se negocian:

- **No modifica el estado de origen.** Escribe una copia nueva y deja escrito de dónde
  viene. Un migrador que edita en sitio no tiene vuelta atrás.
- **No borra trabajo.** Una pieza que la doctrina retira se guarda entera dentro de la
  entrada de `migraciones`, con sus decisiones y sus evidencias. Este proyecto aparta y
  marca en vez de borrar, y una migración no es la excepción.

Un renombre no se adivina: `prompts` → `prompts_v2` es indistinguible de «prompts
retirada, prompts_v2 nueva» mirando solo las dos anatomías. Lo declara quien migra, con
`--renombrar viejo=nuevo`; sin declararlo, la pieza vieja se trata como retirada.
"""

from __future__ import annotations

from copy import deepcopy

from .planner import calculate_steps, now

# Una pieza cerrada es trabajo hecho: su paso conserva el razonamiento con el que se
# planificó y la migración no lo recalcula.
CERRADOS = {"completada", "descartada", "deuda_aceptada"}


def parse_renames(pairs: list[str]) -> dict[str, str]:
    """Convierte `viejo=nuevo` en un mapa, y explica el error en vez de reventar."""
    renames: dict[str, str] = {}
    for pair in pairs or []:
        viejo, _, nuevo = pair.partition("=")
        viejo, nuevo = viejo.strip(), nuevo.strip()
        if not viejo or not nuevo:
            raise ValueError(f"`--renombrar {pair}` no tiene la forma viejo=nuevo")
        renames[viejo] = nuevo
    return renames


def plan_migration(anatomy: dict, state: dict, renames: dict[str, str] | None = None) -> dict:
    """Qué cambiaría, sin escribir nada.

    Se usa en dos sitios: el arranque lo consulta para avisar en palabras en vez de
    enseñar un error de esquema, y `migrate --solo-comprobar` lo enseña antes de tocar
    nada. Que la comprobación y la migración compartan este cálculo es lo que evita que
    el aviso y el resultado puedan discrepar.
    """
    renames = dict(renames or {})
    nuevos = [p["id"] for p in anatomy["piezas"]]
    viejos = [paso["pieza_id"] for paso in state.get("ruta", {}).get("pasos", [])]
    # Solo cuentan los renombres que van de una pieza que existía a una que existe. Un
    # `--renombrar` con cualquiera de los dos lados equivocado se ignora y se dice.
    aplicables = {v: n for v, n in renames.items() if v in viejos and n in nuevos}
    ignorados = {v: n for v, n in renames.items() if v not in aplicables}
    trasladados = {aplicables.get(x, x) for x in viejos}
    retiradas = [x for x in viejos if aplicables.get(x, x) not in nuevos]
    version_vieja = state.get("anatomia_version")
    version_nueva = anatomy["doctrina_version"]
    return {
        "de": version_vieja,
        "a": version_nueva,
        "renombradas": aplicables,
        "renombres_ignorados": ignorados,
        "retiradas": retiradas,
        "nuevas": [x for x in nuevos if x not in trasladados],
        "version_distinta": version_vieja != version_nueva,
        "piezas_distintas": bool(retiradas or aplicables) or any(x not in trasladados for x in nuevos),
    }


def needs_migration(plan: dict) -> bool:
    """Hace falta migrar si cambió la versión o cambió el conjunto de piezas."""
    return bool(plan["version_distinta"] or plan["piezas_distintas"])


def _renombrar_ids(nodo, renames: dict[str, str]):
    """Reescribe cada `pieza_id` del árbol y no toca nada más.

    Es el paso «transformar solo claves conocidas». Se hace recorriendo el árbol en vez
    de enumerar sitios porque `pieza_id` aparece en los pasos, en las decisiones globales
    y dentro de cada decisión de cada pieza: una lista de sitios envejece y deja alguno
    sin migrar, que es la peor forma de fallar aquí.
    """
    if isinstance(nodo, dict):
        return {
            clave: renames.get(valor, valor) if clave == "pieza_id" and isinstance(valor, str) else _renombrar_ids(valor, renames)
            for clave, valor in nodo.items()
        }
    if isinstance(nodo, list):
        return [_renombrar_ids(x, renames) for x in nodo]
    return nodo


def _reglas_declaradas(anatomy: dict) -> dict[str, str]:
    """Id de regla → prioridad que declara, construido igual que en el validador.

    Se repite la construcción a propósito en vez de importarla: si algún día divergen,
    lo que falla es una prueba de migración, no un estado ya escrito en el disco de otra
    persona.
    """
    reglas = {r["id"]: r["prioridad"] for r in anatomy["reglas_globales"]}
    reglas.update({f"base.{p['id']}": p["prioridad_base"] for p in anatomy["piezas"]})
    reglas.update({r["id"]: r["prioridad"] for p in anatomy["piezas"] for r in p["reglas_aplicabilidad"] + p["reglas_prioridad"]})
    reglas["peticion_del_usuario"] = "alta"
    return reglas


def _recolocar_reglas(prefijo: list[dict], frescos: list[dict], anatomy: dict, renombradas: dict[str, str], notas: list[str]) -> dict:
    """Deja citable la regla de cada paso ya cerrado, sin inventar por qué se cerró.

    Un paso conserva la regla con la que se planificó, y esa regla puede haber dejado de
    existir. Dos casos distintos, y confundirlos es lo que produce un estado inválido o
    una traza falsa:

    - La regla **deriva del nombre de la pieza** (`suelo.<id>`, `base.<id>`). Entonces
      sigue al renombre: `suelo.salida` pasa a `suelo.resultados` porque el identificador
      se construye con el de la pieza, no porque se esté eligiendo otra regla.
    - La regla **ya no está declarada** o cambió de prioridad. Aquí no se adivina: el paso
      pasa a citar la que la doctrina vigente le daría hoy, y la anterior queda escrita
      dentro de la migración para que la traza no desaparezca.
    """
    reglas = _reglas_declaradas(anatomy)
    por_id = {x["pieza_id"]: x for x in frescos}
    sustituidas: dict[str, dict] = {}
    for paso in prefijo:
        if paso.get("regla") in reglas and paso.get("prioridad") == reglas[paso["regla"]]:
            continue
        derivada = next(
            (
                f"{familia}{nuevo}"
                for viejo, nuevo in renombradas.items()
                for familia in ("suelo.", "base.")
                if paso.get("regla") == f"{familia}{viejo}" and f"{familia}{nuevo}" in reglas
            ),
            None,
        )
        if derivada and reglas[derivada] == paso.get("prioridad"):
            paso["regla"] = derivada
            continue
        fresco = por_id.get(paso["pieza_id"])
        if fresco is None:
            continue
        sustituidas[paso["pieza_id"]] = {
            "antes": {k: paso.get(k) for k in ("regla", "prioridad", "porque", "origen")},
            "ahora": {k: fresco[k] for k in ("regla", "prioridad")},
        }
        notas.append(
            f"«{paso['pieza_id']}» se cerró citando «{paso.get('regla')}», que la doctrina nueva ya no "
            f"declara igual: el paso pasa a citar «{fresco['regla']}» y lo anterior queda guardado en la migración."
        )
        paso.update({k: fresco[k] for k in ("regla", "prioridad", "porque", "origen")})
    return sustituidas


def migrate_state(anatomy: dict, state: dict, renames: dict[str, str] | None = None) -> tuple[dict, list[str]]:
    """Devuelve el estado migrado y lo que hay que contarle a la persona.

    Los siete pasos de `docs/MANTENIMIENTO.md`, en orden: se lee y valida fuera de aquí,
    se copia en vez de editar, se conserva el prefijo realizado con sus decisiones y sus
    Markdown, se transforman solo los `pieza_id`, se anota la migración con de/a/fecha, se
    recalcula únicamente el tramo pendiente con las reglas nuevas y se valida la salida
    fuera de aquí.
    """
    plan = plan_migration(anatomy, state, renames)
    notas: list[str] = []
    for viejo, nuevo in plan["renombres_ignorados"].items():
        notas.append(f"Ignorado el renombre «{viejo}» → «{nuevo}»: una de las dos piezas no existe donde debería.")
    if not needs_migration(plan):
        return deepcopy(state), [*notas, "El recorrido ya está en la anatomía vigente: no hay nada que migrar."]

    resultado = _renombrar_ids(deepcopy(state), plan["renombradas"])
    piezas = resultado.get("piezas") or {}
    for viejo, nuevo in plan["renombradas"].items():
        if viejo in piezas:
            piezas[nuevo] = piezas.pop(viejo)
        notas.append(f"«{viejo}» pasa a llamarse «{nuevo}»; su registro viaja entero.")
    resultado["piezas"] = piezas

    # Lo retirado se aparta con todo dentro, no se borra. Si tenía trabajo hecho, se dice
    # con esas palabras: una pieza cerrada que desaparece de la doctrina es justo lo que
    # una persona necesita saber antes de dar la migración por buena.
    apartadas = {}
    for pid in plan["retiradas"]:
        registro = piezas.pop(pid, None)
        apartadas[pid] = registro
        if registro and registro.get("estado") in CERRADOS:
            notas.append(f"«{pid}» ya no está en la doctrina y la tenías {registro['estado']}: su registro queda guardado dentro de la migración.")
        else:
            notas.append(f"«{pid}» ya no está en la doctrina y no tenías trabajo cerrado en ella.")
    for pid in plan["nuevas"]:
        notas.append(f"«{pid}» es nueva en la doctrina y entra en el tramo pendiente.")

    cerradas = {pid for pid, pieza in piezas.items() if pieza.get("estado") in CERRADOS}
    pasos_viejos = [p for p in resultado.get("ruta", {}).get("pasos", []) if p["pieza_id"] not in plan["retiradas"]]
    frescos = calculate_steps(anatomy, resultado["diagnostico"], piezas)
    prefijo = [p for p in pasos_viejos if p["pieza_id"] in cerradas]
    pendientes = [p for p in frescos if p["pieza_id"] not in cerradas]
    sustituidas = _recolocar_reglas(prefijo, frescos, anatomy, plan["renombradas"], notas)
    pasos = [*prefijo, *pendientes]
    # El `orden` se reasigna en todos los pasos, también en los cerrados. Cuando el
    # conjunto de piezas cambia, las posiciones exactas no se pueden conservar, y dejar
    # ordinales del reparto anterior produciría números repetidos o huecos: una traza que
    # miente. Lo que el prefijo conserva es su razonamiento —prioridad, regla y porqué—,
    # que es lo que hace auditable una decisión ya tomada.
    for i, paso in enumerate(pasos, 1):
        paso["orden"] = i

    ruta = resultado["ruta"]
    ruta["pasos"] = pasos
    ruta["generada_en"] = now()
    # El esquema admite `diagnostico`, `replanificacion` y `peticion_manual`. Una
    # migración es una replanificación por causa externa: no se añade un valor nuevo al
    # enum, porque relajar el validador para que quepa el caso propio es exactamente lo
    # que `MANTENIMIENTO.md` prohíbe.
    ruta["motivo"] = "replanificacion"
    ruta.setdefault("replanificaciones", []).append({
        "fecha": now(),
        "motivo": f"Migración de la anatomía {plan['de']} a {plan['a']}",
        "regla": "reglas_declaradas",
        "prefijo_inmutable": [p["pieza_id"] for p in prefijo],
        "antes_pendiente": [p["pieza_id"] for p in pasos_viejos if p["pieza_id"] not in cerradas],
        "despues_pendiente": [p["pieza_id"] for p in pendientes],
    })

    resultado["anatomia_version"] = plan["a"]
    resultado.setdefault("migraciones", []).append({
        "de": plan["de"],
        "a": plan["a"],
        "fecha": now(),
        "renombradas": plan["renombradas"],
        "piezas_retiradas": apartadas,
        "piezas_nuevas": plan["nuevas"],
        "reglas_sustituidas": sustituidas,
        "orden_reasignado": True,
        "motivo": "El conjunto de piezas o la versión de la doctrina cambiaron; el prefijo realizado se conserva y solo se recalculó el tramo pendiente.",
    })
    notas.append(f"Recorrido migrado de {plan['de']} a {plan['a']}: {len(prefijo)} paso(s) conservados y {len(pendientes)} recalculados.")
    return resultado, notas
