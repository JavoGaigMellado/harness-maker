#!/usr/bin/env python3
"""Prepara una copia recién clonada y la deja lista para trabajar.

Único punto de entrada desde cero. Solo usa la biblioteca estándar, así que funciona
antes de instalar nada y en cualquier sistema operativo:

    python arrancar.py

Crea el entorno virtual si falta, instala el paquete, declara el recorrido activo,
valida, pasa las pruebas y abre el mapa. Es idempotente: volver a ejecutarlo sobre una
copia ya lista solo comprueba y abre la vista.

Lo que no hace: instalar Python, tocar el recorrido de otro proyecto ni reiniciar el
recorrido existente. Un arranque no debe poder destruir trabajo.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
VENV = RAIZ / ".venv"
SUELO = (3, 12)


def interprete_venv() -> Path:
    """El python del entorno, con el nombre que le da cada sistema operativo."""
    if os.name == "nt":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def aviso(texto: str) -> None:
    print(f"  {texto}")


def ejecutar(comando: list[str], titulo: str) -> bool:
    resultado = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
    if resultado.returncode == 0:
        return True
    print(f"MAL {titulo}")
    salida = (resultado.stdout + resultado.stderr).strip()
    for linea in salida.splitlines()[-15:]:
        aviso(linea)
    return False


def main() -> int:
    print("Preparando Harness-Maker")
    print("")

    if sys.version_info < SUELO:
        actual = ".".join(str(x) for x in sys.version_info[:3])
        minimo = ".".join(str(x) for x in SUELO)
        print(f"MAL Python {actual} es anterior al suelo del proyecto ({minimo} o posterior).")
        aviso(f"Instala Python {minimo} o superior y vuelve a ejecutar este arrancador.")
        return 1

    python = interprete_venv()
    if python.exists():
        print(f"OK  Entorno virtual: ya existe en .venv")
    else:
        print("... Creando el entorno virtual en .venv")
        if not ejecutar([sys.executable, "-m", "venv", str(VENV)], "no se pudo crear .venv"):
            return 1
        print("OK  Entorno virtual creado")

    # Se instala siempre: es barato cuando ya está y evita el fallo más común, que es
    # un entorno creado en una sesión anterior y quedado sin el paquete.
    print("... Instalando el paquete y sus dependencias de desarrollo")
    if not ejecutar(
        [str(python), "-m", "pip", "install", "-q", "-e", ".[dev]"],
        "falló la instalación",
    ):
        return 1
    print("OK  Paquete instalado")
    print("")

    # A partir de aquí manda `harness-lab start`: la lógica vive en el paquete, para que
    # no haya dos versiones de la misma comprobación que puedan discrepar. Los argumentos
    # se pasan tal cual, así que `python arrancar.py --recorrido-nuevo` vale para preparar
    # un caso del banco sin tener que conocer la CLI por dentro.
    return subprocess.run(
        [str(python), "-m", "harness_lab", "start", *sys.argv[1:]], cwd=RAIZ
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
