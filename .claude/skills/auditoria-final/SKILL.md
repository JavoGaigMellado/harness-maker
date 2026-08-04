---
name: auditoria-final
description: Audita en profundidad un proyecto terminado de Harness-Maker desde cero: lee el repositorio completo, contrasta código, estado, pruebas, git y chats autorizados de Claude y ChatGPT, encuentra fallos y propone cambios sin implementarlos. Invocar manualmente con /auditoria-final después de /cierre.
disable-model-invocation: true
---

<!-- GENERADO por `harness-lab generate`. NO EDITAR A MANO. -->
# Auditoría final

1. Leer por completo `taller/prompts/100_auditoria_final.md` y cumplir todas sus puertas de evidencia.
2. Empezar con hipótesis vacías. No usar conclusiones de este chat salvo que reaparezcan en una
   fuente auditada.
3. Resolver el recorrido solo mediante `.harness-maker.json`; usar como salida el directorio
   `auditorias/` situado junto a su archivo de estado.
4. Mostrar un **Estado actual** con commit, limpieza del árbol, archivos inventariados, fuentes de
   conversación encontradas y el recuento exacto por estado: completadas y verificadas, completadas
   sin verificar, abiertas, con deuda y descartadas. Nombrar también las tres vidas del proyecto
   —doctrina, taller e instancia— con los directorios que ocupa cada una.
5. Preguntar con `AskUserQuestion` únicamente por: autorización para leer los chats externos
   candidatos, autorización para ejercitar la frontera de permisos con los intentos concretos que se
   van a hacer, rutas de exportaciones que no sean observables y la decisión de auditar una
   fotografía sucia o incompleta. Agrupar todo lo conocido; no preguntar datos disponibles.
6. Si la interfaz exige varias ventanas, abrir todas las necesarias dentro de esta ejecución. Tras
   recibir autorización, leer solo conversaciones vinculadas al proyecto por ruta, nombre y fecha.
7. Realizar la auditoría completa. Se pueden usar agentes auxiliares si están disponibles para
   pasadas independientes, pero el agente principal debe inventariar primero, entregarles fuentes
   sin conclusiones previas y verificar por sí mismo cada hallazgo incorporado.
8. Escribir exclusivamente `auditoria-final.md` y `auditoria-final.json`. No aplicar propuestas ni
   actualizar estado, cobertura o auditoría semántica durante esta ejecución.
9. Validar que ambos entregables coincidan, que cada hallazgo tenga evidencia, aceptación y la vida
   del proyecto a la que pertenece, y que `git status` no muestre otras escrituras atribuibles a la
   auditoría.
10. Responder con la estructura adaptada a la persona: primero los cuatro veredictos y si está listo
    para repartir, después los cinco hallazgos principales y el enlace al informe. La capacidad final
    es comprender el proyecto y disponer de un plan argumentado, no haber implementado todavía las
    mejoras.

## Explicación adaptada a la persona

Buscar en Contexto una decisión `Perfil de interacción`. Si no existe, usar **Simple y guiado**:

- `Simple y guiado` — explicar el resultado y la próxima acción con palabras cotidianas. No poner
  rutas, nombres de funciones, pruebas ni detalles de implementación en la conclusión principal.
- `Breve y directo` — dar estado, decisiones, capacidad y siguiente paso sin explicación didáctica.
- `Técnico y detallado` — incluir además archivos, implementación, comprobaciones y riesgos.

El nivel describe cómo presentar la información, no la capacidad de la persona. Cambiarlo cuando lo
pida explícitamente y guardar entonces la preferencia confirmada en Contexto; no convertir una sola
pregunta técnica en un cambio de perfil.

Cerrar siempre con esta estructura y en este orden:

1. `Actividad completada: <nombre>` o `Actividad en curso: <nombre>`.
2. **En una frase** — qué se acaba de conseguir, sin jerga.
3. **Lo que decidiste** — lista breve; separar lo confirmado por la persona de lo observado o
   implementado automáticamente.
4. **Qué cambia para ti** — consecuencia práctica al usar el harness.
5. **Tu harness ahora puede** — una sola frase acumulativa y comprensible.
6. **Qué queda** — número de actividades resueltas y abiertas, y siguiente actividad explicada en
   lenguaje normal.
7. **Impacto en otras partes** — decir `Ninguno` o nombrarlas con una frase práctica por cada una.
8. **Detalles técnicos** — solo si el perfil es técnico, la persona los pide o necesita actuar ante
   un fallo. Resumir rutas, pruebas y riesgos; no narrar refactorizaciones ni decir que «las pruebas
   mentían» en la explicación principal.

No pegar un informe interno largo. Un riesgo que afecte a la persona sí se explica, pero primero en
lenguaje normal y después, si hace falta, con su causa técnica.
