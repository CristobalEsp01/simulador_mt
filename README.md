# Simulador de Maquina de Turing - Interfaz grafica

Interfaz didactica (Tkinter) para el simulador de Maquina de Turing 
## Archivos

- `interfaz.py` ........ interfaz grafica (definicion de la maquina + evaluacion de palabras)
- `main.py` ........ motor de la MT

## Ejecutar desde el codigo fuente

Requiere Python 3 con Tkinter (incluido en la instalacion estandar de Windows y macOS;
en Linux: `sudo apt install python3-tk`).

```
python interfaz.py
```

## Generar el ejecutable

El ejecutable se crea con PyInstaller. IMPORTANTE: PyInstaller produce un
ejecutable para el sistema operativo donde se compila. Para obtener un `.exe`
de Windows hay que compilar EN Windows.

1. Instalar PyInstaller:

   ```
   pip install pyinstaller
   ```

2. Compilar (desde la carpeta del codigo fuente):

   ```
   pyinstaller --onefile --windowed --name SimuladorMT --add-data "main.py:." interfaz.py
   ```

   En Windows, el separador de `--add-data` es `;` en lugar de `:`:

   ```
   pyinstaller --onefile --windowed --name SimuladorMT --add-data "main.py;." interfaz.py
   ```

   El ejecutable queda en la carpeta `dist/`.

## Uso de la interfaz

1. Pestaña "Definir maquina": ingresa estados, estado inicial, finales, alfabeto
   de cinta, simbolo blanco, alfabeto de entrada y las transiciones (una por una).
   El boton "Cargar ejemplo" precarga una maquina que reconoce a^n b^n.
2. Pulsa "Construir maquina".
3. Pestaña "Evaluar palabras": escribe palabras y obten si pertenecen o no al
   lenguaje, junto con la cinta final y un historial de las pruebas.
