from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .diagnose import diagnostic_skeleton
from .validate import ValidationFailure

POINTER_VERSION = "1.0.0"


def archive_workspace(workspace: Path) -> Path | None:
    """Aparta un recorrido anterior en lugar de borrarlo.

    La política de memoria del proyecto es explícita: no se borra nada, lo superado
    se marca y se conserva como procedencia. Volver a empezar mueve, nunca destruye.
    """
    if not workspace.exists():
        return None
    stamp=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    archived=workspace.with_name(f"{workspace.name}-anterior-{stamp}")
    if archived.exists():
        raise ValidationFailure(f"{archived.name} ya existe: espera un segundo y repite el comando.")
    workspace.rename(archived)
    return archived


def archive_state(state: Path) -> Path:
    """Aparta una copia del estado antes de sustituirlo, con su fecha.

    Misma política que `archive_workspace`, un nivel más abajo: la usa `migrate --aplicar`
    para que dejar el recorrido migrado en su sitio no signifique perder el anterior. Se
    copia en vez de renombrar porque quien llama escribe justo después en esa misma ruta.
    """
    stamp=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    archived=state.with_name(f"{state.stem}-anterior-{stamp}{state.suffix}")
    if archived.exists():
        raise ValidationFailure(f"{archived.name} ya existe: espera un segundo y repite el comando.")
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
    relative=workspace.resolve().relative_to(root.resolve()).as_posix()
    pointer.write_text(json.dumps({
        "schema_version":POINTER_VERSION,
        "estado":f"{relative}/estado.json",
        "diagnostico":f"{relative}/diagnostico.json",
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return [*([archived] if archived else []),*written,pointer]
