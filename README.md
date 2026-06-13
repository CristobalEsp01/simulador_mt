# Simulador de Máquina de Turing — INFO 139

Este proyecto consiste en un programa computacional desarrollado en **Python** capaz de simular una Máquina de Turing (MT) estándar reconocedora de lenguajes, utilizando una cinta semi-infinita (con inicio fijo a la izquierda y extensible hacia la derecha). 

El simulador está diseñado para ser completamente autoexplicativo, guiando al usuario paso a paso en el ingreso de los componentes del autómata por teclado y permitiendo evaluar múltiples palabras consecutivas para una misma máquina cargada.

---

## 🛠️ ¿Cómo lo hicimos? (Lógica del Simulador)

El motor de simulación replica el comportamiento teórico de una Máquina de Turing de una sola cinta. El flujo principal funciona de la siguiente manera:

1. **Inicialización:** La cinta se modela dinámicamente y el cabezal comienza obligatoriamente en la **posición 0** (extremo izquierdo).
2. **Ciclo de Ejecución:** El programa lee el símbolo bajo el cabezal y busca en la tabla de transiciones la acción correspondiente al `(estado_actual, simbolo_leido)`.
3. **Control de la Cinta Semi-Infinita:** * Si el cabezal se mueve a la derecha (`D`) más allá del contenido actual, la cinta se expande dinámicamente añadiendo el **Símbolo Blanco**.
   * Si el cabezal intenta moverse a la izquierda (`I`) estando en la posición `0`, la máquina se aborta inmediatamente por **bloqueo en el límite izquierdo**.
4. **Criterios de Parada y Finalización:**
   * **Aceptación:** Si la máquina alcanza un estado que pertenece al *Conjunto de Estados Finales*, la simulación se detiene con éxito.
   * **Rechazo por Bloqueo:** Si no existe una transición definida para la combinación actual de estado y símbolo, la máquina se detiene y la palabra se rechaza.
   * **Prevención de Bucles Infinitos:** Para evitar que el programa se congele ante palabras no aceptadas que ciclean (Problema de la Parada), implementamos un **Historial de Configuraciones**. Si la máquina repite una combinación idéntica de `(contenido_cinta, posición_cabezal, estado_actual)`, detecta el bucle determinista y aborta la ejecución rechazando la palabra.

---

## 📦 Estructuras de Datos Utilizadas

Para garantizar la máxima eficiencia en tiempo de ejecución ($O(1)$ en búsquedas y modificaciones) y cumplir con los requisitos académicos, utilizamos las siguientes estructuras nativas de Python:

* **Conjunto de Estados ($Q$) y Estados Finales ($F$):** Utiliza un `set` de strings. Esto permite validar si un estado pertenece al autómata de forma instantánea.
* **Estado Inicial ($q_0$):** Un `str` que almacena el punto de partida.
* **Tabla de Transiciones ($\delta$):** Un **Diccionario anidado (`dict`)** donde la clave externa es el `estado_actual`, la clave interna es el