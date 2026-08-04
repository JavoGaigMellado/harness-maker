from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def lookup(data: dict, dotted: str):
    cur = data
    for key in dotted.split("."):
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def matches(condition: dict, diagnostic: dict) -> bool:
    if condition.get("always") is True:
        return True
    if "all" in condition:
        return all(matches(x, diagnostic) for x in condition["all"])
    if "any" in condition:
        return any(matches(x, diagnostic) for x in condition["any"])
    for key, expected in condition.items():
        actual = lookup(diagnostic, key)
        if isinstance(expected, dict):
            if "in" in expected and actual not in expected["in"]:
                return False
            if "gt" in expected and not (isinstance(actual, (int, float)) and actual > expected["gt"]):
                return False
        elif actual != expected:
            return False
    return True


def _best(current: dict, candidate: dict, ranks: dict) -> dict:
    if candidate["prioridad"] == "descartar" or ranks[candidate["prioridad"]] < ranks[current["prioridad"]]:
        return candidate
    # A igualdad de prioridad gana la regla específica sobre la base o el suelo:
    # ambas llevan a lo mismo, pero la específica explica por qué le toca a esta persona.
    if ranks[candidate["prioridad"]] == ranks[current["prioridad"]] and current["origen"] in {"base", "suelo"}:
        return candidate
    return current


def calculate_steps(anatomy: dict, diagnostic: dict, piece_states: dict | None = None, manual: list[str] | None = None) -> list[dict]:
    states = piece_states or {}
    manual = manual or []
    ranks = {k: v["orden"] for k, v in anatomy["prioridades"].items()}
    globals_by_piece = {r["id"].split(".", 1)[1]: r for r in anatomy["reglas_globales"]}
    items = []
    for piece in anatomy["piezas"]:
        chosen = {"prioridad": piece["prioridad_base"], "regla": f"base.{piece['id']}", "porque": f"Prioridad base declarada para {piece['nombre']}.", "origen": "base"}
        floor = globals_by_piece.get(piece["id"])
        if floor and matches(floor["condicion"], diagnostic):
            chosen = {"prioridad": floor["prioridad"], "regla": floor["id"], "porque": floor["porque"], "origen": "suelo"}
        for rule in piece["reglas_aplicabilidad"] + piece["reglas_prioridad"]:
            if matches(rule["condicion"], diagnostic):
                cand = {"prioridad": rule["prioridad"], "regla": rule["id"], "porque": rule["porque"], "origen": "regla"}
                chosen = _best(chosen, cand, ranks)
        if piece["id"] in manual:
            chosen = {"prioridad": "alta", "regla": "peticion_del_usuario", "porque": "La persona pidió priorizar esta pieza.", "origen": "peticion_manual"}
        state = states.get(piece["id"], {}).get("estado", "pendiente")
        items.append({"pieza_id": piece["id"], **chosen, "estado_al_planificar": state, "_deps": piece["dependencias"], "_index": len(items)})
    # Prioridad primero; dependencias solo adelantan si ambas siguen pendientes.
    ordered = sorted(items, key=lambda x: (ranks[x["prioridad"]], x["_index"]))
    changed = True
    while changed:
        changed = False
        pos = {x["pieza_id"]: i for i, x in enumerate(ordered)}
        for i, item in enumerate(ordered):
            for dep in item["_deps"]:
                if dep in pos and pos[dep] > i:
                    ordered.insert(i, ordered.pop(pos[dep])); changed = True; break
            if changed: break
    return [{k: v for k, v in item.items() if not k.startswith("_")} | {"orden": i} for i, item in enumerate(ordered, 1)]


def initial_state(anatomy: dict, diagnostic: dict, manual: list[str] | None = None) -> dict:
    return {"schema_version":"1.0.0","anatomia_version":anatomy["doctrina_version"],"consentimiento":{"reutilizacion_anonimizada":False,"registrado_en":None},"diagnostico":diagnostic,"ruta":{"generada_en":now(),"motivo":"peticion_manual" if manual else "diagnostico","pasos":calculate_steps(anatomy,diagnostic,manual=manual),"replanificaciones":[]},"piezas":{},"decisiones_globales":[],"riesgos_aceptados":[],"deuda":[],"migraciones":[]}


def replan(anatomy: dict, state: dict, manual: list[str] | None = None) -> dict:
    result = deepcopy(state)
    old = state["ruta"]["pasos"]
    completed_ids = {k for k,v in state.get("piezas",{}).items() if v.get("estado") in {"completada","descartada","deuda_aceptada"}}
    fresh = calculate_steps(anatomy,state["diagnostico"],state.get("piezas"),manual)
    pending = [x for x in fresh if x["pieza_id"] not in completed_ids]
    pending_iter = iter(pending)
    # Un paso cerrado conserva objeto y posición. Solo se rellenan de nuevo los huecos pendientes.
    merged = [deepcopy(x) if x["pieza_id"] in completed_ids else next(pending_iter) for x in old]
    for i,x in enumerate(merged,1):
        if x["pieza_id"] not in completed_ids:
            x["orden"] = i
    result["ruta"]["pasos"] = merged
    result["ruta"]["generada_en"] = now(); result["ruta"]["motivo"] = "peticion_manual" if manual else "replanificacion"
    result["ruta"]["replanificaciones"].append({"fecha":now(),"motivo":"Petición manual" if manual else "Cambio de diagnóstico o estado","regla":"peticion_del_usuario" if manual else "reglas_declaradas","prefijo_inmutable":[x["pieza_id"] for x in old if x["pieza_id"] in completed_ids],"antes_pendiente":[x["pieza_id"] for x in old if x["pieza_id"] not in completed_ids],"despues_pendiente":[x["pieza_id"] for x in merged if x["pieza_id"] not in completed_ids]})
    return result
