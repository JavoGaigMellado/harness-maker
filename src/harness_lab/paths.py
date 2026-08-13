from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANATOMY_PATH = ROOT / "datos" / "anatomia.json"
ANATOMY_JS_PATH = ROOT / "datos" / "anatomia.js"
SCHEMA_DIR = ROOT / "schema"
PROMPTS_DIR = ROOT / "taller" / "prompts"
CLAUDE_SKILLS_DIR = ROOT / ".claude" / "skills"
EXAMPLE_DIR = ROOT / "taller" / "ejemplo"
EXAMPLE_STATE_PATH = EXAMPLE_DIR / "estado.json"
EXAMPLE_STATE_JS_PATH = EXAMPLE_DIR / "estado.js"
# El ejemplo también lleva su cobertura desde el 2026-08-12. Sin ella, sus dieciséis piezas
# verificadas dejaban de contar como listas en cuanto el diagrama empezó a exigir criterios
# evaluados, y el recorrido modelo —lo que abre quien acaba de llegar— salía en 0 de 18.
EXAMPLE_COVERAGE_PATH = EXAMPLE_DIR / "cobertura.json"
EXAMPLE_COVERAGE_JS_PATH = EXAMPLE_DIR / "cobertura.js"
HARNESS_LAB_DIR = ROOT / "proyectos" / "harness-lab"
HARNESS_LAB_STATE_PATH = HARNESS_LAB_DIR / "estado.json"
HARNESS_LAB_STATE_JS_PATH = HARNESS_LAB_DIR / "estado.js"
HARNESS_LAB_COVERAGE_PATH = HARNESS_LAB_DIR / "cobertura.json"
HARNESS_LAB_COVERAGE_JS_PATH = HARNESS_LAB_DIR / "cobertura.js"
# El recorrido de cada persona. No está en el repositorio de la plantilla: aparece
# cuando alguien lo crea, y desde entonces su mapa se abre con doble clic igual que el nuestro.
MI_HARNESS_DIR = ROOT / "mi-harness"
MI_HARNESS_STATE_PATH = MI_HARNESS_DIR / "estado.json"
MI_HARNESS_STATE_JS_PATH = MI_HARNESS_DIR / "estado.js"
MI_HARNESS_COVERAGE_PATH = MI_HARNESS_DIR / "cobertura.json"
MI_HARNESS_COVERAGE_JS_PATH = MI_HARNESS_DIR / "cobertura.js"
# Declara cuál de los recorridos posibles es el activo. Sin este puntero una actividad
# no adivina destino: se detiene y pide `harness-lab init`. Así un clon nunca escribe
# en el recorrido de otro proyecto por ser el único que encontró.
POINTER_PATH = ROOT / ".harness-maker.json"
