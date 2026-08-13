"""Deja la copia lista para trabajar y abre el mapa del recorrido activo.

Reúne en un solo sitio lo que antes había que hacer a mano leyendo la guía de traslado:
comprobar el entorno, declarar el recorrido activo, validar, pasar las pruebas y abrir la
vista. Cada comprobación informa de lo que encontró, no solo de si pasó, porque el valor
de arrancar es saber en qué estado está la copia.

No instala nada ni crea entornos: eso lo hace `arrancar.py` en la raíz, que funciona sobre
un clon recién hecho sin dependencias. Aquí se supone que el paquete ya es importable.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import webbrowser
from pathlib import Path

from .generate import generate, load_anatomy
from .migrate import needs_migration, plan_migration
from .paths import HARNESS_LAB_DIR, MI_HARNESS_DIR, POINTER_PATH, ROOT
from .validate import ValidationFailure, load_json, validate_anatomy, validate_generated, validate_state
from .workspace import enable_git_hooks, init_workspace, resolve_state_path

# Dos vistas, una por recorrido. Las dos cargan sus datos por <script>, así que se abren
# con doble clic y sin servidor. `mapa_harness_lab.html` es la interfaz del taller con la
# fotografía fija de este proyecto; `diagrama_taller.html` es la que lee un recorrido propio.
MAPA_PROPIO_PROYECTO = ROOT / "diagramas" / "mapa_harness_lab.html"
MAPA_RECORRIDO = ROOT / "diagramas" / "diagrama_taller.html"

ESTADOS_ABIERTOS = ("pendiente", "en_curso")


class Paso:
    """Una comprobación del arranque, con su resultado legible."""

    def __init__(self, titulo: str) -> None:
        self.titulo = titulo
        self.ok = True
        self.detalle = ""

    def bien(self, detalle: str) -> "Paso":
        self.ok, self.detalle = True, detalle
        return self

    def mal(self, detalle: str) -> "Paso":
        self.ok, self.detalle = False, detalle
        return self


def _puntero(reparar: bool, recorrido_nuevo: bool = False, repo: Path | None = None, adoptar: bool = False) -> Paso:
    """Declara el recorrido activo, sea la primera vez o la número treinta y cuatro.

    Nunca reinicia nada. Con puntero, informa. Sin puntero, **estrena el recorrido de quien
    arranca**, en `mi-harness/`.

    Ese valor por defecto se invirtió el 2026-08-04. Antes, si el repositorio traía un
    recorrido propio en `proyectos/harness-lab/`, arrancar sin argumentos lo adoptaba: quien
    acababa de clonar aterrizaba en decisiones ajenas y con un «siguiente trabajo» que no era
    el suyo, y para empezar el suyo tenía que haber leído una tabla del README. El camino
    fácil llevaba al sitio equivocado, que es el peor reparto posible de los dos caminos.

    Ahora adoptar es explícito, con `--adoptar`, y solo lo necesita quien mantiene el
    proyecto: la copia de reparto no lleva dentro `proyectos/`, así que ahí no hay nada que
    adoptar aunque se pida.
    """
    paso = Paso("Recorrido activo")
    if POINTER_PATH.exists():
        try:
            declarado = json.loads(POINTER_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            return paso.mal(f"`.harness-maker.json` existe pero no se puede leer: {error}")
        if recorrido_nuevo and not str(declarado.get("estado", "")).startswith("mi-harness/"):
            # La negativa se mantiene —forzarla contaminaría el caso—, pero se nombra la
            # salida. Antes decía «usa una copia limpia» sin decir cómo, y quien ya había
            # arrancado la copia se quedaba en rojo sin saber qué comando lo saca.
            return paso.mal(
                f"se pidió recorrido nuevo pero el puntero ya declara "
                f"{declarado.get('estado')}. Un caso del banco no se ejecuta sobre el "
                "recorrido de otro y esto no se fuerza. Dos salidas: si es un caso del "
                "banco, clona otra vez y pon --recorrido-nuevo en el primer arranque; si "
                "solo quieres estrenar tu recorrido en esta copia, ejecuta "
                "`harness-lab init --reiniciar`, que aparta el anterior con su fecha."
            )
        estado_declarado = str(declarado.get("estado", "")) or "sin estado"
        # El puntero declara una ruta; que el archivo exista es otra cosa. Entre estrenar el
        # recorrido y terminar `/diagnostico` no hay estado todavía, así que quien arranca,
        # lo deja a medias y vuelve al día siguiente leía «ya declarado en
        # mi-harness/estado.json» sobre un archivo que no está —y en verde—, contradiciendo
        # dos líneas más abajo a su propio informe, que decía «sin ruta calculada todavía».
        if estado_declarado != "sin estado" and not (ROOT / estado_declarado).exists():
            return paso.bien(
                f"declarado en {estado_declarado}, que todavía no existe porque el "
                "diagnóstico no se ha terminado; sigue por /diagnostico"
            )
        return paso.bien(f"ya declarado en {estado_declarado}")
    if not reparar:
        return paso.mal("no existe `.harness-maker.json`; las actividades se detendrán")
    if adoptar and (HARNESS_LAB_DIR / "diagnostico.json").exists():
        init_workspace(ROOT, POINTER_PATH, HARNESS_LAB_DIR, ROOT)
        return paso.bien("adoptado proyectos/harness-lab sin sobrescribir su diagnóstico")
    if adoptar:
        return paso.mal(
            "se pidió adoptar el recorrido de Harness-Maker, pero esta copia no lo trae: "
            "`proyectos/harness-lab/` no viaja al reparto. Arranca sin `--adoptar` y "
            "estrenarás el tuyo."
        )
    init_workspace(ROOT, POINTER_PATH, MI_HARNESS_DIR, repo or ROOT)
    return paso.bien("recorrido nuevo y vacío en mi-harness/; empieza por /diagnostico")


def _derivados() -> Paso:
    """Pone al día lo generado, para que la vista muestre el estado de ahora.

    Sin esto, abrir el mapa después de tocar el estado enseñaba la fotografía anterior
    sin avisar. Regenerar es idempotente y su fuente manda, así que se hace siempre que
    haga falta; lo que no se hace es callarlo.
    """
    paso = Paso("Vistas y prompts generados")
    desfase = validate_generated()
    if not desfase:
        return paso.bien("al día con datos/anatomia.json y el estado activo")
    generate()
    resto = validate_generated()
    if resto:
        return paso.mal(
            f"{len(desfase)} desfasados y {len(resto)} siguen sin cuadrar tras regenerar:\n"
            + "\n".join(f"  - {e}" for e in resto[:8])
        )
    return paso.bien(f"{len(desfase)} regenerados para reflejar el estado de ahora")


def _guardian() -> Paso:
    """El guardián de git no viaja activado: se arma una vez por copia."""
    paso = Paso("Guardián de generados")
    # Se mira antes de actuar: `enable_git_hooks` es idempotente y no distingue entre
    # «lo he activado» y «ya lo estaba», así que informar sin comprobar era afirmar de más.
    def configurado() -> bool:
        hooks = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        return hooks.stdout.strip() == ".githooks"

    if configurado():
        return paso.bien("ya estaba activado (core.hooksPath = .githooks)")
    enable_git_hooks(ROOT)
    if configurado():
        return paso.bien("activado ahora (core.hooksPath = .githooks)")
    return paso.mal("no se pudo activar; los commits no comprobarán los generados")


def _ruta_estado() -> Path | None:
    """La ruta del estado activo, o None si el recorrido aún no tiene ruta calculada.

    Un recorrido recién estrenado solo tiene `diagnostico.json`: el estado lo escribe
    `plan` después de que la persona complete los desconocidos. Tratarlo como error
    dejaba el primer arranque en rojo por hacer lo que le toca.
    """
    if not POINTER_PATH.exists():
        return None
    try:
        ruta = resolve_state_path(ROOT, POINTER_PATH)
    except ValidationFailure:
        return None
    return ruta if ruta.exists() else None


def _validacion() -> Paso:
    paso = Paso("Validación")
    errores = validate_anatomy() + validate_generated()
    estado = _ruta_estado()
    if estado is not None:
        # Antes de enseñar errores de esquema se comprueba si la causa es una doctrina
        # nueva. Quien se pone al día por `git pull` recibe piezas cambiadas sin haber
        # tocado nada, y «referencia a pieza inexistente» le dice qué falla pero no qué
        # hacer. Con la causa identificada, el arranque nombra el comando que lo arregla.
        try:
            plan = plan_migration(load_anatomy(), load_json(estado))
        except (ValidationFailure, KeyError, OSError):
            plan = None
        if plan is not None and needs_migration(plan):
            relativa = estado.relative_to(ROOT).as_posix() if estado.is_relative_to(ROOT) else estado.as_posix()
            detalle = (
                f"tu recorrido se planificó con la doctrina {plan['de']} y esta copia ya trae la "
                f"{plan['a']}. No has hecho nada mal: la actualización trae piezas distintas.\n"
                f"  Llévalo a la doctrina nueva sin perder trabajo:\n"
                f"    harness-lab migrate --state {relativa} --output {relativa}.migrado\n"
                f"  Enseña primero qué cambiaría con `--solo-comprobar`; el original no se toca."
            )
            if plan["retiradas"] or plan["nuevas"]:
                detalle += f"\n  Piezas retiradas: {plan['retiradas'] or 'ninguna'} · nuevas: {plan['nuevas'] or 'ninguna'}"
            return paso.mal(detalle)
        try:
            errores += validate_state(load_json(estado))
        except ValidationFailure as error:
            errores.append(str(error))
    if errores:
        return paso.mal("\n".join(f"  - {e}" for e in errores[:12]))
    if estado is None:
        return paso.bien("anatomía y generados cuadran; el recorrido aún no tiene ruta")
    return paso.bien("anatomía, generados y recorrido activo cuadran")


def _pruebas() -> Paso:
    paso = Paso("Pruebas")
    resultado = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    ultima = [x for x in resultado.stdout.strip().splitlines() if x.strip()]
    resumen = ultima[-1] if ultima else "sin salida"
    if resultado.returncode != 0:
        return paso.mal(resumen)
    return paso.bien(resumen)


def _fotografia() -> tuple[Paso, str | None]:
    """Cuenta el recorrido y señala el siguiente trabajo, si queda alguno."""
    paso = Paso("Estado del recorrido")
    if not POINTER_PATH.exists():
        return paso.mal("sin recorrido activo que contar"), None
    ruta = _ruta_estado()
    if ruta is None:
        # Recorrido estrenado y sin ruta: no es un fallo, es el punto de partida.
        return paso.bien("recorrido nuevo, sin ruta calculada todavía"), "diagnostico"
    try:
        estado = load_json(ruta)
    except (ValidationFailure, OSError) as error:
        return paso.mal(f"no se puede leer el estado: {error}"), None

    # La ruta manda, no el diccionario de piezas. Una actividad que nadie ha tocado todavía
    # no figura en `piezas`, así que contar solo ese diccionario daba «no queda nada abierto»
    # con las 18 sin empezar. Se recorre la ruta y se mira el registro solo si existe.
    piezas = estado.get("piezas", {})
    pasos = estado.get("ruta", {}).get("pasos", [])
    recuento: dict[str, int] = {}
    sin_verificar = []
    siguiente = None
    for aso in pasos:
        pid = aso.get("pieza_id")
        registro = piezas.get(pid)
        actual = registro.get("estado", "?") if registro else "pendiente"
        recuento[actual] = recuento.get(actual, 0) + 1
        if registro:
            verificacion = registro.get("verificacion") or {}
            if verificacion.get("estado") == "no_verificada":
                sin_verificar.append(pid)
        if siguiente is None and actual in ESTADOS_ABIERTOS:
            siguiente = pid

    reparto = " · ".join(f"{n} {k}" for k, n in sorted(recuento.items()))
    if sin_verificar:
        reparto += f" · sin verificar: {', '.join(sorted(sin_verificar))}"
    if not pasos:
        return paso.bien("recorrido nuevo, sin ruta calculada todavía"), "diagnostico"

    if siguiente is None and sin_verificar:
        siguiente = sin_verificar[0]
    return paso.bien(reparto), siguiente


def en_claude_code() -> bool:
    """¿Se está ejecutando dentro de Claude Code, o en un terminal suelto?

    Importa porque el último mensaje del arranque manda a `/diagnostico`, y una barra es
    un comando de Claude Code: en PowerShell no existe. Quien arranca desde un terminal
    suelto no ve un error, ve un taller que no hace nada, y eso no se parece a «te falta
    una herramienta».

    Se mira `CLAUDECODE`, que Claude Code exporta al proceso hijo. Si algún día dejara de
    hacerlo, el fallo cae del lado bueno: se enseña la explicación larga a quien no la
    necesita, en vez de callarla a quien sí.
    """
    return bool(os.environ.get("CLAUDECODE"))


def _mapa() -> Path:
    """La vista que corresponde al recorrido activo, no una fija.

    Quien continúa este proyecto quiere su mapa con la fotografía fijada; quien estrena
    un recorrido propio quiere el diagrama que lee `mi-harness/`. Abrir el que no toca
    enseña el trabajo de otro y parece que el suyo se ha perdido.
    """
    if POINTER_PATH.exists():
        try:
            declarado = json.loads(POINTER_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            declarado = {}
        if str(declarado.get("estado", "")).startswith("mi-harness/"):
            return MAPA_RECORRIDO
    # El mapa del propio proyecto no viaja al reparto, así que se comprueba antes de
    # ofrecerlo: prometer una vista que no está en la copia deja al arranque diciendo
    # «no se encuentra» sin que nadie haya hecho nada mal.
    return MAPA_PROPIO_PROYECTO if MAPA_PROPIO_PROYECTO.exists() else MAPA_RECORRIDO


def start(
    abrir: bool = True,
    reparar: bool = True,
    recorrido_nuevo: bool = False,
    repo: Path | None = None,
    adoptar: bool = False,
) -> int:
    """Prepara la copia, informa de su estado y abre el mapa. Devuelve el código de salida."""
    # El orden importa: primero se sabe qué recorrido manda, después se pone al día lo
    # generado a partir de él, y solo entonces se valida y se abre la vista.
    pasos = [_puntero(reparar, recorrido_nuevo, repo, adoptar), _derivados(), _guardian(), _validacion(), _pruebas()]
    fotografia, siguiente = _fotografia()
    pasos.append(fotografia)

    print("Arranque de Harness-Maker")
    print(f"Python {sys.version.split()[0]} · raíz {ROOT}")
    print("")
    for paso in pasos:
        marca = "OK  " if paso.ok else "MAL "
        print(f"{marca}{paso.titulo}: {paso.detalle}")

    print("")
    mapa = _mapa()
    if abrir and mapa.exists():
        webbrowser.open(mapa.as_uri())
        print(f"Mapa abierto en el navegador: {mapa.relative_to(ROOT).as_posix()}")
    elif abrir:
        print(f"No se encuentra el mapa en {mapa.relative_to(ROOT).as_posix()}")

    fallos = [p.titulo for p in pasos if not p.ok]
    if fallos:
        print("")
        print(f"Hay {len(fallos)} comprobación(es) en rojo: {', '.join(fallos)}.")
        print("Arréglalo antes de recorrer actividades: trabajar sobre rojo confunde")
        print("un fallo del taller con un fallo de la máquina.")
        return 1

    if siguiente:
        if en_claude_code():
            print(f"Siguiente trabajo: la actividad `{siguiente}`. Ábrela con /{siguiente}.")
        else:
            # Decir «/diagnostico» a quien está en PowerShell es mandarlo a un comando que
            # ahí no existe, y el atasco no se parece a un fallo: se parece a que el taller
            # no hace nada. Quien arranca desde un terminal suelto necesita saber primero
            # dónde se sigue.
            print(f"Siguiente trabajo: la actividad `{siguiente}`.")
            print("")
            print("Se sigue desde Claude Code, no desde este terminal: `/` es un comando suyo.")
            print(f"Abre esta carpeta en Claude Code y escribe /{siguiente} ahí.")
    else:
        print("No queda actividad abierta ni verificación pendiente en el recorrido activo.")
    return 0
