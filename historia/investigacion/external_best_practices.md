# Estado del arte en arquitecturas de agentes/LLM (2024-2026)

> Investigación externa para el proyecto `harness-lab`. Objetivo: informar el refinamiento del schema de perfilado de proyectos de IA con hallazgos concretos de la industria, no con "buenas prácticas" genéricas.
>
> Fecha de la investigación: 2026-07-31.

---

## 1. Arquitecturas de agentes/LLM: patrones y taxonomías

### La distinción fundacional: Workflows vs. Agents (Anthropic)

El documento de referencia más citado en la industria es ["Building Effective Agents" de Anthropic](https://www.anthropic.com/research/building-effective-agents) (19 dic 2024). Establece una distinción que casi toda la literatura posterior reutiliza:

- **Workflows**: sistemas donde LLMs y herramientas se orquestan mediante **caminos de código predefinidos**. El desarrollador posee el control de flujo completo. Son predecibles, testeables y más baratos.
- **Agents**: sistemas donde el LLM **dirige dinámicamente su propio proceso** y uso de herramientas, decidiendo en tiempo real qué hacer a continuación en función del feedback del entorno. El desarrollador posee el objetivo y los guardrails, no cada rama de decisión.

Recomendación explícita de Anthropic: *"find the simplest solution possible, and only increase complexity when needed"*. Empezar con una llamada simple optimizada; subir a workflow si el problema se puede descomponer en pasos fijos; subir a agente autónomo solo si la tarea es abierta y el conteo de pasos es impredecible.

**Los 6 patrones de workflow** que describe (base de facto de toda taxonomía posterior — LangGraph, CrewAI, guías de OpenAI la citan o replican):

1. **Prompt chaining**: pasos secuenciales con checkpoints programáticos entre ellos. Uso: tarea descomponible en subtareas fijas donde cambiar latencia por precisión merece la pena.
2. **Routing**: clasifica el input y lo dirige a un proceso especializado. Uso: categorías de tarea claramente distintas (p. ej. enrutar a modelos de distinto tamaño/coste según complejidad).
3. **Parallelization** (sectioning y voting): ejecuta múltiples llamadas LLM en paralelo y agrega resultados. Uso: acelerar trabajo divisible, o aumentar confianza con múltiples perspectivas (p. ej. varios revisores de vulnerabilidades de código).
4. **Orchestrator-workers**: un LLM central descompone la tarea dinámicamente, delega a LLMs trabajadores y sintetiza resultados. Uso: cuando las subtareas no se pueden predefinir (p. ej. modificar múltiples archivos de código).
5. **Evaluator-optimizer**: un LLM genera, otro evalúa y da feedback en bucle iterativo. Uso: existen criterios de evaluación claros y la iteración mejora demostrablemente el resultado.
6. **Autonomous agents**: el LLM opera con independencia usando herramientas basándose en feedback del entorno, potencialmente muchas iteraciones, con checkpoints humanos opcionales. Uso: problemas abiertos, número de pasos impredecible, cuando ya se confía suficientemente en el modelo.

Principios transversales de diseño: **simplicidad**, **transparencia** (mostrar explícitamente el razonamiento/planificación del agente), e inversión fuerte en el **"Agent-Computer Interface" (ACI)** — documentar y testear las herramientas tan cuidadosamente como una API para humanos.

Fuente: [Building Effective Agents — Anthropic](https://www.anthropic.com/research/building-effective-agents)

### La guía de OpenAI

["A Practical Guide to Building Agents"](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) de OpenAI (guía de 34 páginas basada en despliegues reales con clientes) cubre una progresión similar: qué es un agente, cuándo construir uno, componentes de diseño fundacionales, patrones de orquestación (single-agent vs. multi-agent) y **guardrails** como componente de primera clase del diseño — no como añadido posterior.

### 12-Factor Agents (HumanLayer)

[12-factor-agents](https://github.com/humanlayer/12-factor-agents) es un conjunto de principios de ingeniería (inspirado en 12-factor apps) que va más allá de la taxonomía de patrones y ataca el "cómo construir software confiable" con LLMs. Los 12 factores, resumidos:

1. Natural Language to Tool Calls — convertir intención en llamadas a función estructuradas.
2. Own your prompts — no delegar el prompt engineering a los defaults de un framework.
3. **Own your context window** — gestionar activamente qué entra en el contexto.
4. Tools are just structured outputs — los tools son schemas de datos, no constructos mágicos de framework.
5. Unify execution state and business state — el estado del flujo del agente debe sincronizarse con el modelo de datos real de la app.
6. Launch/Pause/Resume con APIs simples.
7. **Contact humans with tool calls** — escalar a humanos usando el mismo mecanismo que para integraciones de sistema (human-in-the-loop como tool call, no como excepción).
8. **Own your control flow** — escribir lógica explícita del loop del agente en vez de aceptar el control flow opaco de un framework.
9. Compact errors into context window — los errores deben caber y ser útiles dentro del límite de tokens.
10. **Small, focused agents** — agentes especializados en problemas concretos, no generalistas todopoderosos.
11. Trigger from anywhere.
12. Make your agent a stateless reducer — función pura que transforma estado de entrada en estado de salida.

Un dato relevante que da este proyecto: **hay pocos frameworks reales detrás de agentes de producción de cara al cliente** — la mayoría del código real es "mostly just software" con LLMs invocados en puntos concretos, no un framework agentic genérico.

### Frameworks de orquestación multi-agente: mapa de 2025-2026

- **LangGraph**: runtime de orquestación de bajo nivel — el desarrollador posee el loop, el schema de estado y cada arista del grafo (modelo de grafo dirigido: nodos = funciones, edges = flujo, estado tipado y persistido). Funciona con cualquier proveedor de modelo.
- **Claude Agent SDK**: harness "opinionado, todo incluido" donde Anthropic posee el agent loop; el patrón multi-agente es de **subagentes definidos programáticamente** con un Claude orquestador que delega y sintetiza (orchestrator-worker limpio y trazable, pero más constreñido).
- **CrewAI**: orquestación basada en roles ("equipo" de agentes con roles/tareas); ~1.3M instalaciones PyPI/mes, adopción de producción alta, 30-60% más rápido que AutoGen en tareas simples.
- **AutoGen / AG2**: interacción conversacional abierta entre agentes (debate/negociación). Microsoft puso AutoGen en modo mantenimiento a fines de 2025; la comunidad original hizo fork como **AG2** con arquitectura event-driven async. Mejor en escenarios de negociación multi-turno complejos.
- Patrón híbrido recomendado en 2026: LangGraph para orquestación de alto nivel + Claude Agent SDK (u otro SDK opinionado) para agentes especializados que tocan filesystem/terminal.

Fuentes: [Claude Agent SDK vs LangGraph — Developers Digest](https://www.developersdigest.tech/blog/claude-agent-sdk-vs-langgraph), [AG2 vs CrewAI comparison](https://dev.to/agentsindex/ag2-vs-crewai-the-complete-comparison-including-the-autogen-rebrand-explained-248l), [best AI agent frameworks 2026 — LangChain](https://www.langchain.com/resources/ai-agent-frameworks)

### Un dato de madurez a matizar

A pesar de la proliferación de frameworks, un hallazgo consistente en 2026 es que **la mayoría de las empresas usan loops escritos a mano o wrappers finos, no frameworks completos** — es decir, los frameworks son herramientas, no un estándar de facto ("table stakes"). El único elemento que sí se está consolidando como estándar de interoperabilidad es **MCP (Model Context Protocol)** de Anthropic, descrito como "USB-C para agentes de IA".

---

## 2. Gestión de contexto y memoria

### Context engineering ≠ prompt engineering

Anthropic formalizó esta distinción en su post de ingeniería ["Effective context engineering for AI agents"](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) (29 sept 2025):

> Prompt engineering es discreto (escribir un buen prompt para una tarea puntual). Context engineering es **iterativo y dinámico** — ocurre cada vez que decidimos qué pasar al modelo en cada paso de un loop agentic.

Principio central: encontrar **"el conjunto más pequeño posible de tokens de alta señal que maximice la probabilidad del resultado deseado"** — el contexto es un recurso finito y "precioso", no un cubo donde volcar todo lo que pueda ser relevante.

### Context rot: la razón técnica de por qué "más contexto" no es gratis

Un estudio de 2025 de Chroma probó 18 modelos frontera (GPT-4.1, Claude Opus 4, Gemini 2.5, etc.) y encontró que **todos degradan su desempeño a medida que crece el input**, incluso muy por debajo del límite documentado de su ventana de contexto — caídas de precisión de 30-50% ya en 50K tokens en modelos con ventana de 200K. Causas identificadas: efecto "lost-in-the-middle" (atención pobre a la parte media del contexto), dilución de atención (la atención transformer es cuadrática: 100K tokens = ~10.000 millones de relaciones par-a-par) e interferencia de distractores.

**Implicación práctica directa para el schema**: "context management" no debería ser un campo de texto libre vago; el estado del arte identifica **4 estrategias concretas** que conviene poder categorizar:
- **Write** (escribir a memoria persistente fuera de la ventana — notas estructuradas)
- **Select** (recuperar en el momento justo — "just-in-time", identificadores ligeros como paths/queries en vez de volcar todo el contenido de antemano)
- **Compress** (compactación/resumen del historial preservando decisiones arquitectónicas y bugs no resueltos, descartando outputs de tools redundantes)
- **Isolate** (sub-agentes con ventanas de contexto limpias que devuelven resúmenes condensados de 1000-2000 tokens al coordinador)

Fuentes: [Effective context engineering for AI agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [Chroma: Context Rot study — ZenML LLMOps DB](https://www.zenml.io/llmops-database/context-rot-evaluating-llm-performance-degradation-with-increasing-input-tokens)

### Memoria corto/largo plazo

El patrón "de facto" dominante en producción (coding assistants, bots de servicio al cliente, copilots empresariales) es un **híbrido**:
- **Memoria de trabajo** = lo que vive en la ventana de contexto (configuración, eventos recientes).
- **Memoria de largo plazo** = almacén externo (vector store para similitud semántica, o almacén estructurado — tuplas/BD/knowledge graph — para hechos exactos y consultas de rango), con un pipeline de recuperación que inyecta registros relevantes en cada paso.

La elección vector vs. estructurado no es binaria: vectorización para "conceptos similares", extracción a formato estructurado para hechos/entidades/preferencias que necesitan exact-match. La mayoría de agentes de producción **combinan ambas**.

Fuentes: [Long-Term Memory Architectures for AI Agents — Redis](https://redis.io/blog/long-term-memory-architectures-ai-agents/), [Long-Term Memory for AI Agents — mem0.ai](https://mem0.ai/blog/long-term-memory-ai-agents)

### RAG vs. fine-tuning vs. prompt caching: marco de decisión

Consenso emergente en guías de 2025-2026:
- **Prompt caching + full-context**: para bases de conocimiento <200K tokens, suele ser más rápido y barato que montar infraestructura RAG. Con ventanas de hasta 1M-2M tokens (Claude, Gemini), cubre muchos casos de documentación interna/catálogos.
- **RAG**: único camino escalable cuando el conocimiento cambia con el tiempo, o cuando se necesita citar fuentes/mostrar procedencia para auditoría (un modelo fine-tuneado no puede "apuntar" al documento que justificó una respuesta).
- **Fine-tuning**: se justifica para formato de salida consistente que el prompting no logra imponer, razonamiento de dominio específico, calibración de tono/estilo, u optimización de coste (modelo pequeño fine-tuneado superando a uno grande genérico en una tarea concreta). Solo ~43% de organizaciones encuestadas por LangChain (2025) hacen fine-tuning activo; el 57% restante usa modelos base con prompt engineering + RAG.
- Progresión recomendada: empezar con prompt engineering (horas/días) → escalar a RAG cuando se necesitan datos en tiempo real → fine-tuning solo cuando se necesita especialización profunda (meses de trabajo + hasta 6x coste de inferencia).

Fuente: [RAG vs Fine-Tuning vs Prompt Engineering — thedatascientist.com](https://thedatascientist.com/fine-tuning-rag-or-prompt-engineering/), [State of AI Agents 2025 — LangChain](https://www.langchain.com/state-of-agent-engineering)

---

## 3. Estrategia de prompts: versionado, testing, prompt-as-code

Hallazgo central: **la mayoría de las empresas no tiene ningún proceso de gestión de cambios de prompts**. Cita textual de una de las fuentes: *"most companies lack processes for prompt change management, testing, and deployment—there is no CI/CD for prompts, no evaluation before release, no observability after."*

Distinción que se está consolidando en 2025-2026:
- **Prompt engineering** = escribir el prompt (arte/oficio, foco en precisión y tono).
- **Prompt management** = tratar los prompts como artefactos versionados con almacenamiento, testing, evaluación y despliegue a escala — *"prompt management es a los sistemas LLM lo que el control de versiones es a la ingeniería de software"*.

Diferencia clave frente al versionado de código tradicional: los prompts **no son deterministas** — no puedes correr un test unitario clásico y confiar en que el output será idéntico cada vez. Esto empuja a prácticas específicas:
- **Despliegue por etapas** (dev → staging → producción) con testing de cambios antes de promoción, y rollback a la última versión conocida como buena.
- Equipos con gestión de prompts sistemática reportan **40-60% de ciclos de iteración más rápidos** y menos incidentes de producción frente a enfoques ad hoc (cifra de proveedor, tomar con cautela pero direccionalmente consistente con lo demás).
- Herramientas emergentes de esta categoría: Langfuse, Braintrust, Agenta, LaunchDarkly (prompt flags), Arize, Maxim — todas ofrecen versionado + eval + observability como paquete integrado, señal de que el mercado ve estas tres cosas como inseparables.

Fuentes: [Prompt Versioning & Management Guide — LaunchDarkly](https://launchdarkly.com/blog/prompt-versioning-and-management/), [Prompt Versioning: The Complete Guide — Agenta](https://agenta.ai/blog/prompt-versioning-guide), [Top 5 AI Prompt Management Tools 2026 — Arize](https://arize.com/blog/top-5-ai-prompt-management-tools-for-2026/)

---

## 4. Orquestación de flujos multi-paso/multi-agente

(Complementa la sección 1). Los frameworks convergen en un puñado de **patrones de control** reutilizables:

- **State machines / grafos con estado tipado** (LangGraph): necesarios cuando el agente corre horas, se pausa para aprobación humana, o debe reanudar desde un paso intermedio tras un despliegue.
- **Patrón supervisor**: un agente orquestador enruta a sub-agentes especialistas — más estructurado que tool-calling simple.
- **Orchestrator-worker** (Claude Agent SDK, patrón 4 de Anthropic): el orquestador delega y sintetiza, limpio y trazable pero más constreñido que un grafo libre.
- **DAGs / prompt chaining**: para pipelines deterministas de varios pasos donde no hace falta que el modelo decida el flujo.

Punto de fricción real reportado: **"unify execution state and business state"** (factor 5 de 12-factor-agents) — muchos proyectos fallan porque el estado del agente vive separado del modelo de datos real de la aplicación, generando inconsistencias difíciles de depurar.

---

## 5. Evaluación y testing de sistemas LLM

### ¿Qué tan extendida está la evaluación seria? (dato duro)

Del **LangChain "State of AI Agents" 2025** (1,340 respuestas, encuesta del 18 nov – 2 dic 2025):

- **57.3%** de encuestados tienen agentes corriendo en producción (vs. 51% en 2024); otro 30.4% los está desarrollando activamente.
- **Calidad** es el principal bloqueador de producción — citado por **32-33%**, más del doble que el siguiente factor (coste/seguridad). Cita: *"Quality is the production killer"*.
- **Observabilidad**: 89% ha implementado alguna forma; entre los que ya tienen agentes en producción, 94% tiene observabilidad y 71.5% tiene tracing completo (i.e., el ~6-29% restante, incluso en producción, opera con visibilidad parcial o nula).
- **Evaluación offline** (test-sets): 52.4% la usa. **Evaluación online** (monitoreo continuo en producción): solo 37.3%.
- **Método de evaluación**: 59.8% usa revisión humana; 53.3% usa LLM-as-judge (los porcentajes se solapan — muchos usan ambos).
- Control de permisos: la mayoría restringe a acceso de solo lectura o exige aprobación humana para escritura/borrado — pero esto no es universal.

Lectura honesta: **incluso entre equipos que ya llegaron a producción, una fracción no trivial (~30-40%) no tiene evaluación online ni tracing completo**. La eval "seria" (con datasets, LLM-as-judge calibrado, sampling continuo) es más la excepción que la norma incluso en 2025-2026, aunque la tendencia es claramente ascendente año a año.

Fuentes: [State of AI Agents — LangChain](https://www.langchain.com/state-of-agent-engineering), [LangChain State of AI Agents 2024](https://www.langchain.com/stateofaiagents)

### LLM-as-judge: cómo se hace bien

- No basta con "adivinar" un prompt de evaluador: **la confiabilidad depende de una alineación sistemática con juicio humano** (ciclo: recolectar correcciones humanas → construir few-shot examples → medir el nivel de acuerdo humano-juez a lo largo del tiempo — p.ej. LangSmith "Align Evals").
- Práctica estándar: **no evaluar cada request** — usar sampling sobre trazas para detectar drift/degradación como sistema de alerta temprana, no medición exhaustiva.
- Human-in-the-loop se integra como "annotation queues": trazas de baja confianza se enrutan a revisores humanos, y ese feedback retroalimenta el dataset de evaluación (flywheel de mejora continua).

### La crítica de Hamel Husain: "eval-driven development" no es la respuesta ingenua

Voz influyente en la práctica de evals (Hamel Husain, con Shreya Shankar): escribir evaluadores *antes* de construir features (por analogía con TDD) **crea más problemas de los que resuelve**, porque a diferencia del software tradicional, los LLMs tienen una "superficie de fallo infinita" — no se puede anticipar qué va a fallar. Recomendación concreta: empezar con **análisis de errores reales** (leer transcripciones/logs) y escribir evaluadores para los errores *descubiertos*, no para los *imaginados*. Empresas citadas (p. ej. Rechat) mantienen **cientos de tests unitarios actualizados continuamente** a partir de fallos observados en datos reales — el eval set es un organismo vivo, no un documento de requisitos fijado al inicio.

Fuentes: [Your AI Product Needs Evals — Hamel Husain](https://hamel.dev/blog/posts/evals/), [Should I practice eval-driven development? — Hamel Husain](https://hamel.dev/blog/posts/evals-faq/should-i-practice-eval-driven-development.html)

---

## 6. Fallos comunes / antipatrones en producción

### Taxonomía de fallos 2026

Reportes de campo (Arize, Trantor, Enlight Lab) convergen en una lista recurrente de causas de fallo en agentes de producción:
1. **Errores en cascada** a través de planes multi-paso.
2. **Mal uso de herramientas** (tool misuse / argumentos incorrectos) — señalado como **la causa proximal más común, ~31% de los fallos de producción en 2024-2025**.
3. **Prompt injection** (directa e indirecta).
4. **Degradación por ventana de contexto** ("context rot", ver sección 2).
5. Fallos de planificación.
6. **Alucinación de "grounding"** (afirmar que algo viene de una fuente cuando no es así).
7. Huecos de observabilidad.
8. Despliegues "ciegos al contexto" (no adaptados al entorno real de uso).
9. Guardrails ausentes.
10. **"Set-and-forget" drift** — el agente se despliega y nunca se re-audita a medida que cambian datos/modelo/entorno.

### Hallazgos de seguridad concretos (no genéricos)

- **OWASP Top 10 for LLM Applications (2025)**: *prompt injection* ocupa el primer puesto **por segunda edición consecutiva**. "Excessive Agency" es una de las categorías más ampliadas en la edición 2025 — dar a un agente más herramientas o permisos de los que su tarea requiere, o permitirle actuar sin aprobación humana, crea una superficie de ataque explotable.
- **OWASP Top 10 for Agentic Applications (ASI, diciembre 2025)** — primer framework revisado por pares específico para seguridad de agentes autónomos, con más de 100 expertos y respaldo de NIST/Microsoft/NVIDIA. Categorías: Agent Goal Hijack, Tool Misuse & Exploitation, Agent Identity & Privilege Abuse, Agentic Supply Chain Compromise, Unexpected Code Execution, **Memory & Context Poisoning**, Insecure Inter-Agent Communication, Cascading Agent Failures, Human-Agent Trust Exploitation, Rogue Agents.
- **Dato cuantitativo de tendencia de ataque**: intentos documentados de prompt injection contra sistemas empresariales de IA **aumentaron 340% interanual a fines de 2025**; los ataques **indirectos** ya representan >55% de los incidentes observados y logran tasas de éxito 20-30% más altas que los directos.
- **Incidentes reales documentados**:
  - *Slack AI* (PromptArmor, 2024): instrucción maliciosa en un canal público o documento subido permitía exfiltrar datos de canales privados (incluyendo API keys).
  - *EchoLeak* (Aim Labs, 2025): primer ataque de exfiltración de datos **zero-click** contra Microsoft 365 Copilot — un email nunca abierto por el usuario, procesado en segundo plano por Copilot, filtraba datos ante una consulta posterior no relacionada.
  - Múltiples incidentes de fuga de datos jul-ago 2025 vía prompt injection (chats de usuario, credenciales, datos de apps de terceros).

Marco de mitigación citado: **guardrails pre-LLM** (PII, datos sensibles, detección de inyección) vs. **guardrails post-LLM** (calidad de output, alucinaciones, validación de acciones antes de ejecutarlas).

Fuentes: [OWASP Top 10 for LLM Applications 2025 — Mend.io](https://www.mend.io/blog/2025-owasp-top-10-for-llm-applications-a-quick-guide/), [OWASP Top 10 for Agentic Applications — OWASP GenAI Security](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/), [Why AI Agents Break — Arize](https://arize.com/blog/common-ai-agent-failures/), [awesome-ai-agent-attacks — GitHub](https://github.com/webpro255/awesome-ai-agent-attacks)

---

## 7. Magnitud del problema: ¿qué tan maduro está esto en 2025-2026?

Conclusión honesta tras revisar múltiples fuentes: **no es "wild west" total, pero tampoco hay consenso maduro** — es una madurez desigual, con islas de estandarización dentro de un océano todavía cambiante.

### Señales de inmadurez / "sigue siendo salvaje"

- **MIT, "State of AI in Business" (2025)**: basado en 150 entrevistas + encuesta a 350 empleados + análisis de 300 despliegues públicos — **el 95% de los pilotos de GenAI empresariales fallan en escalar a producción o generar resultados medibles**. El diagnóstico del propio MIT: el problema no es la calidad de los modelos sino un **"learning gap"** de integración organizacional — no un problema de tecnología, sino de proceso.
- **Gartner (jun 2025)**, sobre una encuesta a más de 3,400 organizaciones: predice que **más del 40% de los proyectos de IA agentic serán cancelados antes de fines de 2027**, por costes escalantes, valor de negocio poco claro o controles de riesgo inadecuados. Cita textual de un analista Gartner: *"most agentic AI projects right now are early stage experiments or proof of concepts that are mostly driven by hype and are often misapplied"*.
- **"Agent washing"**: término ya acuñado por analistas para describir el re-etiquetado de chatbots/RPA existentes como "agentes", sin cambio arquitectónico real — señal de que el término "agente" está sobreusado en marketing más de lo que refleja arquitecturas reales.
- Gestión de prompts: la mayoría de empresas **no tiene CI/CD para prompts** ni evaluación pre-release (sección 3).
- Frameworks: la mayoría usa **loops escritos a mano**, no frameworks maduros — el ecosistema de herramientas cambia mes a mes.

### Señales de madurez creciente / consolidación real

- **MCP (Model Context Protocol)** de Anthropic se ha consolidado como estándar de interoperabilidad de facto ("USB-C para agentes").
- La taxonomía workflows-vs-agents de Anthropic y los 6 patrones se han convertido en vocabulario compartido de la industria (citado/replicado por OpenAI, LangChain, frameworks comerciales).
- Observabilidad: 89-94% de equipos con agentes en producción ya tiene *alguna* observabilidad — la instrumentación básica ya es norma, no excepción, entre quienes llegan a producción (el problema es la profundidad, no la existencia).
- Producción real: 57.3% de encuestados (LangChain 2025) ya tiene agentes en producción, subiendo año a año.
- Seguridad: aparición de un framework revisado por pares (OWASP ASI) con respaldo de NIST/Microsoft/NVIDIA en dic-2025 es una señal fuerte de que la industria está pasando de "nadie habla de esto" a "hay un estándar de referencia".

### Un dato que conecta con la "magnitud" del problema a futuro: METR time horizons

[METR](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) mide la capacidad de agentes de IA en términos de **duración de tarea humana equivalente que el modelo completa con 50% de éxito** ("time horizon"). Hallazgo: este horizonte temporal **se ha duplicado cada ~7 meses durante 6 años** (de segundos en 2019 a >16 horas en 2026), con aceleración reciente a **duplicación cada 4 meses en 2024-2025**. Los modelos actuales tienen ~100% de éxito en tareas de <4 minutos (humano) y caen a <10% de éxito en tareas de >4 horas. Esto es relevante para la "magnitud del problema": **la capacidad técnica está creciendo más rápido que la madurez de ingeniería/evaluación/seguridad que la rodea** — un desfase que explica por qué tantos pilotos fallan a pesar de que el modelo subyacente "sí puede" técnicamente.

**Conclusión para el usuario**: construir con buenas prácticas de contexto, evaluación y guardrails no es prematuro ni excesivo para un "laboratorio personal" — es exactamente el tipo de disciplina que, según estos datos, **separa al ~5-40% que sí llega a producción/escala del resto**.

Fuentes: [MIT report: 95% of GenAI pilots fail — Yahoo Finance / MIT NANDA](https://finance.yahoo.com/news/mit-report-95-generative-ai-105412686.html), [Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027), [METR: Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)

---

## Resumen ejecutivo de hallazgos clave (para referencia rápida)

| Tema | Dato concreto | Fuente |
|---|---|---|
| Adopción en producción | 57.3% de encuestados tienen agentes en producción (2025), sube desde 51% (2024) | LangChain State of AI Agents |
| Principal barrera | Calidad (32-33%), más del doble que coste/seguridad | LangChain State of AI Agents 2025 |
| Observabilidad en producción | 94% tiene algo; solo 71.5% tiene tracing completo | LangChain State of AI Agents 2025 |
| Evaluación online (no solo offline) | Solo 37.3% | LangChain State of AI Agents 2025 |
| Fine-tuning activo | Solo 43%; 57% usa modelo base + prompting/RAG | LangChain State of AI Agents 2025 |
| Fallo de pilotos empresariales | 95% de pilotos GenAI no escalan a producción | MIT State of AI in Business 2025 |
| Cancelación de proyectos agentic | >40% cancelados para fin de 2027 (predicción) | Gartner, jun 2025 |
| Causa proximal más común de fallo | Mal uso de herramientas (~31% de fallos) | Arize / análisis de campo 2024-2025 |
| Crecimiento de prompt injection | +340% interanual (fines 2025); indirecta >55% de incidentes | Reportes de seguridad 2025 |
| Degradación por contexto largo | Caídas de 30-50% de precisión incluso a 50K tokens en ventanas de 200K | Chroma, "Context Rot" 2025 |
| Capacidad técnica (time horizon) | Duplica cada 4-7 meses; de segundos (2019) a >16h (2026) | METR |

---

## Notas metodológicas

Esta investigación se basó en búsquedas web (WebSearch) y lectura directa de páginas fuente (WebFetch) realizadas el 2026-07-31, priorizando: (a) publicaciones primarias de laboratorios (Anthropic, OpenAI), (b) encuestas de industria con metodología declarada (LangChain, Gartner, MIT, PwC, METR), (c) proyectos de referencia open-source (12-factor-agents), y (d) frameworks de seguridad revisados por pares (OWASP). Se evitaron blogs de marketing sin datos propios salvo cuando resumían fielmente una fuente primaria citable. Cifras de proveedores comerciales (p. ej. "40-60% de iteración más rápida" de herramientas de prompt management) se señalan explícitamente como tales — direccionalmente consistentes con el resto de la evidencia, pero no verificadas de forma independiente.
