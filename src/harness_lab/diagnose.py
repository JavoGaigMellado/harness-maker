from __future__ import annotations

from pathlib import Path


def observe(repo: Path) -> dict:
    files = [p for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts]
    suffixes = {p.suffix for p in files}
    manifests = [x for x in ["pyproject.toml","package.json","Cargo.toml","go.mod","requirements.txt"] if (repo/x).exists()]
    has_code = bool(suffixes & {".py",".js",".ts",".tsx",".go",".rs",".java"})
    donde = repo.resolve().name or str(repo.resolve())
    facts = [{"campo":"manifiestos","valor":manifests,"fuente":f"nombres de archivo en «{donde}»"},{"campo":"archivos","valor":len(files),"fuente":f"recorrido local de «{donde}»"}]
    if has_code: facts.append({"campo":"ejes.forma_codigo","valor":"codigo_propio","fuente":f"extensiones de código observadas en «{donde}»"})
    # `forma_codigo` se observa, pero la observación describe el directorio escaneado y ese
    # puede no ser el proyecto de la persona: quien estrena un recorrido dentro del propio
    # taller acaba con «código propio» describiendo al taller. Va como desconocido para que
    # se ofrezca a confirmar, no para volver a mirar los ficheros.
    unknown = ["forma_codigo","proposito","usuarios","propietario","criterio_exito","patron_ejecucion","ritmo","madurez","fuente_entrada","datos_sensibles","herramientas_lectura","herramientas_escritura","reversibilidad","coste_prueba","capacidad_decision","horizonte_vida"]
    questions = [f"Se ha mirado la carpeta «{donde}». ¿Es esa la de tu proyecto, y el código que hay dentro es el tuyo?","¿Qué resultado concreto cuenta como éxito y quién responde por él?","¿El modelo hace una llamada, sigue pasos fijos o decide su propio recorrido?","¿Usa datos externos o sensibles y puede escribir en sistemas reales?","¿Cuánto cuesta hoy probar un cambio en dinero, minutos y revisión humana?","¿Cuál es el horizonte previsto y quién puede autorizar cambios?"]
    return {"hechos":facts,"inferencias":[],"desconocidos":unknown,"preguntas_pendientes":questions}


def diagnostic_skeleton(repo: Path) -> dict:
    obs=observe(repo); code=next((x["valor"] for x in obs["hechos"] if x["campo"]=="ejes.forma_codigo"),"desconocido")
    return {"schema_version":"1.0.0","proyecto":{"nombre":repo.name,"proposito":None,"usuarios":[],"propietario":None,"criterio_exito":None},"ejes":{"forma_codigo":code,"patron_ejecucion":"desconocido","ritmo":"desconocido","madurez":"desconocido","fuente_entrada":"desconocido","datos_sensibles":None,"herramientas_lectura":None,"herramientas_escritura":None,"reversibilidad":"desconocido","coste_prueba":{"economico":None,"minutos":None,"revision_humana":None},"capacidad_decision":"desconocido","horizonte_vida":"desconocido"},"observacion":obs}
