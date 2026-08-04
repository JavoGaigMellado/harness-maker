---
name: start
description: Prepara la copia para trabajar (entorno, recorrido activo, guardián, validación y pruebas), abre el mapa en el navegador y dice cuál es el siguiente trabajo. Invocar manualmente con /start.
disable-model-invocation: true
---

<!-- GENERADO por `harness-lab generate`. NO EDITAR A MANO. -->
# Arranque

Objetivo: que la persona pueda empezar con un solo comando, sin leer la guía de traslado ni
recordar en qué orden va cada paso.

1. Ejecutar `python arrancar.py` desde la raíz del repositorio. Funciona sobre un clon recién
   hecho porque solo usa la biblioteca estándar: crea `.venv` si falta, instala el paquete y
   después delega en `harness-lab start`, que es donde vive la lógica. Si el entorno ya está
   listo, basta `harness-lab start`.
2. No inventar los pasos ni ejecutarlos por separado. Si el arrancador falla, leer su salida:
   informa de qué comprobación cayó y por qué. Un arranque en rojo no se sortea a mano.
3. Leer la fotografía que imprime y **repetírsela a la persona en lenguaje llano**: si el
   entorno quedó listo, qué dice el recorrido activo, si la validación y las pruebas están en
   verde, y cuál es la siguiente actividad.
4. Si alguna comprobación está en rojo, decirlo primero y proponer el arreglo concreto antes
   de ofrecer trabajo del recorrido. Trabajar sobre rojo confunde un fallo del taller con un
   fallo de la máquina, y eso contamina cualquier prueba posterior.
5. El mapa se abre solo en el navegador. Si la persona no lo ve, darle **la ruta que el arrancador
   acaba de imprimir**, no una fija: en una copia recibida el mapa es `diagramas/diagrama_taller.html`
   y `diagramas/mapa_harness_lab.html` no existe, porque es del recorrido propio del proyecto y no
   viaja. Carga sus datos por `<script>` y no necesita servidor, así que basta el doble clic. Con
   `file://` enseña la semilla generada; para que se refresque solo, abrirlo con Live Preview.
6. Cerrar diciendo qué puede hacer ya y con qué comando sigue. Si no queda actividad abierta
   pero hay verificaciones pendientes, nombrarlas: definidas no es lo mismo que comprobadas.

Lo que este comando **no** hace, y hay que decirlo si la persona lo espera: no instala Python,
no reinicia el recorrido existente y no toca el recorrido de otro proyecto. Para empezar uno
nuevo desde cero está `harness-lab init --reiniciar`, que aparta el anterior sin borrarlo.
