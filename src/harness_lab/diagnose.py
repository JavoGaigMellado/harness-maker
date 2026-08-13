from __future__ import annotations

from pathlib import Path

from .paths import ROOT

# Nombre del proyecto cuando no hay nada de donde sacarlo. Tiene que ser una cadena no vacía
# —el esquema lo exige— y tiene que leerse como lo que es: un hueco, no una respuesta. El
# prompt del diagnóstico propone nombres concretos y la persona elige; hasta entonces esto.
NOMBRE_SIN_DECIDIR = "por decidir"


def es_el_propio_taller(repo: Path) -> bool:
    """¿La carpeta observada es el clon de Harness-Maker en vez del proyecto de alguien?

    Distinguirlo importa porque el camino por defecto pasa justo por ahí: `--repo` toma la
    carpeta actual, y quien arranca desde el clon sin más está mirando el taller. Antes eso
    producía un diagnóstico que afirmaba «código propio» describiendo al taller y bautizaba
    el proyecto como «Harness-Maker». Para quien no tiene proyecto —el caso normal de quien
    monta un harness para su día a día— era el primer contacto, no un caso raro.
    """
    try:
        return repo.resolve() == ROOT.resolve()
    except OSError:
        return False


def observe(repo: Path) -> dict:
    files = [p for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts]
    suffixes = {p.suffix for p in files}
    manifests = [x for x in ["pyproject.toml","package.json","Cargo.toml","go.mod","requirements.txt"] if (repo/x).exists()]
    has_code = bool(suffixes & {".py",".js",".ts",".tsx",".go",".rs",".java"})
    propio = es_el_propio_taller(repo)
    donde = repo.resolve().name or str(repo.resolve())
    facts = [] if propio else [{"campo":"manifiestos","valor":manifests,"fuente":f"nombres de archivo en «{donde}»"},{"campo":"archivos","valor":len(files),"fuente":f"recorrido local de «{donde}»"}]
    # `forma_codigo` se observa, pero la observación describe el directorio escaneado y ese
    # puede no ser el proyecto de la persona: quien estrena un recorrido dentro del propio
    # taller acaba con «código propio» describiendo al taller. Va como desconocido para que
    # se ofrezca a confirmar, no para volver a mirar los ficheros. Y si lo escaneado *es* el
    # taller, el hecho no se registra siquiera: no es un dato flojo sobre el proyecto de
    # nadie, es un dato sobre otra cosa.
    if has_code and not propio:
        facts.append({"campo":"ejes.forma_codigo","valor":"codigo_propio","fuente":f"extensiones de código observadas en «{donde}»"})
    if propio:
        # Único hecho cuando lo mirado es el taller. Los manifiestos y el recuento de archivos
        # se quedan fuera a propósito: describen el taller y su `.venv`, no el trabajo de
        # quien pregunta, y bajo el rótulo «hechos observados» se leen como si fueran suyos.
        # Decir «no se ha observado nada de lo tuyo» es más exacto que dar 2.358 archivos.
        facts.append({"campo":"carpeta_observada","valor":"el propio taller","fuente":f"«{donde}» es el clon de Harness-Maker, así que no se ha observado nada del trabajo de la persona"})
    unknown = ["puesto","forma_codigo","proposito","usuarios","propietario","criterio_exito","patron_ejecucion","ritmo","madurez","fuente_entrada","datos_sensibles","herramientas_lectura","herramientas_escritura","reversibilidad","coste_prueba","capacidad_decision","horizonte_vida"]
    # La primera pregunta es por la persona, no por una carpeta. «Persona» ya es la primera
    # capa de Contexto en la doctrina, y montar un harness para el día a día de alguien que
    # no programa empieza por saber en qué consiste ese día a día. Preguntar antes por un
    # directorio obliga a quien no tiene proyecto a decir que no a algo que nunca fue suyo.
    persona = [
        "¿Quién eres y a qué te dedicas en tu día a día? Di tu puesto con tus palabras: qué tipo de trabajo haces y qué te ocupa más tiempo.",
        "Con eso, este taller te va a montar un sistema de trabajo con IA para *ese* día a día. Según el puesto se parecerá más a depurar y revisar código, a analizar datos y escribir SQL, a mantener contenidos o a atender peticiones. ¿Cuál de esas cosas es la tuya?",
    ]
    sobre_el_proyecto = [
        "¿Qué resultado concreto cuenta como éxito y quién responde por él?",
        "¿El modelo hace una llamada, sigue pasos fijos o decide su propio recorrido?",
        "¿Usa datos externos o sensibles y puede escribir en sistemas reales?",
        "¿Cuánto cuesta hoy probar un cambio en dinero, minutos y revisión humana?",
        "¿Cuál es el horizonte previsto y quién puede autorizar cambios?",
    ]
    if propio:
        carpeta = ["Solo se ha mirado el propio taller, así que no hay nada observado sobre tu trabajo. ¿Tienes una carpeta de proyecto propia sobre la que montarlo, o lo montamos sobre tu día a día sin repositorio detrás?"]
    else:
        carpeta = [f"Se ha mirado la carpeta «{donde}». ¿Es esa la de tu proyecto, y el código que hay dentro es el tuyo?"]
    return {"hechos":facts,"inferencias":[],"desconocidos":unknown,"preguntas_pendientes":persona+carpeta+sobre_el_proyecto}


def diagnostic_skeleton(repo: Path) -> dict:
    obs=observe(repo); code=next((x["valor"] for x in obs["hechos"] if x["campo"]=="ejes.forma_codigo"),"desconocido")
    # El nombre venía del nombre de la carpeta, y cuando la carpeta es el taller eso bautiza
    # el proyecto de la persona como «Harness-Maker». Se deja vacío a propósito para que el
    # diagnóstico proponga nombres según el puesto y sea ella quien elija.
    nombre = NOMBRE_SIN_DECIDIR if es_el_propio_taller(repo) else repo.name
    return {"schema_version":"1.0.0","persona":{"puesto":None},"proyecto":{"nombre":nombre,"proposito":None,"usuarios":[],"propietario":None,"criterio_exito":None},"ejes":{"forma_codigo":code,"patron_ejecucion":"desconocido","ritmo":"desconocido","madurez":"desconocido","fuente_entrada":"desconocido","datos_sensibles":None,"herramientas_lectura":None,"herramientas_escritura":None,"reversibilidad":"desconocido","coste_prueba":{"economico":None,"minutos":None,"revision_humana":None},"capacidad_decision":"desconocido","horizonte_vida":"desconocido"},"observacion":obs}
