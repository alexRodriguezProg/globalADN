import random
from clases import Detector, Sanador, Radiacion, Virus

def main() -> None:
    # Crear una instancia de Detector
    detector = Detector()

    # Crear una instancia de Sanador y pasar el detector
    sanador = Sanador(detector)

    
    
    print("<--- CREACION DE MATRIZ -->")

    matriz_adn = []

    print("\n¿COMO DESEA GENERAR LA MATRIZ ADN?: ")
    opc_creacion = int(input("1) TECLADO \n2) ALEATORIA\n\n"))

    match opc_creacion:
        case 1:
            for i in range(6):
                cadena_adn = input(f"INGRESE LA CADENA DE ADN N°{i+1} -> (Las letras deben ser las siguientes: A, G, C, T): ")

                matriz_adn.append(cadena_adn)
        case 2:
            matriz_adn = generar_matriz_aleatoria()
        case _: 
            print("LA OPCION INGRESADA NO ES VALIDA")

    print("\n<--- MATRIZ INGRESADA -->\n")
    imprimir_matriz_adn(adn = matriz_adn)


    print("\nELIGA QUE OPCIONES DESEA REALIAZAR CON LA CADENA DE ADN INTRODUCIDO: ")
    opciones = int(input("1) MUTAR \n2) SANAR \n3) DETECTAR\n\n"))

    match opciones:
        case 1:
            fila = int(input("\nINGRESE LA FILA DONDE DESEA QUE EMPIECE LA MUTACION: "))
            columna = int(input("INGRESE LA COLUMNA DONDE DESEA QUE EMPIECE LA MUTACION: "))
            base_nitro = input("INGRESE LA BASE NITROGENADA: (A) (C) (G) (T): ")

            posicion_inicial = (fila,columna)
            
            radiacion = Radiacion(base_nitro, matriz_adn)
            virus = Virus(base_nitro, matriz_adn)

            print("\nQUE TIPO DE MUTACION DESEA REALIZAR: ")
            opc_mutaciones = int(input("1) RADIACION \n2) VIRUS\n\n "))

            match opc_mutaciones:
                case 1:
                    print("\nQUE TIPO DE RADIACION DESEA REALIZAR: ") 
                    orientacion = input("1) H (HORIZONTAL) \n2) V (VERTICAL)\n\n ")
                    mutacion_radiacion = radiacion.crear_mutante(base_nitro, posicion_inicial, orientacion)
                    
                    print(f"\n<--- RADIACION {radiacion.tipo_mutacion} -->\n")

                    imprimir_matriz_adn(mutacion_radiacion)
                case 2:
                    mutacion_virus = virus.crear_mutante(base_nitro, posicion_inicial)

                    print("\n<--- RADIACION DIAGONAL -->\n")
                    imprimir_matriz_adn(mutacion_virus) 
                case _: 
                    print("LA OPCION INGRESADA NO ES VALIDA")

        case 2:
            print("\n<--- ADN SANADO -->\n")
            adn_sano = sanador.sanar_mutantes(matriz_adn)
            imprimir_matriz_adn(adn_sano)

        case 3:
            detectado = detector.detectar_mutantes(matriz_adn)

            if detectado == True:
                print(f"SE DETECTO UN ADN MUTADO {detector.tipo_mutacion} EN LA FILA {detector.fila_inicial} Y COLUMNA {detector.columna_inicial}")
            else:
                print("NO SE DETECTO MUTACION DE NINGUN TIPO")

        case _: 
            print("LA OPCION INGRESADA NO ES VALIDA")


def imprimir_matriz_adn(adn: list[str]) -> None:
    """
    Imprime la matriz ADN en formato fila por fila

    :param adn: Una lista de cadenas que representa la matriz ADN
    """
    for fila in adn:
        print(fila)

def generar_matriz_aleatoria() -> list[str]:
    """
    """
    matriz_aleatoria = []
    base_nitrogenadas = ["A", "G", "C", "T"]
    fila_adn = ""
            
    for _ in range(6):
        fila_adn = ""
        for _ in range(6):
            fila_adn += random.choice(base_nitrogenadas)
                    
        matriz_aleatoria.append(fila_adn)
    
    return matriz_aleatoria


if __name__ == "__main__":
    main()
