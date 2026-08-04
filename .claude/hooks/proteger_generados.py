#!/usr/bin/env python3
"""Impide editar a mano un archivo generado.

Regla del proyecto llevada a un mecanismo que la impone, decidida en la actividad
«Instrucciones persistentes». Un generado editado a mano se pierde en el siguiente
`harness-lab generate` sin avisar, así que el aviso se da antes.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

PREFIJOS_GENERADOS = ("taller/prompts/", ".claude/skills/")
ARCHIVOS_GENERADOS = {
    "datos/anatomia.js",
    "datos/indice_piezas.json",
    "taller/ejemplo/estado.js",
}
MARCAS = ("NO EDITAR A MANO", '"generated": true')


def es_generado(rel: str, destino: Path) -> bool:
    if rel in ARCHIVOS_GENERADOS or rel.startswith(PREFIJOS_GENERADOS):
        return True
    if rel.startswith("proyectos/") and rel.endswith("/estado.js"):
        return True
    if destino.is_file():
        cabecera = destino.read_text(encoding="utf-8", errors="replace")[:400]
        return any(marca in cabecera for marca in MARCAS)
    return False


def main() -> None:
    try:
        datos = json.load(sys.stdin)
    except Exception:
        return  # un guardián roto no puede bloquear el trabajo
    ruta = (datos.get("tool_input") or {}).get("file_path")
    if not ruta:
        return
    destino = Path(ruta)
    try:
        rel = destino.resolve().relative_to(RAIZ).as_posix()
    except ValueError:
        return  # fuera del repositorio: no es asunto de esta regla
    if not es_generado(rel, destino):
        return
    razon = (
        f"`{rel}` es un archivo generado y no se edita a mano: el siguiente "
        "`harness-lab generate` borraría el cambio sin avisar.\n\n"
        "Edita la fuente —`datos/anatomia.json` para doctrina y prompts, o el "
        "`estado.json` correspondiente para los wrappers— y regenera con "
        "`harness-lab generate`."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": razon,
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
