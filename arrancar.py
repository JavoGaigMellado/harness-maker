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


def venv_utilizable(python: Path) -> bool:
    """Que el ejecutable arranque no basta: hay que poder instalar con él.

    Un arranque interrumpido a mitad deja `.venv` a medias, y hay dos formas de quedarse a
    medias, no una. La primera comprobación miraba solo que el archivo existiera; la segunda,
    que el python arrancara. Ninguna cubre el corte más probable: `venv` coloca el intérprete
    y después ejecuta `ensurepip`, así que un Ctrl+C en medio deja un python que arranca
    perfectamente y no tiene pip. Ese entorno pasaba en verde, el arrancador decía «ya existe»
    y se estrellaba en el paso siguiente con «No module named pip», que ni nombra la causa ni
    dice que hay que borrar `.venv`.

    Se prueba directamente lo que se va a usar —pip— porque arrancar es condición de eso: si
    pip responde, el intérprete arrancó. Una sola llamada en el camino bueno.
    """
    if not python.exists():
        return False
    return subprocess.run([str(python), "-m", "pip", "--version"], capture_output=True).returncode == 0


def diagnostico_venv(python: Path) -> str:
    """Por qué no sirve el `.venv` que hay. Solo se llama cuando ya se sabe que no sirve.

    Decir «está a medias» sin decir de qué manera obliga a la persona a investigarlo, y el
    arreglo es el mismo en los dos casos. Se distingue igualmente para que el mensaje no
    afirme algo que no ha comprobado.
    """
    if subprocess.run([str(python), "-c", ""], capture_output=True).returncode != 0:
        return "su python existe pero no arranca"
    return "su python arranca pero se quedó sin pip"


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
    if venv_utilizable(python):
        print("OK  Entorno virtual: ya existe en .venv")
    elif python.exists():
        print(f"MAL El .venv está a medias: {diagnostico_venv(python)}.")
        aviso("Suele pasar cuando un arranque anterior se interrumpió a mitad.")
        aviso("Bórralo y repite:  Remove-Item -Recurse -Force .venv   (en Linux o macOS, rm -rf .venv)")
        return 1
    else:
        # Los dos pasos que siguen son, con diferencia, los más lentos: en Windows, con antivirus
        # de por medio, crear el entorno e instalar puede pasar del minuto. La salida se captura
        # para no inundar la consola, así que sin este aviso el arrancador se queda mudo justo
        # cuando más tarda y parece colgado. Alguien lo interrumpió por eso, y un Ctrl+C aquí
        # deja el `.venv` a medias.
        print("... Creando el entorno virtual en .venv")
        aviso("Esto y la instalación tardan uno o dos minutos la primera vez. No lo interrumpas:")
        aviso("un corte a mitad deja el entorno inservible y hay que borrarlo a mano.")
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
