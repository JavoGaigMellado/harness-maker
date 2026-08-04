from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .generate import expected_outputs, load_anatomy
from .paths import ANATOMY_PATH, SCHEMA_DIR


class ValidationFailure(ValueError):
    pass


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationFailure(f"{path}: JSON ilegible: {exc}") from exc


def _registry() -> Registry:
    registry = Registry()
    for path in SCHEMA_DIR.glob("*.schema.json"):
        schema = load_json(path)
        if "$id" in schema:
            registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return registry


def schema_errors(instance: dict, schema_name: str) -> list[str]:
    schema = load_json(SCHEMA_DIR / schema_name)
    validator = Draft202012Validator(schema, registry=_registry(), format_checker=Draft202012Validator.FORMAT_CHECKER)
    return [f"{'.'.join(map(str,e.absolute_path)) or '$'}: {e.message}" for e in sorted(validator.iter_errors(instance), key=lambda e:list(e.absolute_path))]


def validate_anatomy(data: dict | None = None) -> list[str]:
    data = data or load_anatomy(); errors = schema_errors(data,"anatomia.schema.json")
    ids=[p["id"] for p in data.get("piezas",[])]; known=set(ids)
    if len(ids)!=len(set(ids)): errors.append("piezas: identificadores duplicados")
    if len({(p["anillo"],p["angulo"]) for p in data.get("piezas",[])}) != len(ids): errors.append("piezas: posiciones visuales duplicadas")
    rules={r["id"] for r in data.get("reglas_globales",[])}
    for p in data.get("piezas",[]):
        for ref in p.get("dependencias",[])+p.get("desbloquea",[]):
            if ref not in known: errors.append(f"{p['id']}: referencia a pieza inexistente {ref}")
        for r in p.get("reglas_aplicabilidad",[])+p.get("reglas_prioridad",[]):
            if r["id"] in rules: errors.append(f"regla duplicada: {r['id']}")
            rules.add(r["id"])
    return errors


def validate_diagnostic(data: dict) -> list[str]:
    return schema_errors(data,"diagnostico.schema.json")


def validate_state(data: dict, anatomy: dict | None = None) -> list[str]:
    anatomy=anatomy or load_anatomy(); errors=schema_errors(data,"estado_taller.schema.json")
    piece_ids={p["id"] for p in anatomy["piezas"]}
    rule_priority={r["id"]:r["prioridad"] for r in anatomy["reglas_globales"]}
    rule_priority.update({f"base.{p['id']}":p["prioridad_base"] for p in anatomy["piezas"]})
    rule_priority.update({r["id"]:r["prioridad"] for p in anatomy["piezas"] for r in p["reglas_aplicabilidad"]+p["reglas_prioridad"]})
    rule_priority["peticion_del_usuario"]="alta"
    steps=data.get("ruta",{}).get("pasos",[]); routed=[x.get("pieza_id") for x in steps]
    if set(routed)!=piece_ids or len(routed)!=len(piece_ids): errors.append("ruta: debe contener exactamente las 18 piezas, sin desapariciones ni duplicados")
    for step in steps:
        rule=step.get("regla")
        if rule not in rule_priority: errors.append(f"ruta.{step.get('pieza_id')}: regla no declarada {rule!r}")
        elif step.get("prioridad") != rule_priority[rule]: errors.append(f"ruta.{step.get('pieza_id')}: prioridad no coincide con la regla {rule}")
    orders=[x.get("orden") for x in steps]
    if orders != list(range(1,len(steps)+1)): errors.append("ruta: los órdenes deben ser consecutivos y coincidir con la posición")
    for pid, status in data.get("piezas",{}).items():
        if pid not in piece_ids: errors.append(f"piezas.{pid}: pieza desconocida")
        state=status.get("estado")
        outcomes=bool(status.get("decisiones") or status.get("artefactos") or status.get("evidencias") or status.get("descarte") or status.get("deuda"))
        if state=="completada" and not outcomes: errors.append(f"piezas.{pid}: completada sin decisión, artefacto, evidencia, descarte ni deuda")
        if state=="descartada" and not (status.get("descarte") or {}).get("motivo"): errors.append(f"piezas.{pid}: descarte sin motivo")
        debt=status.get("deuda") or {}
        if state=="deuda_aceptada" and not (debt.get("responsable") and debt.get("condicion_revision")): errors.append(f"piezas.{pid}: deuda sin responsable o condición de revisión")
    return errors


def validate_generated() -> list[str]:
    errors=[]
    for path, expected in expected_outputs().items():
        if not path.exists(): errors.append(f"generado ausente: {path.relative_to(ANATOMY_PATH.parents[1])}")
        elif path.read_text(encoding="utf-8") != expected: errors.append(f"generado desincronizado: {path.relative_to(ANATOMY_PATH.parents[1])}")
    return errors


def raise_if(errors: list[str]) -> None:
    if errors: raise ValidationFailure("\n".join(f"- {e}" for e in errors))
