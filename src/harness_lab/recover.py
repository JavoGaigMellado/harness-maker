from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

BLOCK = re.compile(r"```estado-pieza\s*\n(.*?)\n```", re.DOTALL)


def recover_from_markdown(state: dict, pieces_dir: Path) -> tuple[dict, list[str]]:
    result=deepcopy(state); notes=[]; result.setdefault("piezas",{})
    for path in sorted(pieces_dir.glob("*.md")):
        matches=BLOCK.findall(path.read_text(encoding="utf-8"))
        if not matches:
            notes.append(f"{path.name}: sin bloque estado-pieza"); continue
        try: piece=json.loads(matches[-1])
        except json.JSONDecodeError as exc:
            notes.append(f"{path.name}: bloque corrupto ({exc})"); continue
        pid=path.stem; piece["markdown_fuente"]=str(path)
        current=result["piezas"].get(pid)
        if current and current.get("fechas",{}).get("actualizada") and piece.get("fechas",{}).get("actualizada") and current["fechas"]["actualizada"] > piece["fechas"]["actualizada"]:
            notes.append(f"{path.name}: estado JSON más reciente, no sustituido"); continue
        result["piezas"][pid]=piece; notes.append(f"{path.name}: recuperada")
    return result, notes
