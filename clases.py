import random
'''
========================================================================
                            Clase Detector
========================================================================
'''
class Detector:

    def __init__(self) -> None:
        """
        Inicializa una clase detector para encontrar mutaciones.
        """
        self.tipo_mutacion = ""
        self.fila_inicial = 0
        self.columna_inicial = 0
    
    def detectar_mutantes(self, adn: list[str]) -> bool:
        """
        Busca mutante en el adn, buscando secuencias de al menos 4 bases nitrogenadas iguales
        en direccion vertical, horizaontal o diagonal

        :param adn: Una lista de cadenas que representa la matriz ADN

        :return: True si hay mutaciones, False en caso contrario
        """
        return (self.__detectar_horizontal(adn) or 
                self.__detectar_vertical(adn) or 
                self.__detectar_diagonal(adn))
    

    def __detectar_horizontal(self, adn: list[str]) -> bool:
        
        cantidad_filas = len(adn)
        letras_por_filas = len(adn[0])

        for f in range(cantidad_filas):
            contador = 1 
            for c in range(letras_por_filas - 1) :
            
                letra_columna_actual = adn[f][c]
                letra_columna_siguiente = adn[f][c + 1]

                if letra_columna_actual == letra_columna_siguiente:
                    contador += 1
                    if contador == 4:
                        self.tipo_mutacion = "HORIZONTAL"
                        self.fila_inicial = f
                        self.columna_inicial = c - 2
                        return True
                else:
                    contador = 1
        return False
    

    def __detectar_vertical(self, adn: list[str]) -> bool:
        cantidad_filas = len(adn)
        letras_por_filas = len(adn[0])

        for c in range(letras_por_filas):
            contador = 1 
            for f in range(cantidad_filas - 1) :

                letra_fila_actual = adn[f][c]
                letra_fila_siguiente = adn[f + 1][c]

                if letra_fila_actual == letra_fila_siguiente:
                    contador += 1
                    if contador == 4:
                        self.tipo_mutacion = "VERTICAL"
                        self.fila_inicial = f - 2
                        self.columna_inicial = c
                        return True
                else:
                    contador = 1 
        return False 
    
    
    def __detectar_diagonal(self, adn: list[str]) -> bool:
        cantidad_filas = len(adn)
        letras_por_filas = len(adn[0])
        
        for f in range(cantidad_filas - 3):
            for c in range(letras_por_filas - 3):
                if (adn[f][c] == adn[f + 1][c + 1] and 
                    adn[f][c] == adn[f + 2][c + 2] and
                    adn[f][c] == adn[f + 3][c + 3]):
                        self.columna_inicial = c
                        self.fila_inicial = f
                        self.tipo_mutacion = "DIAGONAL"
                        return True
        
        
        for f in range(cantidad_filas - 3):
            for c in range(3, letras_por_filas):
                if (adn[f][c] == adn[f + 1][c - 1] and 
                    adn[f][c] == adn[f + 2][c - 2] and
                    adn[f][c] == adn[f + 3][c - 3]):
                        self.columna_inicial = c
                        self.fila_inicial = f
                        self.tipo_mutacion = "DIAGONAL"
                        return True
        
        return False


'''
========================================================================
                            Clase Sanador 
========================================================================
'''

class Sanador: 
    
    def __init__(self, detector: Detector) -> None:
        self.detector = detector
        self.adn_infectado = ""

    def sanar_mutantes(self, adn: list[str]) -> list[str]:
        base_nitrogenadas = ["A", "G", "C", "T"]
        adn_sano = []
        fila_adn = ""

        if self.detector.detectar_mutantes(adn):
            while True:
                adn_sano = []
        
                for _ in range(len(adn)):
                    fila_adn = ""
                    for _ in range(len(adn[0])):
                        fila_adn += random.choice(base_nitrogenadas)
                
                    adn_sano.append(fila_adn)
                    
                if not self.detector.detectar_mutantes(adn_sano):
                    return adn_sano
                    
        else: 
            return adn
        
        
'''
========================================================================
                            SuperClase Mutador
========================================================================
'''

class Mutador:
    def __init__(self, base_nitrogenada: str, adn: list[str]) -> None:
        self.adn = adn 
        self.base_nitrogenada = base_nitrogenada
        self.tipo_mutacion = ""

    def crear_mutante(self,base_nitrogenada: str, posicion_inicial: int, orientacion_de_la_mutacion: str = None):
        pass

'''
========================================================================
                            Clase Radiacion (hija)
========================================================================
'''  

class Radiacion(Mutador):
    def __init__(self, base_nitrogenada: str, adn: list[str]) -> None:
        super().__init__(base_nitrogenada, adn)

    def crear_mutante(self, base_nitrogenada: str, posicion_inicial: tuple[int, int], orientacion_de_la_mutacion: str) -> list[str]:
        try:
            fila, columna = posicion_inicial

            # Convertir la matriz a una lista de listas
            adn = [list(fila_adn) for fila_adn in self.adn]

            if orientacion_de_la_mutacion == "H":
                self.tipo_mutacion = "HORIZONTAL"
                if 0 <= columna <= len(adn[fila]) - 4:  # Mutación hacia la derecha
                    for i in range(4):
                        adn[fila][columna + i] = base_nitrogenada
                elif 3 <= columna < len(adn[fila]):  # Mutación hacia la izquierda
                    for i in range(4):
                        adn[fila][columna - i] = base_nitrogenada
                else:
                    raise IndexError("La mutación excede los límites de la matriz horizontalmente.")

            elif orientacion_de_la_mutacion == "V":
                self.tipo_mutacion= "VERTICAL"
                if 0 <= fila <= len(adn) - 4:  # Mutación hacia abajo
                    for i in range(4):
                        adn[fila + i][columna] = base_nitrogenada
                elif 3 <= fila < len(adn):  # Mutación hacia arriba
                    for i in range(4):
                        adn[fila - i][columna] = base_nitrogenada
                else:
                    raise IndexError("La mutación excede los límites de la matriz verticalmente.")

            else:
                raise ValueError("Solo se aceptan las orientaciones 'H' (horizontal) o 'V' (vertical).")

            # Convertir la matriz a lista de cadenas y retornar
            self.adn = ["".join(fila_adn) for fila_adn in adn]
            return self.adn

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None  # Manejo seguro: devuelve None si falla



'''
========================================================================    
                            Clase Virus (hija)
========================================================================
''' 

class Virus(Mutador):
    def __init__(self, base_nitrogenada: str, adn: list[str]) -> None:
        super().__init__(base_nitrogenada, adn)
        self.tipo_mutacion = "Diagonal"
        
    def crear_mutante(self, base_nitrogenada: str, posicion_inicial: tuple[int, int]) -> list[str]:
        try:
            fila, columna = posicion_inicial
            
            adn = [list(fila_adn) for fila_adn in self.adn]
            
            if fila + 3 < len(adn) and columna + 3 < len(adn[0]):
                for i in range(4):
                    adn[fila + i][columna + i] = base_nitrogenada
            
            elif fila - 3 >= 0 and columna - 3 >= 0:
                for i in range(4):
                    adn[fila - i][columna - i] = base_nitrogenada
            
            elif fila + 3 < len(adn) and columna - 3 >= 0:
                for i in range(4):
                    adn[fila + i][columna - i] = base_nitrogenada
            
            elif fila - 3 >= 0 and columna + 3 < len(adn[0]):
                for i in range(4):
                    adn[fila - i][columna + i] = base_nitrogenada
            
            else:
                raise Exception("La posición inicial y la longitud de la mutación exceden los límites de la matriz diagonalmente")
            
            self.adn = ["".join(fila_adn) for fila_adn in adn]

            return self.adn
        
        except Exception as e:
            print(f"Ocurrió un error: {e}")