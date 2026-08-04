<!-- GENERADO desde datos/anatomia.json por `harness-lab generate`. NO EDITAR A MANO. -->
# Paso 0 · Diagnóstico multidimensional

Eres un asistente de desarrollo portable. Diagnostica ESTE repositorio antes de conversar: revisa
`git status`, README, manifiestos, estructura, llamadas a modelos, herramientas, datos, tests,
despliegue e instrucciones existentes. Registra rutas y comandos como evidencia.

Clasifica por separado hechos observados, inferencias y desconocidos. Pregunta únicamente lo que no
pueda descubrirse y reúne todos esos datos en la misma ejecución, usando tantos bloques como sean
necesarios. No uses un `tipo_proyecto` excluyente.

Ejes obligatorios:

- `forma_codigo`
- `patron_ejecucion`
- `ritmo`
- `madurez`
- `fuente_entrada`
- `datos_sensibles`
- `herramientas_lectura`
- `herramientas_escritura`
- `reversibilidad`
- `coste_prueba`
- `capacidad_decision`
- `horizonte_vida`

Decisiones globales de entrada/salida:

- **proposito_gobierno**: ¿Qué trabajo se delega, para quién, quién responde y qué resultado cuenta como éxito?
- **datos_privacidad**: ¿Qué datos se usan, con qué finalidad, acceso, retención, borrado y residencia?
- **intervencion_humana**: ¿Cuándo se detiene, escala o pide autorización y quién puede aprobar?
- **estado_recuperacion**: ¿Cómo se evitan duplicados y se reanuda tras un fallo?
- **operacion_feedback**: ¿Cómo se despliega, observa, revierte, atiende un incidente y aprende del uso real?
- **seguridad_supply_chain**: ¿Qué identidades, permisos, dependencias y fronteras limitan el impacto?
- **ciclo_vida**: ¿Se promueve, congela, retira o acepta como deuda, quién decide y cuándo?

Obtén consentimiento explícito para reutilización anonimizada; el valor por defecto es `false` y no
condiciona el uso local. Escribe `mi-harness/diagnostico.json`, valida con
`harness-lab validate --diagnostic mi-harness/diagnostico.json`, genera la ruta con
`harness-lab plan --diagnostic mi-harness/diagnostico.json --output mi-harness/estado.json` y valida
el estado. Cada prioridad debe citar una regla declarada; las 18 piezas deben aparecer, incluso si
la acción recomendada es descartarlas con motivo.
