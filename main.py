import sys

def simular_mt(estado_inicial, estados_finales, transiciones, palabra_entrada, simbolo_blanco="B"):
    # Si la palabra es vacía la cinta empieza con un blanco
    cinta = list(palabra_entrada) if palabra_entrada != "" else [simbolo_blanco]
    cabezal = 0
    estado_actual = estado_inicial

    # Guardamos configuraciones anteriores para detectar si entra en loop
    historial = set()

    while estado_actual not in estados_finales:
        cinta_str = "".join(cinta)
        config = (cinta_str, cabezal, estado_actual)

        if config in historial:
            print("\n[Abortado] Se detectó un bucle infinito.")
            return False, cinta_str.strip(simbolo_blanco)

        historial.add(config)

        # Expandir cinta si el cabezal se va a la derecha
        if cabezal >= len(cinta):
            cinta.append(simbolo_blanco)
        elif cabezal < 0:
            print("\n[Abortado] El cabezal intentó salir por la izquierda.")
            return False, "".join(cinta).strip(simbolo_blanco)

        simbolo_actual = cinta[cabezal]

        if estado_actual in transiciones and simbolo_actual in transiciones[estado_actual]:
            nuevo_estado, simbolo_escrito, movimiento = transiciones[estado_actual][simbolo_actual]

            cinta[cabezal] = simbolo_escrito
            estado_actual = nuevo_estado

            if movimiento == "D":
                cabezal += 1
            elif movimiento == "I":
                cabezal -= 1
        else:
            print(f"\n[Abortado] No hay transición para estado '{estado_actual}' con símbolo '{simbolo_actual}'.")
            return False, "".join(cinta).strip(simbolo_blanco)

    return True, "".join(cinta).strip(simbolo_blanco)


def ingresar_datos_mt_estricto():
    print("="*60)
    print("  SIMULADOR DE MÁQUINA DE TURING - INFO 139  ")
    print("="*60)
    print("Ingrese exclusivamente los componentes solicitados.\n")

    # 1. Estado Inicial
    print("[1] ESTADO INICIAL")
    estado_inicial = input(">> Estado inicial: ").strip()

    # 2. Estados Finales
    print("\n[2] ESTADOS FINALES")
    print("Ingrese los estados de aceptación separados por espacios (ej: qf):")
    estados_finales = set(input(">> ").strip().split())

    # 3. Transiciones
    print("\n[3] TRANSICIONES")
    print("Formato: estado_actual simbolo_leido -> nuevo_estado simbolo_escrito movimiento")
    print("Ejemplo: q0 1 -> q1 X D")
    print("Escriba FIN para terminar.\n")

    transiciones = {}
    simbolo_blanco = "B"  # Fijado por defecto según requerimiento estructural
    
    # Conjuntos para recopilar la información implícita de las transiciones
    alfabeto_cinta_descubierto = {simbolo_blanco}

    contador = 1
    while True:
        entrada = input(f"Transición #{contador}: ").strip()
        if entrada.upper() == "FIN":
            if not transiciones:
                print("Ingrese al menos una transición.")
                continue
            break

        try:
            if "->" in entrada:
                izq, der = entrada.split("->")
                est_act, sim_lei = izq.strip().split()
                n_est, sim_esc, mov = der.strip().split()
            else:
                est_act, sim_lei, n_est, sim_esc, mov = entrada.split()

            mov = mov.upper()

            if mov not in ["D", "I"]:
                print("Error: el movimiento debe ser D o I.")
                continue

            # Registro y descubrimiento dinámico de símbolos de la cinta
            alfabeto_cinta_descubierto.add(sim_lei)
            alfabeto_cinta_descubierto.add(sim_esc)

            # Inicializar dinámicamente el diccionario indexado por el estado actual
            if est_act not in transiciones:
                transiciones[est_act] = {}
                
            transiciones[est_act][sim_lei] = (n_est, sim_esc, mov)
            contador += 1

        except ValueError:
            print("Formato incorrecto. Ejemplo: q0 1 -> q1 X D")

    # --- INFERENCIA AUTOMÁTICA DEL ALFABETO DE ENTRADA ---
    # Se asume que el alfabeto de la palabra está compuesto por los símbolos que la máquina
    # es capaz de leer directamente desde su estado inicial, excluyendo el espacio en blanco "B".
    alfabeto_entrada = set()
    if estado_inicial in transiciones:
        for simbolo in transiciones[estado_inicial].keys():
            if simbolo != simbolo_blanco:
                alfabeto_entrada.add(sim_simbolo) if 'sim_simbolo' in locals() else alfabeto_entrada.add(simbolo)

    # Caso de resguardo: si en el estado inicial solo lee el blanco, mapeamos los caracteres 
    # descubiertos en la cinta que no correspondan a símbolos de control clásicos (X, Y) ni al blanco.
    if not alfabeto_entrada:
        alfabeto_entrada = {sim for sim in alfabeto_cinta_descubierto if sim not in [simbolo_blanco, "X", "Y"]}

    return estado_inicial, estados_finales, transiciones, alfabeto_entrada, simbolo_blanco


def main():
    # El menú inicial ahora solo captura lo estrictamente solicitado por la pauta
    estado_inicial, estados_finales, transiciones, alfabeto_entrada, simbolo_blanco = ingresar_datos_mt_estricto()

    while True:
        print("\n" + "="*60)
        print("  INGRESAR PALABRA  ")
        print("="*60)
        print(f"Símbolos de entrada válidos (inferidos): {', '.join(alfabeto_entrada) if alfabeto_entrada else 'Cualquiera excepto B'}")
        print("Escriba SALIR para terminar.")

        palabra = input(">> ").strip()

        if palabra.upper() == "SALIR":
            print("Programa finalizado.")
            sys.exit()

        palabra_valida = True
        for caracter in palabra:
            if caracter == simbolo_blanco:
                print(f"Error: el carácter '{caracter}' corresponde al símbolo blanco y no puede ir en la entrada.")
                palabra_valida = False
                break

        if not palabra_valida:
            continue

        print(f"\nProcesando '{palabra}'...")

        es_aceptada, cinta_resultante = simular_mt(
            estado_inicial, estados_finales, transiciones, palabra, simbolo_blanco
        )

        print("-" * 40)
        if es_aceptada:
            print("🎉 ACEPTADA. La palabra pertenece al lenguaje.")
        else:
            print("❌ RECHAZADA. La palabra no pertenece al lenguaje.")
        print(f"Cinta final: '{cinta_resultante}'")
        print("-" * 40)


if __name__ == "__main__":
    main()