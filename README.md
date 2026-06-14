# Simulador de Maquina de Turing - INFO 139

Programa en Python que simula una Maquina de Turing reconocedora de lenguajes, con cinta semi-infinita.

## Como ejecutar

```
python main.py
```

El programa pide por teclado los estados, transiciones y la palabra a evaluar, y dice si pertenece o no al lenguaje.

## Como funciona

La cinta se representa como una lista que se expande hacia la derecha cuando es necesario. El cabezal no puede salir por la izquierda.

En cada paso se lee el simbolo bajo el cabezal, se busca la transicion correspondiente y se aplica. Si no hay transicion definida, la palabra se rechaza.

Para evitar loops infinitos se guarda un historial de configuraciones (cinta, posicion del cabezal, estado). Si se repite alguna, se aborta.

## Estructuras usadas

- Estados: `set`
- Estado inicial: `str`
- Transiciones: `dict` anidado, `transiciones[estado][simbolo] = (nuevo_estado, simbolo_escrito, movimiento)`
- Cinta: `list`
