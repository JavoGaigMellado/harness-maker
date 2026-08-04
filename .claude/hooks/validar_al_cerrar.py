#!/usr/bin/env python3
"""No deja cerrar un turno con la validación o las pruebas en rojo.

Regla del proyecto llevada a un mecanismo que la impone, decidida en la actividad
«Instrucciones persistentes». Validar estaba escrito en varios sitios y aun así
dependía de que alguien se acordase.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def interprete() -> str:
    """El intérprete del entorno del proyecto, si lo hay.

    El vigilante puede arrancar con el Python del sistema, donde el paquete no está
    instalado. Sin esto, la comprobación fallaba por no encontrarlo y el turno se
    cerraba con el repositorio en rojo sin que nadie se enterara.
    """
    for relativa in ("Scripts/python.exe", "bin/python"):
        candidato = RAIZ / ".venv" / relativa
        if candidato.exists():
            return str(candidato)
    return sys.executable


def entorno() -> dict:
    """Deja `src/` al alcance para que valga también sin instalación editable."""
    variables = dict(os.environ)
    ruta = str(RAIZ / "src")
    previa = variables.get("PYTHONPATH")
    variables["PYTHONPATH"] = f"{ruta}{os.pathsep}{previa}" if previa else ruta
    return variables


# 50 s por comprobación: dos seguidas caben en el tope de 120 s declarado en
# settings.json. Con el tope anterior podían sumar 180 s, y un vigilante al que
# matan a mitad no bloquea nada aunque las pruebas estén en rojo.
LIMITE = 50

COMPROBACIONES = (
    ("validación", ["-m", "harness_lab", "validate", "--all"]),
    ("pruebas", ["-m", "pytest", "-q"]),
)


def main() -> None:
    try:
        datos = json.load(sys.stdin)
    except Exception:
        datos = {}
    if datos.get("stop_hook_active"):
        return  # ya se avisó una vez; no encerrar el turno en un bucle

    fallos = []
    python = interprete()
    variables = entorno()
    for etiqueta, argumentos in COMPROBACIONES:
        try:
            resultado = subprocess.run(
                [python, *argumentos],
                cwd=RAIZ,
                capture_output=True,
                text=True,
                timeout=LIMITE,
                env=variables,
            )
        except Exception as error:
            fallos.append(f"{etiqueta}: no se pudo ejecutar ({error})")
            continue
        if resultado.returncode != 0:
            salida = (resultado.stdout + resultado.stderr).strip()[-1500:]
            fallos.append(f"{etiqueta} en rojo:\n{salida}")

    if not fallos:
        return
    print(json.dumps({
        "decision": "block",
        "reason": (
            "El repositorio no queda en verde. Arréglalo antes de cerrar:\n\n"
            + "\n\n".join(fallos)
        ),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
