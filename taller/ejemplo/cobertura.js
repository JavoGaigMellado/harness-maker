/* GENERADO desde taller/ejemplo/cobertura.json por `harness-lab generate`.
 * NO EDITAR A MANO. Permite ver los criterios evaluados del ejemplo sin servidor.
 * sha256 fuente: 94cbae6ec522f02878aa1d303a81c329d67c1d920d207e49ca96b49457188ff7
 */
window.EJEMPLO_COBERTURA = {
  "version": "1.0.0",
  "anatomia_version": "2026.08.02",
  "fecha": "2026-08-12",
  "regla_cierre": "completada exige todos los criterios definidos o no aplicables; en_curso conserva cualquier cobertura parcial o ausente; descartada exige que todos no apliquen y un motivo; deuda_aceptada cierra con algún criterio todavía parcial solo si la deuda tiene responsable y condición de revisión.",
  "procedencia": "Evaluada criterio a criterio el 2026-08-12 contra las decisiones del propio ejemplo, y escrita después de completar las que faltaban: el ejemplo declaraba dieciséis piezas verificadas con treinta y cinco decisiones para noventa y nueve criterios, así que ninguna sostenía su cierre. Cada criterio cita las decisiones que lo cubren. Es material pedagógico: el ayudante de correo es una ficción, y su cobertura también, pero la relación entre criterio y decisión es la que tendría que existir en un recorrido real.",
  "piezas": {
    "contexto": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Separar las cinco capas: persona, organización, proyecto, tarea, sesión.",
          "estado": "definido",
          "evidencias": [
            "contexto-1",
            "harness/contexto.md"
          ]
        },
        {
          "criterio": "Decidir qué se carga siempre y qué solo cuando hace falta.",
          "estado": "definido",
          "evidencias": [
            "contexto-3",
            "contexto-2",
            "harness/contexto.md"
          ]
        },
        {
          "criterio": "Escribir qué se anota al cerrar la sesión.",
          "estado": "definido",
          "evidencias": [
            "contexto-4",
            "harness/ultima-sesion.md"
          ]
        },
        {
          "criterio": "Probar con menos contexto del que crees y comparar.",
          "estado": "definido",
          "evidencias": [
            "contexto-5",
            "casos/recortes/",
            "harness/contexto.md"
          ]
        },
        {
          "criterio": "Anotar qué dejaste fuera y por qué.",
          "estado": "definido",
          "evidencias": [
            "contexto-6",
            "harness/contexto.md"
          ]
        }
      ]
    },
    "memoria": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Decidir qué se guarda de cada uno de los cinco tipos.",
          "estado": "definido",
          "evidencias": [
            "memoria-1",
            "memoria-3"
          ]
        },
        {
          "criterio": "Elegir dónde vive cada tipo y quién lo edita.",
          "estado": "definido",
          "evidencias": [
            "memoria-3",
            "memoria-4",
            "memoria-2",
            "harness/memoria.md",
            "harness/estado-hilos.md"
          ]
        },
        {
          "criterio": "Definir qué se escribe al cerrar una sesión.",
          "estado": "definido",
          "evidencias": [
            "contexto-4",
            "memoria-5",
            "memoria-2",
            "harness/ultima-sesion.md"
          ]
        },
        {
          "criterio": "Fijar cada cuánto se revisa y qué se borra.",
          "estado": "definido",
          "evidencias": [
            "memoria-6",
            "harness/correcciones.md"
          ]
        },
        {
          "criterio": "Comprobar que otra persona entiende el estado solo leyendo.",
          "estado": "definido",
          "evidencias": [
            "memoria-7",
            "harness/estado-hilos.md"
          ]
        }
      ]
    },
    "prompts": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Escribir la orientación permanente en un solo sitio.",
          "estado": "definido",
          "evidencias": [
            "prompts-1",
            "harness/instrucciones.md"
          ]
        },
        {
          "criterio": "Marcar qué es preferencia personal y qué es regla del proyecto.",
          "estado": "definido",
          "evidencias": [
            "prompts-3",
            "harness/instrucciones.md"
          ]
        },
        {
          "criterio": "Definir la prioridad cuando dos instrucciones chocan.",
          "estado": "definido",
          "evidencias": [
            "prompts-2",
            "prompts-4",
            "prompts-3",
            "harness/instrucciones.md"
          ]
        },
        {
          "criterio": "Revisar periódicamente qué sigue vigente.",
          "estado": "definido",
          "evidencias": [
            "prompts-5",
            "harness/correcciones.md"
          ]
        },
        {
          "criterio": "Lo que no puede fallar, ponerlo donde el sistema lo imponga.",
          "estado": "definido",
          "evidencias": [
            "prompts-6",
            "harnessdev-2",
            ".claude/"
          ]
        }
      ]
    },
    "conocimiento": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Listar las fuentes autorizadas y quién mantiene cada una.",
          "estado": "definido",
          "evidencias": [
            "conocimiento-1",
            "conocimiento-3",
            "harness/fuentes.md"
          ]
        },
        {
          "criterio": "Escribir cuál manda en caso de conflicto.",
          "estado": "definido",
          "evidencias": [
            "conocimiento-1",
            "harness/fuentes.md"
          ]
        },
        {
          "criterio": "Marcar qué información no puede salir de su origen.",
          "estado": "definido",
          "evidencias": [
            "conocimiento-4",
            "guardrails-2"
          ]
        },
        {
          "criterio": "Definir cómo se cita la procedencia.",
          "estado": "definido",
          "evidencias": [
            "conocimiento-5"
          ]
        },
        {
          "criterio": "Decidir qué se responde cuando no hay fuente.",
          "estado": "definido",
          "evidencias": [
            "conocimiento-2",
            "harness/fuentes.md"
          ]
        }
      ]
    },
    "guardrails": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Listar qué datos toca y cuáles no pueden salir de su sitio.",
          "estado": "definido",
          "evidencias": [
            "guardrails-4",
            "guardrails-2",
            "guardrails-5"
          ]
        },
        {
          "criterio": "Dar a cada integración su identidad y su permiso mínimo.",
          "estado": "definido",
          "evidencias": [
            "guardrails-5",
            "tools-1",
            ".claude/settings.json"
          ]
        },
        {
          "criterio": "Tratar todo texto de terceros como información.",
          "estado": "definido",
          "evidencias": [
            "guardrails-1",
            "guardrails-6"
          ]
        },
        {
          "criterio": "Escribir qué acciones exigen confirmación.",
          "estado": "definido",
          "evidencias": [
            "guardrails-7",
            "tools-1"
          ]
        },
        {
          "criterio": "Estimar el daño máximo y ajustar el encierro.",
          "estado": "definido",
          "evidencias": [
            "guardrails-3",
            "guardrails-8",
            "tools-2"
          ]
        },
        {
          "criterio": "Definir retención y borrado.",
          "estado": "definido",
          "evidencias": [
            "guardrails-4",
            "memoria-2"
          ]
        }
      ]
    },
    "proveedor": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Escribir qué plataforma y qué modelo usas, y por qué.",
          "estado": "definido",
          "evidencias": [
            "proveedor-1",
            "proveedor-3"
          ]
        },
        {
          "criterio": "Anotar coste y límites previstos.",
          "estado": "definido",
          "evidencias": [
            "proveedor-4"
          ]
        },
        {
          "criterio": "Revisar condiciones de datos y privacidad.",
          "estado": "definido",
          "evidencias": [
            "proveedor-5",
            "harness/plataforma.md"
          ]
        },
        {
          "criterio": "Definir qué se hace si el servicio no está.",
          "estado": "definido",
          "evidencias": [
            "proveedor-2",
            "harness/plataforma.md"
          ]
        },
        {
          "criterio": "Anotar qué parte es portable.",
          "estado": "definido",
          "evidencias": [
            "proveedor-6"
          ]
        },
        {
          "criterio": "Si hay código propio: aislar la llamada en un único sitio.",
          "estado": "no_aplica",
          "evidencias": [
            "diagnostico.ejes.forma_codigo"
          ]
        }
      ]
    },
    "tools": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Listar qué herramientas hacen falta y para qué tarea.",
          "estado": "definido",
          "evidencias": [
            "tools-1",
            "tools-2",
            "tools-3",
            "harness/herramientas.md"
          ]
        },
        {
          "criterio": "Separar las que leen de las que escriben o gastan.",
          "estado": "definido",
          "evidencias": [
            "tools-1",
            "tools-3",
            "harness/herramientas.md"
          ]
        },
        {
          "criterio": "Dar identidad y permiso mínimo a cada una.",
          "estado": "definido",
          "evidencias": [
            "tools-4",
            "tools-3",
            "harness/herramientas.md"
          ]
        },
        {
          "criterio": "Escribir cuáles piden confirmación.",
          "estado": "definido",
          "evidencias": [
            "tools-1",
            "tools-5",
            "harness/herramientas.md"
          ]
        },
        {
          "criterio": "Anotar qué pasa si una falla a medias.",
          "estado": "definido",
          "evidencias": [
            "tools-6",
            "harness/herramientas.md"
          ]
        },
        {
          "criterio": "Dejar por escrito la alternativa manual.",
          "estado": "definido",
          "evidencias": [
            "tools-7",
            "harness/herramientas.md"
          ]
        }
      ]
    },
    "salida": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Escribir qué tipo de resultado produce cada tarea.",
          "estado": "definido",
          "evidencias": [
            "salida-1",
            "salida-3",
            "harness/resultados.md"
          ]
        },
        {
          "criterio": "Anotar quién lo consume: persona o máquina.",
          "estado": "definido",
          "evidencias": [
            "salida-4",
            "global-1"
          ]
        },
        {
          "criterio": "Definir dónde se guarda.",
          "estado": "definido",
          "evidencias": [
            "salida-1",
            "borradores/PLANTILLA.md"
          ]
        },
        {
          "criterio": "Marcar el estado: borrador, revisado o definitivo.",
          "estado": "definido",
          "evidencias": [
            "salida-2",
            "borradores/PLANTILLA.md"
          ]
        },
        {
          "criterio": "Exigir fuentes y dudas dentro del resultado.",
          "estado": "definido",
          "evidencias": [
            "salida-1",
            "borradores/PLANTILLA.md"
          ]
        },
        {
          "criterio": "Listar los efectos externos que puede producir.",
          "estado": "definido",
          "evidencias": [
            "salida-5",
            "tools-1",
            "guardrails-3"
          ]
        }
      ]
    },
    "flujo": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Listar las tareas habituales y cuáles merecen secuencia preparada.",
          "estado": "definido",
          "evidencias": [
            "flujo-1",
            "flujo-3",
            "harness/flujo-correo.md"
          ]
        },
        {
          "criterio": "Escribir los pasos y el criterio de parada de cada una.",
          "estado": "definido",
          "evidencias": [
            "flujo-1",
            "flujo-2",
            "flujo-3",
            "harness/flujo-correo.md"
          ]
        },
        {
          "criterio": "Fijar topes de intentos, tiempo y coste.",
          "estado": "definido",
          "evidencias": [
            "flujo-2",
            "flujo-4",
            "harness/flujo-correo.md"
          ]
        },
        {
          "criterio": "Marcar dónde hace falta visto bueno.",
          "estado": "definido",
          "evidencias": [
            "flujo-5",
            "flujo-6",
            "salida-2"
          ]
        },
        {
          "criterio": "Definir cuándo y a quién se escala.",
          "estado": "definido",
          "evidencias": [
            "flujo-6",
            "harness/flujo-correo.md"
          ]
        },
        {
          "criterio": "Anotar qué decide el modelo y qué la persona.",
          "estado": "definido",
          "evidencias": [
            "flujo-7",
            "flujo-3",
            "flujo-5"
          ]
        }
      ]
    },
    "validar": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Estimar el coste de comprobar cada tipo de resultado.",
          "estado": "definido",
          "evidencias": [
            "validar-3",
            "validar-1",
            "validar-2",
            "harness/coste-de-comprobar.md"
          ]
        },
        {
          "criterio": "Separar tiempo propio, espera, dinero y dificultad.",
          "estado": "definido",
          "evidencias": [
            "validar-3"
          ]
        },
        {
          "criterio": "Diseñar un escalón barato para lo que salga caro.",
          "estado": "definido",
          "evidencias": [
            "validar-2",
            "harness/coste-de-comprobar.md"
          ]
        },
        {
          "criterio": "Anotar el coste de un falso bien y de un falso mal.",
          "estado": "definido",
          "evidencias": [
            "validar-4",
            "riesgo registrado en la pieza validar"
          ]
        },
        {
          "criterio": "Revisar la autonomía a la luz de ese coste.",
          "estado": "definido",
          "evidencias": [
            "validar-5",
            "validar-3",
            "global-2"
          ]
        }
      ]
    },
    "medidor": {
      "resultado": "descartada",
      "criterios": [
        {
          "criterio": "Reunir casos que deben aprobar y casos que deben fallar.",
          "estado": "no_aplica",
          "evidencias": [
            "descarte registrado en la propia pieza"
          ]
        },
        {
          "criterio": "Comprobar el revisor contra ellos antes de fiarte.",
          "estado": "no_aplica",
          "evidencias": [
            "descarte registrado en la propia pieza"
          ]
        },
        {
          "criterio": "Separar quien genera de quien evalúa.",
          "estado": "no_aplica",
          "evidencias": [
            "descarte registrado en la propia pieza"
          ]
        },
        {
          "criterio": "Revisar los desacuerdos con la persona.",
          "estado": "no_aplica",
          "evidencias": [
            "descarte registrado en la propia pieza"
          ]
        },
        {
          "criterio": "Declarar qué cubre y qué no.",
          "estado": "no_aplica",
          "evidencias": [
            "descarte registrado en la propia pieza"
          ]
        }
      ]
    },
    "eval": {
      "resultado": "deuda_aceptada",
      "criterios": [
        {
          "criterio": "Reunir de seis a diez encargos reales.",
          "estado": "definido",
          "evidencias": [
            "eval-1",
            "casos/"
          ]
        },
        {
          "criterio": "Guardar el resultado que consideras bueno.",
          "estado": "definido",
          "evidencias": [
            "eval-1",
            "eval-2"
          ]
        },
        {
          "criterio": "Añadir casos límite y usos indebidos.",
          "estado": "parcial",
          "evidencias": [
            "eval-3",
            "fallos-2",
            "deuda de la pieza eval",
            "deuda aceptada de la pieza"
          ]
        },
        {
          "criterio": "Escribir la checklist de aceptación.",
          "estado": "definido",
          "evidencias": [
            "eval-1",
            "eval-4",
            "harness/checklist-revision.md"
          ]
        },
        {
          "criterio": "Guardar lo corregido y qué se corrigió.",
          "estado": "definido",
          "evidencias": [
            "eval-2",
            "observabilidad-1"
          ]
        },
        {
          "criterio": "Revisar el banco con casos nuevos.",
          "estado": "definido",
          "evidencias": [
            "eval-5",
            "observabilidad-2"
          ]
        }
      ]
    },
    "observabilidad": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Decidir qué se anota: petición, acción, fuentes, cambios y coste.",
          "estado": "definido",
          "evidencias": [
            "observabilidad-3",
            "observabilidad-1",
            "harness/correcciones.md"
          ]
        },
        {
          "criterio": "Registrar sobre todo lo aprobado, corregido y rechazado.",
          "estado": "definido",
          "evidencias": [
            "observabilidad-4"
          ]
        },
        {
          "criterio": "Fijar una revisión periódica.",
          "estado": "definido",
          "evidencias": [
            "observabilidad-2",
            "harness/correcciones.md"
          ]
        },
        {
          "criterio": "Definir cómo cada aprendizaje se convierte en regla.",
          "estado": "definido",
          "evidencias": [
            "observabilidad-2",
            "harness/correcciones.md"
          ]
        },
        {
          "criterio": "Decidir retención y acceso de los registros.",
          "estado": "definido",
          "evidencias": [
            "observabilidad-5"
          ]
        }
      ]
    },
    "harnessdev": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Inventariar qué mecanismos usas y para qué.",
          "estado": "definido",
          "evidencias": [
            "harnessdev-1",
            "harnessdev-3",
            "harness/mecanismos.md"
          ]
        },
        {
          "criterio": "Colocar cada regla en un único sitio.",
          "estado": "definido",
          "evidencias": [
            "harnessdev-3",
            "harnessdev-2"
          ]
        },
        {
          "criterio": "Separar configuración personal, de proyecto y de organización.",
          "estado": "definido",
          "evidencias": [
            "harnessdev-4"
          ]
        },
        {
          "criterio": "Versionar lo que deba viajar con el proyecto.",
          "estado": "definido",
          "evidencias": [
            "harnessdev-4",
            ".claude/"
          ]
        },
        {
          "criterio": "Comprobar que alguien puede clonar y arrancar sin ayuda.",
          "estado": "definido",
          "evidencias": [
            "harness/herramientas.md",
            "harnessdev-1"
          ]
        }
      ]
    },
    "fallos": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Abrir un registro de incidentes con su evidencia.",
          "estado": "definido",
          "evidencias": [
            "fallos-1",
            "fallos-3",
            "harness/incidentes.md"
          ]
        },
        {
          "criterio": "Buscar patrones antes de escribir defensas.",
          "estado": "definido",
          "evidencias": [
            "fallos-4"
          ]
        },
        {
          "criterio": "Convertir cada patrón en regla o límite.",
          "estado": "definido",
          "evidencias": [
            "fallos-2",
            "fallos-4"
          ]
        },
        {
          "criterio": "Añadir un caso que detecte ese fallo.",
          "estado": "definido",
          "evidencias": [
            "fallos-5",
            "fallos-2"
          ]
        },
        {
          "criterio": "Comprobar que la defensa funciona.",
          "estado": "definido",
          "evidencias": [
            "fallos-5",
            "harness/incidentes.md",
            "verificación de la pieza fallos"
          ]
        },
        {
          "criterio": "Poner fecha de revisión a cada defensa.",
          "estado": "definido",
          "evidencias": [
            "fallos-5"
          ]
        }
      ]
    },
    "epistemica": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Distinguir por escrito hecho, inferencia y desconocido.",
          "estado": "definido",
          "evidencias": [
            "epistemica-1",
            "epistemica-3"
          ]
        },
        {
          "criterio": "Exigir fuente para cada dato.",
          "estado": "definido",
          "evidencias": [
            "epistemica-3",
            "epistemica-1"
          ]
        },
        {
          "criterio": "Pedir evidencia de las acciones.",
          "estado": "definido",
          "evidencias": [
            "epistemica-4"
          ]
        },
        {
          "criterio": "Definir qué se verifica siempre y qué según riesgo.",
          "estado": "definido",
          "evidencias": [
            "epistemica-5",
            "epistemica-1"
          ]
        },
        {
          "criterio": "Aceptar «no lo sé» como resultado.",
          "estado": "definido",
          "evidencias": [
            "epistemica-2",
            "epistemica-1"
          ]
        },
        {
          "criterio": "Declarar la cobertura de lo comprobado.",
          "estado": "definido",
          "evidencias": [
            "epistemica-6",
            "epistemica-5"
          ]
        }
      ]
    },
    "historial": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Poner el harness bajo control de versiones desde el primer día.",
          "estado": "definido",
          "evidencias": [
            "historial-1",
            "historial-3"
          ]
        },
        {
          "criterio": "Sacar los secretos y documentar cuáles hacen falta.",
          "estado": "definido",
          "evidencias": [
            "historial-3",
            "historial-2"
          ]
        },
        {
          "criterio": "Tener una copia fuera de la máquina de trabajo.",
          "estado": "definido",
          "evidencias": [
            "historial-4",
            "historial-2"
          ]
        },
        {
          "criterio": "Escribir cómo se arranca desde cero.",
          "estado": "definido",
          "evidencias": [
            "historial-5"
          ]
        },
        {
          "criterio": "Comprobar que otra persona puede clonarlo.",
          "estado": "definido",
          "evidencias": [
            "historial-5",
            "historial-4"
          ]
        },
        {
          "criterio": "Anotar dependencias y procedencia.",
          "estado": "definido",
          "evidencias": [
            "historial-6"
          ]
        }
      ]
    },
    "fuera": {
      "resultado": "completada",
      "criterios": [
        {
          "criterio": "Abrir un registro de descartes con motivo y fecha.",
          "estado": "definido",
          "evidencias": [
            "fuera-4",
            "fuera-5",
            "fuera-1"
          ]
        },
        {
          "criterio": "Separar no aplica, no se construye, se pospone y deuda.",
          "estado": "definido",
          "evidencias": [
            "fuera-4",
            "fuera-5"
          ]
        },
        {
          "criterio": "Asignar responsable y condición de reapertura.",
          "estado": "definido",
          "evidencias": [
            "fuera-6",
            "fuera-4",
            "fuera-1",
            "fuera-2"
          ]
        },
        {
          "criterio": "Poner fecha de revisión al harness completo.",
          "estado": "definido",
          "evidencias": [
            "fuera-3",
            "fuera-7"
          ]
        },
        {
          "criterio": "Escribir qué pasa al retirarlo: accesos, secretos y datos.",
          "estado": "definido",
          "evidencias": [
            "fuera-7"
          ]
        }
      ]
    }
  }
};
