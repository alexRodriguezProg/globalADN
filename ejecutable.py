import random
from clases import Detector, Sanador, Radiacion, Virus


def crear_matriz_adn() -> list[str]:
    """
    Permite crear una matriz ADN ingresándola manualmente o generándola aleatoriamente.

    :return: Lista de cadenas que representan la matriz ADN.
    """

    print("<--- CREACION DE MATRIZ -->")
    matriz_adn = []

    while True:
        print("\n¿COMO DESEA GENERAR LA MATRIZ ADN?: ")
        opc_creacion = int(input("1) TECLADO \n2) ALEATORIA\n\n"))

        match opc_creacion:
            case 1:
                matriz_adn = generar_matriz_teclado()
                break
            case 2:
                matriz_adn = generar_matriz_aleatoria()
                break
            case _:
                print("LA OPCION INGRESADA NO ES VALIDA")
    
    return matriz_adn


def mutar_adn(matriz_adn: list[str]) -> list[str]:
    """
    Realiza una mutación en la matriz ADN mediante radiación o virus.

    :param matriz_adn: Lista de cadenas que representan la matriz ADN.
    :return: Matriz ADN mutada.
    """
    caracteres_validos = {"A", "C", "G", "T"}

    while True:
        try:
            fila = int(input("\nINGRESE LA FILA DONDE DESEA QUE EMPIECE LA MUTACION (0-5): "))
            if 0 <= fila < 6:
                break
            else:
                print("LA FILA DEBE ESTAR ENTRE 0 Y 5d")
        except ValueError:
            print("DEBE INGRESAR UN NÚMERO ENTERO ENTRE 0 Y 5.")

    while True:
        try:
            columna = int(input("INGRESE LA COLUMNA DONDE DESEA QUE EMPIECE LA MUTACION (0-5): "))
            if 0 <= columna < 6:
                break
            else:
                print("LA COLUMNA DEBE ESTAR ENTRE 0 Y 5.")
        except ValueError:
            print("DEBE INGRESAR UN NÚMERO ENTERO ENTRE 0 Y 5.")

    while True:
        base_nitro = input("INGRESE LA BASE NITROGENADA (A, C, G, T): ").upper()
        if base_nitro in caracteres_validos:
            break
        else:
            print("BASE NITROGENADA INVÁLIDA. DEBE SER UNA DE LAS SIGUIENTES: A, C, G, T.")

    posicion_inicial = (fila, columna)

    print("\nQUE TIPO DE MUTACION DESEA REALIZAR: ")
    opc_mutaciones = int(input("1) RADIACION \n2) VIRUS\n\n"))

    match opc_mutaciones:
        case 1:
            return mutacion_radiacion(matriz_adn, posicion_inicial, base_nitro)
        case 2:
            return mutacion_virus(matriz_adn, posicion_inicial, base_nitro)
        case _:
            print("LA OPCION INGRESADA NO ES VALIDA")
            return matriz_adn

def mutacion_radiacion(matriz_adn: list[str], posicion_inicial: tuple[int, int], base_nitro: str) -> list[str]:
    """
    Realiza una mutación por radiación en la matriz ADN.

    :param matriz_adn: Lista de cadenas que representan la matriz ADN.
    :param posicion_inicial: Coordenadas (fila, columna) donde inicia la mutación.
    :param base_nitro: Base nitrogenada utilizada en la mutación.
    :return: Matriz ADN mutada por radiación.
    """
    radiacion = Radiacion(base_nitro, matriz_adn)

    while True:
        orientacion = input("1) H (HORIZONTAL) \n2) V (VERTICAL)\n\n").upper()
        if orientacion in {"H", "V"}:
            break
        else:
            print("ORIENTACIÓN INVÁLIDA. SOLO SE ACEPTAN: H (HORIZONTAL) O V (VERTICAL).")

    mutacion_radiacion = radiacion.crear_mutante(base_nitro, posicion_inicial, orientacion)

    print(f"\n<--- RADIACION {radiacion.tipo_mutacion} -->\n")
    imprimir_matriz_adn(mutacion_radiacion)
    return mutacion_radiacion


def mutacion_virus(matriz_adn: list[str], posicion_inicial: tuple[int, int], base_nitro: str) -> list[str]:
    """
    Realiza una mutación por virus en la matriz ADN.

    :param matriz_adn: Lista de cadenas que representan la matriz ADN.
    :param posicion_inicial: Coordenadas (fila, columna) donde inicia la mutación.
    :param base_nitro: Base nitrogenada utilizada en la mutación.
    :return: Matriz ADN mutada por virus.
    """
    virus = Virus(base_nitro, matriz_adn)
    mutacion_virus = virus.crear_mutante(base_nitro, posicion_inicial)

    print("\n<--- MUTACION DIAGONAL -->\n")
    imprimir_matriz_adn(mutacion_virus)
    return mutacion_virus

def sanar_adn(sanador: Sanador, matriz_adn: list[str]) -> list[str]:
    """
    Sana los mutantes presentes en la matriz ADN.

    :param sanador: Instancia de la clase Sanador.
    :param matriz_adn: Lista de cadenas que representan la matriz ADN.
    :return: Matriz ADN saneada.
    """
    print("\n<--- ADN SANADO -->\n")
    adn_sano = sanador.sanar_mutantes(matriz_adn)
    imprimir_matriz_adn(adn_sano)
    return adn_sano


def detectar_adn(detector: Detector, matriz_adn: list[str]) -> None:
    """
    Detecta mutaciones en la matriz ADN.

    :param detector: Instancia de la clase Detector.
    :param matriz_adn: Lista de cadenas que representan la matriz ADN.
    """
    detectado = detector.detectar_mutantes(matriz_adn)

    if detectado:
        print(
            f"SE DETECTO UN ADN MUTADO {detector.tipo_mutacion} EN LA FILA {detector.fila_inicial} Y COLUMNA {detector.columna_inicial}")
    else:
        print("NO SE DETECTO MUTACION DE NINGUN TIPO")


def imprimir_matriz_adn(adn: list[str]) -> None:
    """
    Imprime la matriz ADN en formato fila por fila.

    :param adn: Lista de cadenas que representan la matriz ADN.
    """
    for fila in adn:
        print(fila)


def generar_matriz_aleatoria() -> list[str]:
    """
    Genera una matriz ADN aleatoria de 6x6 con bases nitrogenadas válidas (A, G, C, T).

    :return: Lista de cadenas que representan la matriz ADN generada aleatoriamente.
    """
    matriz_aleatoria = []
    base_nitrogenadas = ["A", "G", "C", "T"]

    for _ in range(6):
        fila_adn = "".join(random.choice(base_nitrogenadas) for _ in range(6))
        matriz_aleatoria.append(fila_adn)

    return matriz_aleatoria

def generar_matriz_teclado() -> list[str]:
    """
    Genera una matriz ADN de 6x6 ingresada manualmente por el usuario, 
    validando que cada cadena tenga 6 caracteres y solo contenga A, C, G, T.

    :return: Lista de cadenas que representan la matriz ADN ingresada por teclado.
    """
    matriz_teclado = []
    caracteres_validos = {"A", "C", "G", "T"}

    for i in range(6):
        while True:
            cadena_adn = input(f"INGRESE LA CADENA DE ADN N°{i+1} -> (Debe contener 6 caracteres: A, G, C, T): ").upper()

            if len(cadena_adn) == 6 and set(cadena_adn).issubset(caracteres_validos):
                matriz_teclado.append(cadena_adn)
                break
            else:
                print("CADENA INVÁLIDA. ASEGÚRESE DE INGRESAR EXACTAMENTE 6 CARACTERES Y SOLO USAR: A, G, C, T.")
    
    return matriz_teclado


def main() -> None:
    """
    Función principal del programa. Permite al usuario realizar diversas operaciones sobre una matriz ADN.
    """
    detector = Detector()
    sanador = Sanador(detector)

    matriz_adn = crear_matriz_adn()

    print("\n<--- MATRIZ INGRESADA -->\n")
    imprimir_matriz_adn(matriz_adn)

    while True:
        print("\nELIGA QUE OPCIONES DESEA REALIZAR CON LA CADENA DE ADN INTRODUCIDO: ")
        opciones = int(input("1) MUTAR \n2) SANAR \n3) DETECTAR \n4) MOSTRAR ADN \n5) SALIR\n\n"))

        match opciones:
            case 1:
                matriz_adn = mutar_adn(matriz_adn)
            case 2:
                matriz_adn = sanar_adn(sanador, matriz_adn)
            case 3:
                detectar_adn(detector, matriz_adn)
            case 4:
                imprimir_matriz_adn(matriz_adn)
            case 5:
                print("SALIENDO...")
                break
            case _:
                print("LA OPCION INGRESADA NO ES VALIDA")


if __name__ == "__main__":
    main()

