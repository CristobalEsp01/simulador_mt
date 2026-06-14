import sys

def simular_mt(estado_inicial, estados_finales, transiciones, palabra_entrada, simbolo_blanco="B"):
    # si la palabra es vacia la cinta empieza con un blanco
    cinta = list(palabra_entrada) if palabra_entrada != "" else [simbolo_blanco]
    cabezal = 0
    estado_actual = estado_inicial

    # guardamos configuraciones anteriores para detectar si entra en loop
    historial = set()

    while estado_actual not in estados_finales:
        cinta_str = "".join(cinta)
        config = (cinta_str, cabezal, estado_actual)

        if config in historial:
            print("\n[Abortado] Se detecto un bucle infinito.")
            return False, cinta_str.strip(simbolo_blanco)

        historial.add(config)

        # expandir cinta si el cabezal se va a la derecha
        if cabezal >= len(cinta):
            cinta.append(simbolo_blanco)
        elif cabezal < 0:
            print("\n[Abortado] El cabezal intento salir por la izquierda.")
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
            print(f"\n[Abortado] No hay transicion para estado '{estado_actual}' con simbolo '{simbolo_actual}'.")
            return False, "".join(cinta).strip(simbolo_blanco)

    return True, "".join(cinta).strip(simbolo_blanco)


def ingresar_datos_mt():
    print("="*60)
    print("  SIMULADOR DE MAQUINA DE TURING - INFO 139  ")
    print("="*60)
    print("Ingrese los componentes de la maquina.\n")

    print("[1] ESTADOS")
    print("Ingrese todos los estados separados por espacios (ej: q0 q1 q2 qf):")
    estados = set(input(">> ").strip().split())

    print("\n[2] ESTADO INICIAL")
    while True:
        estado_inicial = input(">> Estado inicial: ").strip()
        if estado_inicial in estados:
            break
        print(f"Error: '{estado_inicial}' no esta en el conjunto de estados.")

    print("\n[3] ESTADOS FINALES")
    while True:
        print("Ingrese los estados de aceptacion separados por espacios (ej: qf):")
        estados_finales = set(input(">> ").strip().split())
        if estados_finales.issubset(estados) and len(estados_finales) > 0:
            break
        print("Error: los estados finales deben pertenecer al conjunto de estados.")

    print("\n[4] ALFABETO DE LA CINTA")
    print("Ingrese los simbolos de la cinta separados por espacios (ej: 0 1 X Y B):")
    alfabeto_cinta = set(input(">> ").strip().split())

    while True:
        simbolo_blanco = input(">> Cual simbolo es el BLANCO? (ej: B): ").strip()
        if simbolo_blanco in alfabeto_cinta:
            break
        print("Error: el simbolo blanco debe estar en el alfabeto de la cinta.")

    print("\n[5] ALFABETO DE ENTRADA")
    while True:
        print(f"Simbolos de entrada separados por espacios (sin incluir el blanco '{simbolo_blanco}'):")
        alfabeto_entrada = set(input(">> ").strip().split())
        if simbolo_blanco not in alfabeto_entrada:
            break
        print("Error: el alfabeto de entrada no puede incluir el simbolo blanco.")

    print("\n[6] TRANSICIONES")
    print("Formato: estado_actual simbolo_leido -> nuevo_estado simbolo_escrito movimiento")
    print("Ejemplo: q0 1 -> q1 X D")
    print("Escriba FIN para terminar.\n")

    transiciones = {}
    for est in estados:
        transiciones[est] = {}

    contador = 1
    while True:
        entrada = input(f"Transicion #{contador}: ").strip()
        if entrada.upper() == "FIN":
            if not any(transiciones[est] for est in estados):
                print("Ingrese al menos una transicion.")
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

            if est_act not in estados or n_est not in estados:
                print("Error: alguno de los estados no existe.")
                continue
            if sim_lei not in alfabeto_cinta or sim_esc not in alfabeto_cinta:
                print("Error: alguno de los simbolos no esta en el alfabeto de la cinta.")
                continue
            if mov not in ["D", "I"]:
                print("Error: el movimiento debe ser D o I.")
                continue

            transiciones[est_act][sim_lei] = (n_est, sim_esc, mov)
            contador += 1

        except ValueError:
            print("Formato incorrecto. Ejemplo: q0 1 -> q1 X D")

    return estado_inicial, estados_finales, transiciones, alfabeto_entrada, simbolo_blanco


def main():
    estado_inicial, estados_finales, transiciones, alfabeto_entrada, simbolo_blanco = ingresar_datos_mt()

    while True:
        print("\n" + "="*60)
        print("  INGRESAR PALABRA  ")
        print("="*60)
        print(f"Simbolos validos: {', '.join(alfabeto_entrada)}")
        print("Escriba SALIR para terminar.")

        palabra = input(">> ").strip()

        if palabra.upper() == "SALIR":
            print("Programa finalizado.")
            sys.exit()

        palabra_valida = True
        for caracter in palabra:
            if caracter not in alfabeto_entrada:
                print(f"Error: el caracter '{caracter}' no pertenece al alfabeto de entrada.")
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
            print("ACEPTADA. La palabra pertenece al lenguaje.")
        else:
            print("RECHAZADA. La palabra no pertenece al lenguaje.")
        print(f"Cinta final: '{cinta_resultante}'")
        print("-" * 40)


if __name__ == "__main__":
    main()
