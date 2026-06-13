import sys

def simular_mt_con_historial(estado_inicial, estados_finales, transiciones, palabra_entrada, simbolo_blanco="B"):
    # Inicializar la cinta. Si la palabra está vacía, la cinta parte con un blanco.
    cinta = list(palabra_entrada) if palabra_entrada != "" else [simbolo_blanco]
    cabezal = 0
    estado_actual = estado_inicial
    
    # Conjunto para guardar el historial de configuraciones (para detectar bucles infinitos)
    historial_configuraciones = set()
    
    # El bucle continúa mientras el estado actual NO pertenezca al conjunto de estados finales
    while estado_actual not in estados_finales:
        # Generar un identificador único de la configuración actual
        cinta_str = "".join(cinta)
        configuracion_actual = (cinta_str, cabezal, estado_actual)
        
        # SI LA CONFIGURACIÓN YA EXISTÍA: ¡Bucle infinito detectado!
        if configuracion_actual in historial_configuraciones:
            print("\n⚠️ [Simulación Abortada]: Se detectó un bucle infinito determinista.")
            return False, cinta_str.strip(simbolo_blanco)
        
        # Guardar la configuración en el historial
        historial_configuraciones.add(configuracion_actual)
        
        # --- Control de la Cinta Semi-Infinita ---
        # Si se mueve a la derecha más allá del contenido actual, expandimos con un Blanco
        if cabezal >= len(cinta):
            cinta.append(simbolo_blanco)
        # Si intenta moverse a la izquierda de la posición 0, la máquina se bloquea
        elif cabezal < 0:
            print("\n❌ [Simulación Abortada]: El cabezal intentó salir del extremo izquierdo de la cinta.")
            return False, "".join(cinta).strip(simbolo_blanco)
            
        simbolo_actual = cinta[cabezal]
        
        # --- Ejecución de la Transición ---
        if estado_actual in transiciones and simbolo_actual in transiciones[estado_actual]:
            nuevo_estado, simbolo_escrito, movimiento = transiciones[estado_actual][simbolo_actual]
            
            # Aplicar cambios
            cinta[cabezal] = simbolo_escrito
            estado_actual = nuevo_estado
            
            # Mover cabezal usando D (Derecha) e I (Izquierda)
            if movimiento == "D":
                cabezal += 1
            elif movimiento == "I":
                cabezal -= 1
        else:
            # Rechazo por bloqueo (No existe la transición q_actual + sim_actual)
            print(f"\n❌ [Simulación Abortada]: No existe transición definida para el estado '{estado_actual}' leyendo '{simbolo_actual}'.")
            return False, "".join(cinta).strip(simbolo_blanco)
            
    # Si sale del ciclo, significa que estado_actual IN estados_finales (Aceptación)
    return True, "".join(cinta).strip(simbolo_blanco)


def ingresar_datos_mt():
    print("="*60)
    print("  SIMULADOR DE MÁQUINA DE TURING (INFO 139)  ")
    print("="*60)
    print("Por favor, ingrese los componentes de la máquina.\n")

    # 1. Conjunto de Estados
    print("[1] CONJUNTO DE ESTADOS")
    print("Ingrese los estados separados por espacios (Ej: q0 q1 q2 qf q_rec):")
    estados = set(input(">> ").strip().split())
    
    # 2. Estado Inicial
    print("\n[2] ESTADO INICIAL")
    while True:
        estado_inicial = input(">> En qué estado inicia la MT?: ").strip()
        if estado_inicial in estados:
            break
        print(f"❌ Error: El estado '{estado_inicial}' no pertenece al conjunto de estados.")

    # 3. Conjunto de Estados Finales (Aceptación)
    print("\n[3] CONJUNTO DE ESTADOS FINALES (Aceptación)")
    while True:
        print("Ingrese los estados finales separados por espacios (Ej: qf q_ok):")
        estados_finales = set(input(">> ").strip().split())
        
        # Validar que todos los estados finales ingresados existan en el conjunto global de estados
        if estados_finales.issubset(estados) and len(estados_finales) > 0:
            break
        print(f"❌ Error: Todos los estados finales deben pertenecer al conjunto de estados inicial y debe ingresar al menos uno.")

    # 4. Alfabeto de la Cinta y Símbolo Blanco
    print("\n[4] ALFABETO DE LA CINTA")
    print("Ingrese los símbolos permitidos en la cinta separados por espacios (Ej: 0 1 X Y B):")
    alfabeto_cinta = set(input(">> ").strip().split())
    
    while True:
        simbolo_blanco = input(">> Cuál de estos símbolos representa el BLANCO? (Ej: B): ").strip()
        if simbolo_blanco in alfabeto_cinta:
            break
        print(f"❌ Error: El símbolo blanco debe pertenecer al alfabeto de la cinta.")

    # 5. Alfabeto de la Entrada
    print("\n[5] ALFABETO DE LA PALABRA DE ENTRADA")
    while True:
        print(f"Ingrese los símbolos de entrada separados por espacios (No debe incluir el blanco '{simbolo_blanco}'):")
        alfabeto_entrada = set(input(">> ").strip().split())
        if simbolo_blanco not in alphabet_entrada if 'alphabet_entrada' in locals() else simbolo_blanco not in alfabeto_entrada:
            break
        print(f"❌ Error: El alfabeto de entrada no puede contener el símbolo blanco.")

    # 6. Transiciones
    print("\n[6] TRANSICIONES DE LA MÁQUINA")
    print("Ingrese las transiciones una por una.")
    print("Formato requerido: estado_actual simbolo_leido -> nuevo_estado simbolo_escrito movimiento")
    print("Ejemplo: q0 1 -> q1 X D")
    print("(Escriba 'FIN' cuando haya terminado de ingresar todas las transiciones)\n")
    
    transiciones = {}
    for est in estados:
        transiciones[est] = {}

    contador = 1
    while True:
        entrada_transicion = input(f"Transición #{contador}: ").strip()
        if entrada_transicion.upper() == "FIN":
            if not any(transiciones[est] for est in estados):
                print("⚠️ Al menos debes ingresar una transición para simular la máquina.")
                continue
            break
            
        try:
            if "->" in entrada_transicion:
                izq, der = entrada_transicion.split("->")
                est_act, sim_lei = izq.strip().split()
                n_est, sim_esc, mov = der.strip().split()
            else:
                est_act, sim_lei, n_est, sim_esc, mov = entrada_transicion.split()
            
            mov = mov.upper()

            if est_act not in estados or n_est not in estados:
                print("❌ Error: Uno de los estados no pertenece al conjunto inicial.")
                continue
            if sim_lei not in alfabeto_cinta or sim_esc not in alfabeto_cinta:
                print("❌ Error: Uno de los símbolos no pertenece al alfabeto de la cinta.")
                continue
            if mov not in ["D", "I"]:
                print("❌ Error: El movimiento debe ser 'D' (Derecha) o 'I' (Izquierda).")
                continue
                
            transiciones[est_act][sim_lei] = (n_est, sim_esc, mov)
            contador += 1
            
        except ValueError:
            print("❌ Formato incorrecto. Recuerda el ejemplo: q0 1 -> q1 X D")

    return estado_inicial, estados_finales, transiciones, alfabeto_entrada, simbolo_blanco


def main():
    # Cargar la configuración de la MT por teclado
    estado_inicial, estados_finales, transiciones, alfabeto_entrada, simbolo_blanco = ingresar_datos_mt()
    
    # Bucle para evaluar múltiples cadenas con la misma MT
    while True:
        print("\n" + "="*60)
        print("  PROCESAR PALABRA DE ENTRADA  ")
        print("="*60)
        print(f"Ingrese la palabra a analizar (Símbolos válidos: {', '.join(alfabeto_entrada)})")
        print("O escriba 'SALIR' para cerrar el programa.")
        
        palabra = input(">> ").strip()
        
        if palabra.upper() == "SALIR":
            print("\n¡Programa finalizado exitosamente!")
            sys.exit()
            
        # Validar el alfabeto de la palabra ingresada
        palabra_valida = True
        for caracter in palabra:
            if caracter not in alfabeto_entrada:
                print(f"❌ Error: El carácter '{caracter}' no pertenece al alfabeto de entrada.")
                palabra_valida = False
                break
                
        if not palabra_valida:
            continue
            
        print(f"\nProcesando la palabra '{palabra}'...")
        
        es_aceptada, cinta_resultante = simular_mt_con_historial(
            estado_inicial, estados_finales, transiciones, palabra, simbolo_blanco
        )
        
        # --- PRESENTACIÓN DE RESULTADOS ---
        print("-" * 40)
        print("RESULTADO DE LA EVALUACIÓN:")
        if es_aceptada:
            print("🎉 ¡ÉXITO! La palabra PERTENECE al lenguaje.")
        else:
            print("❌ RECHAZADA. La palabra NO PERTENECE al lenguaje.")
        print(f"Contenido final de la cinta (sin blancos externos): '{cinta_resultante}'")
        print("-" * 40)


if __name__ == "__main__":
    main()