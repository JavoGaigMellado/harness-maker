from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .diagnose import diagnostic_skeleton
from .validate import ValidationFailure

POINTER_VERSION = "1.0.0"
COVERAGE_VERSION = "1.0.0"
REGLA_CIERRE = (
    "completada exige todos los criterios definidos o no aplicables; en_curso conserva cualquier "
    "cobertura parcial o ausente; descartada exige que todos no apliquen y un motivo; "
    "deuda_aceptada cierra con algún criterio todavía parcial solo si la deuda tiene responsable y "
    "condición de revisión."
)


def coverage_skeleton(anatomy: dict) -> dict:
    """Los 99 criterios de la anatomía, escritos y sin evaluar.

    `cobertura.json` era una fuente declarada que dos sitios leen —`/incoherencias` y el
    diagrama— y que **ningún comando producía**. Quien estrenaba un recorrido nunca la
    tenía, así que la segunda red del cierre, la que evalúa criterio por criterio, no
    existía en ninguna copia salvo en la del autor, que la escribió a mano.

    Encontrado el 2026-08-12 recorriendo el taller sobre un proyecto real en producción:
    tres criterios genéricos de cierre daban por buena una pieza donde después
    aparecieron cinco de los siete hallazgos altos de la lectura.

    Nace con todo en `no_definido` a propósito. Un esqueleto lleno de `definido` sería la
    misma mentira que se intenta arreglar; lo que hace falta es que la lista exista y se
    vea vacía.
    """
    return {
        "version": COVERAGE_VERSION,
        "anatomia_version": anatomy.get("doctrina_version"),
        "fecha": None,
        "regla_cierre": REGLA_CIERRE,
        "piezas": {
            pieza["id"]: {
                "resultado": "pendiente",
                "criterios": [
                    {"criterio": criterio, "estado": "no_definido", "evidencias": []}
                    for criterio in pieza["que_montar"]
                ],
            }
            for pieza in anatomy["piezas"]
        },
    }


def describe_workspace(workspace: Path) -> str:
    """Qué hay dentro de un recorrido, en una frase, para poder enseñarlo antes de moverlo.

    `--reiniciar` apartaba sin decir qué apartaba. El 7-ago se llevó por delante un
    recorrido con 12 piezas cerradas y 38 deudas, y el diagrama salió vacío cinco días
    después sin que nada explicara por qué. Aceptar la pérdida es decisión de la persona;
    lo que no puede es tomarse a ciegas.
    """
    estado = workspace / "estado.json"
    if not estado.exists():
        return "un recorrido sin estado calculado todavía"
    try:
        datos = json.loads(estado.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "un estado que no se puede leer"
    piezas = datos.get("piezas") or {}
    cerradas = sum(1 for p in piezas.values() if p.get("estado") in ("completada", "descartada", "deuda_aceptada"))
    deudas = sum(1 for p in piezas.values() if p.get("deuda")) + len(datos.get("deuda") or [])
    decisiones = sum(len(p.get("decisiones") or []) for p in piezas.values()) + len(datos.get("decisiones_globales") or [])
    riesgos = len(datos.get("riesgos_aceptados") or [])
    partes = [f"{cerradas} pieza(s) cerrada(s)", f"{decisiones} decisión(es)"]
    if deudas: partes.append(f"{deudas} deuda(s)")
    if riesgos: partes.append(f"{riesgos} riesgo(s) aceptado(s)")
    return "un recorrido con " + ", ".join(partes)


def restore_workspace(root: Path, pointer: Path, workspace: Path, archived: Path) -> list[Path]:
    """Devuelve a su sitio un recorrido apartado, apartando antes el que esté activo.

    `init --reiniciar` y `migrate --aplicar` apartan con fecha; hasta el 2026-08-12 nada
    traía de vuelta. Restaurar era mover carpetas a mano, que funciona pero es justo el
    tipo de operación que el taller existe para no tener que hacer a mano: una
    equivocación ahí pierde el recorrido entero.

    Simétrico a apartar y con la misma política: nada se borra. Lo que estuviera activo se
    aparta con su fecha antes de poner el restaurado en su sitio.
    """
    if not archived.exists() or not archived.is_dir():
        raise ValidationFailure(f"{archived} no existe o no es una carpeta.")
    if archived.resolve() == workspace.resolve():
        raise ValidationFailure(f"{archived.name} ya es el recorrido activo: no hay nada que restaurar.")
    if not (archived / "diagnostico.json").exists():
        raise ValidationFailure(
            f"{archived.name} no parece un recorrido: le falta `diagnostico.json`.\n"
            "Restaurar mueve una carpeta entera al sitio del recorrido activo; comprueba la ruta."
        )
    apartado = archive_workspace(workspace)
    archived.rename(workspace)
    relative = workspace.resolve().relative_to(root.resolve()).as_posix()
    pointer.write_text(json.dumps({
        "schema_version": POINTER_VERSION,
        "estado": f"{relative}/estado.json",
        "diagnostico": f"{relative}/diagnostico.json",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return [*([apartado] if apartado else []), workspace, pointer]


def _nombre_libre(base: Path, sufijo: str = "") -> Path:
    """Un nombre con fecha que no pise a otro del mismo segundo.

    La marca tiene resolución de segundo, así que dos operaciones seguidas chocaban y la
    segunda moría con «espera un segundo y repite el comando». Se toleraba porque apartar
    era raro; desde que existe `--restaurar` deja de serlo —restaurar aparta lo activo
    justo después de un reinicio— y pedirle a alguien que espere un segundo para no perder
    su recorrido es una respuesta pobre. Se desambigua con un contador y nada se pisa.
    """
    stamp=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    candidato=base.with_name(f"{base.stem if sufijo else base.name}-anterior-{stamp}{sufijo}")
    n=2
    while candidato.exists():
        candidato=base.with_name(f"{base.stem if sufijo else base.name}-anterior-{stamp}-{n}{sufijo}")
        n+=1
    return candidato


def archive_workspace(workspace: Path) -> Path | None:
    """Aparta un recorrido anterior en lugar de borrarlo.

    La política de memoria del proyecto es explícita: no se borra nada, lo superado
    se marca y se conserva como procedencia. Volver a empezar mueve, nunca destruye.
    """
    if not workspace.exists():
        return None
    archived=_nombre_libre(workspace)
    workspace.rename(archived)
    return archived


def archive_state(state: Path) -> Path:
    """Aparta una copia del estado antes de sustituirlo, con su fecha.

    Misma política que `archive_workspace`, un nivel más abajo: la usa `migrate --aplicar`
    para que dejar el recorrido migrado en su sitio no signifique perder el anterior. Se
    copia en vez de renombrar porque quien llama escribe justo después en esa misma ruta.
    """
    archived=_nombre_libre(state, state.suffix)
    archived.write_bytes(state.read_bytes())
    return archived


def read_pointer(pointer: Path) -> dict:
    """Lee el puntero al recorrido activo. Sin puntero no hay destino que adivinar."""
    if not pointer.exists():
        raise ValidationFailure(
            f"No existe {pointer.name}: este repositorio todavía no declara un recorrido activo.\n"
            "Ejecuta `harness-lab init` para crear el tuyo."
        )
    try:
        data=json.loads(pointer.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationFailure(f"{pointer.name} no es JSON válido: {exc}") from exc
    if not isinstance(data,dict) or not isinstance(data.get("estado"),str):
        raise ValidationFailure(f"{pointer.name} debe tener una clave `estado` con la ruta del recorrido activo")
    return data


def resolve_state_path(root: Path, pointer: Path) -> Path:
    """Ruta del estado activo según el puntero, sin buscar candidatos por el repositorio."""
    return (root / read_pointer(pointer)["estado"]).resolve()


def enable_git_hooks(root: Path) -> bool:
    """Activa `.githooks/` en esta copia para que el guardián de generados exista tras un clon.

    Sin esto, cada persona que clonara arrancaría sin la comprobación al guardar: los hooks
    de git no viajan. Es best-effort: si el directorio no es un repositorio, no pasa nada.
    """
    if not (root / ".githooks").is_dir():
        return False
    try:
        subprocess.run(["git","config","core.hooksPath",".githooks"],cwd=root,check=True,capture_output=True)
    except (OSError, subprocess.CalledProcessError):
        return False
    return True


def init_workspace(root: Path, pointer: Path, workspace: Path, repo: Path, restart: bool=False) -> list[Path]:
    """Crea el recorrido de esta persona y lo declara como activo.

    Es el arranque que faltaba: antes, quien clonaba escribía en el único
    `proyectos/*/estado.json` que hubiera por ser inequívoco por número.

    Con `restart`, quien reutilice una copia ya avanzada vuelve a empezar de cero:
    su recorrido se aparta con fecha y el puntero se rehace. Solo toca el directorio
    que se está inicializando; un recorrido ajeno al que apunte el puntero no se mueve.
    """
    archived=archive_workspace(workspace) if restart else None
    if pointer.exists() and not restart:
        raise ValidationFailure(
            f"{pointer.name} ya existe y apunta a `{read_pointer(pointer)['estado']}`.\n"
            "Usa `harness-lab init --reiniciar` para empezar de cero apartando el recorrido anterior,\n"
            "o edita el puntero a mano si solo quieres cambiar de recorrido activo."
        )
    diagnostic=workspace / "diagnostico.json"
    written=[]
    if diagnostic.exists():
        # Recorrido ya empezado (otra copia del mismo repositorio): se adopta tal cual,
        # nunca se sobrescribe. Solo falta declararlo activo.
        written.append(diagnostic)
    else:
        workspace.mkdir(parents=True,exist_ok=True)
        diagnostic.write_text(json.dumps(diagnostic_skeleton(repo.resolve()),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        written.append(diagnostic)
    # La cobertura nace con el recorrido, no cuando alguien se acuerda. Se escribe solo si
    # falta: una copia que ya la tenga conserva lo evaluado, igual que el diagnóstico.
    coverage=workspace / "cobertura.json"
    if not coverage.exists():
        from .generate import load_anatomy
        coverage.write_text(json.dumps(coverage_skeleton(load_anatomy()),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    written.append(coverage)
    relative=workspace.resolve().relative_to(root.resolve()).as_posix()
    pointer.write_text(json.dumps({
        "schema_version":POINTER_VERSION,
        "estado":f"{relative}/estado.json",
        "diagnostico":f"{relative}/diagnostico.json",
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return [*([archived] if archived else []),*written,pointer]
