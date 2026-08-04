from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .arranque import start
from .diagnose import diagnostic_skeleton
from .generate import generate, load_anatomy
from .migrate import migrate_state, needs_migration, parse_renames, plan_migration
from .paths import MI_HARNESS_DIR, POINTER_PATH, ROOT
from .planner import initial_state, replan
from .recover import recover_from_markdown
from .workspace import archive_state, enable_git_hooks, init_workspace, resolve_state_path
from .validate import ValidationFailure, load_json, raise_if, validate_anatomy, validate_diagnostic, validate_generated, validate_state


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")


def parser() -> argparse.ArgumentParser:
    p=argparse.ArgumentParser(prog="harness-lab",description="CLI única del taller")
    sub=p.add_subparsers(dest="cmd",required=True)
    ini=sub.add_parser("init",help="crea tu recorrido y lo declara activo"); ini.add_argument("--repo",type=Path,default=Path.cwd()); ini.add_argument("--workspace",type=Path,default=MI_HARNESS_DIR); ini.add_argument("--reiniciar",action="store_true",help="empieza de cero apartando el recorrido anterior con su fecha")
    sub.add_parser("generate",help="regenera wrapper, índice y prompts")
    v=sub.add_parser("validate",help="valida contratos, referencias, rutas y sincronía")
    v.add_argument("--anatomy",action="store_true"); v.add_argument("--diagnostic",type=Path); v.add_argument("--state",type=Path); v.add_argument("--generated",action="store_true"); v.add_argument("--all",action="store_true")
    d=sub.add_parser("diagnose",help="observa un repo y crea diagnóstico por completar"); d.add_argument("--repo",type=Path,default=Path.cwd()); d.add_argument("--output",type=Path,required=True)
    plan=sub.add_parser("plan",help="calcula o replantea una ruta auditable"); plan.add_argument("--diagnostic",type=Path); plan.add_argument("--state",type=Path); plan.add_argument("--manual",action="append",default=[]); plan.add_argument("--output",type=Path,required=True)
    rec=sub.add_parser("recover",help="recupera estado de Markdown acumulativo"); rec.add_argument("--state",type=Path,required=True); rec.add_argument("--pieces",type=Path,required=True); rec.add_argument("--output",type=Path,required=True)
    mig=sub.add_parser("migrate",help="lleva un recorrido a la anatomía vigente sin perder trabajo"); mig.add_argument("--state",type=Path,required=True); mig.add_argument("--output",type=Path,help="escribe la copia migrada aquí y deja el original donde está"); mig.add_argument("--aplicar",action="store_true",help="deja el recorrido migrado en su sitio y aparta el anterior con su fecha; no borra nada"); mig.add_argument("--renombrar",action="append",default=[],metavar="VIEJO=NUEVO",help="declara que una pieza cambió de nombre; sin esto, la vieja se trata como retirada"); mig.add_argument("--solo-comprobar",action="store_true",help="dice qué cambiaría y no escribe nada")
    st=sub.add_parser("start",help="deja la copia lista, informa del estado y abre el mapa"); st.add_argument("--sin-navegador",action="store_true",help="no abre el mapa"); st.add_argument("--solo-comprobar",action="store_true",help="no reactiva el puntero ni activa el guardián"); st.add_argument("--recorrido-nuevo",action="store_true",help="estrena un recorrido vacío en mi-harness/ aunque el repositorio traiga uno propio; es lo que necesita un caso del banco"); st.add_argument("--repo",type=Path,help="el proyecto que se va a diagnosticar, si no es este repositorio"); st.add_argument("--adoptar",action="store_true",help="adopta el recorrido de Harness-Maker en vez de estrenar el tuyo; solo existe en la copia de desarrollo")
    return p


def main(argv: list[str] | None=None) -> None:
    args=parser().parse_args(argv)
    try:
        if args.cmd=="init":
            existing_diagnostic=(args.workspace / "diagnostico.json").exists()
            written=init_workspace(ROOT,POINTER_PATH,args.workspace,args.repo,restart=args.reiniciar)
            if enable_git_hooks(ROOT): print("Activado el guardián de generados (core.hooksPath = .githooks)")
            diagnostic=(args.workspace / "diagnostico.json").resolve()
            for path in written:
                if path==args.workspace / "diagnostico.json" and existing_diagnostic:
                    verb="Adoptado"
                else:
                    verb="Apartado" if path.name.startswith(f"{args.workspace.name}-anterior-") else "Escrito"
                print(f"{verb} {path.resolve().relative_to(ROOT.resolve())}")
            if existing_diagnostic:
                print(f"Recorrido existente reactivado desde {diagnostic.relative_to(ROOT.resolve())}")
            else:
                print(f"Siguiente paso: completa los desconocidos de {diagnostic.relative_to(ROOT.resolve())} con /diagnostico")
        elif args.cmd=="generate":
            paths=generate(); print(f"Generados {len(paths)} archivos desde datos/anatomia.json")
        elif args.cmd=="diagnose":
            write_json(args.output,diagnostic_skeleton(args.repo.resolve())); print(f"Diagnóstico observable escrito en {args.output}; completa los desconocidos")
        elif args.cmd=="plan":
            anatomy=load_anatomy()
            if args.state:
                data=replan(anatomy,load_json(args.state),args.manual)
            elif args.diagnostic:
                diag=load_json(args.diagnostic); raise_if(validate_diagnostic(diag)); data=initial_state(anatomy,diag,args.manual)
            else: raise ValidationFailure("plan requiere --diagnostic o --state")
            raise_if(validate_state(data,anatomy)); write_json(args.output,data); print(f"Ruta escrita en {args.output}")
            # El estado tiene envoltorio generado y `plan` no lo escribía. Entre calcular la
            # ruta y el siguiente arranque, `validate --all` quedaba en rojo por un derivado
            # ausente que nadie había pedido a mano, justo en la secuencia que documenta el
            # README. Se regenera aquí, donde cambia la fuente, en vez de confiar en que la
            # persona adivine que le toca `generate`.
            print(f"Regenerados {len(generate())} derivados: la vista y `validate --all` cuadran ya")
        elif args.cmd=="migrate":
            if not args.solo_comprobar and bool(args.output)==bool(args.aplicar):
                raise ValidationFailure("elige una salida: `--output <ruta>` para dejar una copia, o `--aplicar` para dejarlo en su sitio apartando el anterior con su fecha.")
            # No se migra en sitio: perder el estado de origen deja a la persona sin
            # vuelta atrás justo cuando más la necesita. `--aplicar` no es una excepción,
            # porque aparta el original con fecha antes de escribir, igual que hace
            # `init --reiniciar` con un recorrido entero.
            if args.output and args.output.resolve()==args.state.resolve():
                raise ValidationFailure("--output no puede ser el mismo archivo que --state: la migración escribe una copia nueva a propósito. Si quieres dejarlo en su sitio, usa `--aplicar`.")
            anatomy=load_anatomy(); state=load_json(args.state)
            try: renames=parse_renames(args.renombrar)
            except ValueError as exc: raise ValidationFailure(str(exc)) from exc
            plan=plan_migration(anatomy,state,renames)
            if args.solo_comprobar:
                if not needs_migration(plan): print(f"Nada que migrar: el recorrido ya está en la anatomía {plan['a']}.")
                else:
                    print(f"Migraría de {plan['de']} a {plan['a']}.")
                    for titulo,valor in (("renombradas",plan["renombradas"]),("retiradas",plan["retiradas"]),("nuevas",plan["nuevas"])):
                        if valor: print(f"  {titulo}: {valor}")
                raise SystemExit(0)
            migrated,notes=migrate_state(anatomy,state,renames)
            # Se valida antes de escribir: una migración que produce un estado inválido no
            # debe llegar al disco, y menos aún sustituir al que funcionaba.
            raise_if(validate_state(migrated,anatomy))
            print("\n".join(notes))
            if args.aplicar:
                apartado=archive_state(args.state)
                write_json(args.state,migrated); generate()
                print(f"Recorrido anterior apartado en {apartado}; el migrado queda en {args.state}")
            else:
                write_json(args.output,migrated)
                print(f"Recorrido migrado escrito en {args.output}; el original sigue intacto en {args.state}")
                print(f"Para dejarlo en su sitio sin mover archivos a mano: harness-lab migrate --state {args.state} --aplicar")
        elif args.cmd=="recover":
            data,notes=recover_from_markdown(load_json(args.state),args.pieces); write_json(args.output,data); print("\n".join(notes))
        elif args.cmd=="start":
            raise SystemExit(start(abrir=not args.sin_navegador,reparar=not args.solo_comprobar,recorrido_nuevo=args.recorrido_nuevo,repo=args.repo,adoptar=args.adoptar))
        elif args.cmd=="validate":
            errors=[]; selected=args.all or not any([args.anatomy,args.diagnostic,args.state,args.generated])
            if selected or args.anatomy: errors+=validate_anatomy()
            if selected or args.generated: errors+=validate_generated()
            if args.diagnostic: errors+=validate_diagnostic(load_json(args.diagnostic))
            if args.state: errors+=validate_state(load_json(args.state))
            # `--all` incluye el recorrido activo. Antes solo cubría anatomía y generados,
            # así que prometía más de lo que comprobaba: un estado o un diagnóstico
            # inválidos pasaban el control mientras nadie los nombrara con su ruta.
            if selected and POINTER_PATH.exists():
                declared=json.loads(POINTER_PATH.read_text(encoding="utf-8"))
                state_path=resolve_state_path(ROOT,POINTER_PATH)
                if not args.state and state_path.exists(): errors+=validate_state(load_json(state_path))
                diagnostic_path=(ROOT / declared["diagnostico"]).resolve() if declared.get("diagnostico") else None
                if not args.diagnostic and diagnostic_path and diagnostic_path.exists():
                    errors+=validate_diagnostic(load_json(diagnostic_path))
            raise_if(errors); print("Validación correcta")
    except ValidationFailure as exc:
        print(f"ERROR de validación:\n{exc}",file=sys.stderr); raise SystemExit(1)


if __name__=="__main__": main()
