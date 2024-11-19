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
        return (self._detectar_horizontal(adn) or 
                self._detectar_vertical(adn) or 
                self._detectar_diagonal(adn))
    

    def _detectar_horizontal(self, adn: list[str]) -> bool:
        
        """
        Verifica si existen secuencias mutantes en dirección horizontal en la matriz ADN.

        :param adn: Lista de cadenas que representa la matriz ADN.
        :return: True si se encuentra una mutación horizontal, False en caso contrario.
        """
        
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
    

    def _detectar_vertical(self, adn: list[str]) -> bool:

        """
        Verifica si existen secuencias mutantes en dirección vertical en la matriz ADN.

        :param adn: Lista de cadenas que representa la matriz ADN.
        :return: True si se encuentra una mutación vertical, False en caso contrario.
        """
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
    
    
    def _detectar_diagonal(self, adn: list[str]) -> bool:

        """
        Verifica si existen secuencias mutantes en dirección diagonal o diagonal inversa
        en la matriz ADN.

        :param adn: Lista de cadenas que representa la matriz ADN.
        :return: True si se encuentra una mutación diagonal o diagonal inversa, False en caso contrario.
        """
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
                        self.tipo_mutacion = "DIAGONAL INVERSA"
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
        """
        Genera un nuevo ADN sano reemplazando al existente si se detectan mutantes.
        Itera generando matrices ADN aleatorias hasta que ninguna contenga mutaciones.

        :param adn: Matriz ADN representada como lista de cadenas.
        :return: Nueva matriz ADN sin mutaciones.
        """
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
        
        """
        Crea un mutante en la matriz ADN según la orientación especificada.

        :param base_nitrogenada: Base nitrogenada para realizar la mutación.
        :param posicion_inicial: Coordenadas (fila, columna) de inicio de la mutación.
        :param orientacion_de_la_mutacion: Orientación de la mutación ('H' o 'V').
        :return: Matriz ADN mutada como lista de cadenas.
        """
        try:
            fila, columna = posicion_inicial
        
            adn = [list(fila_adn) for fila_adn in self.adn]

            if orientacion_de_la_mutacion == "H":
                adn = self._mutacion_horizontal(adn, base_nitrogenada, fila, columna)
            elif orientacion_de_la_mutacion == "V":
                adn = self._mutacion_vertical(adn, base_nitrogenada, fila, columna)
            else:
                raise ValueError("Solo se aceptan las orientaciones 'H' (horizontal) o 'V' (vertical).")

            self.adn = ["".join(fila_adn) for fila_adn in adn]
            return self.adn

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return None  
        
    def _mutacion_horizontal(self, adn: list[list[str]], base_nitrogenada: str, fila: int, columna: int) -> list[list[str]]:
        """
        Realiza una mutación horizontal en la matriz ADN.

        :param adn: Matriz ADN como lista de listas.
        :param base_nitrogenada: Base nitrogenada para realizar la mutación.
        :param fila: Fila inicial de la mutación.
        :param columna: Columna inicial de la mutación.
        :return: Matriz ADN mutada.
        """
        if 0 <= columna <= len(adn[fila]) - 4:  
            for i in range(4):
                adn[fila][columna + i] = base_nitrogenada
            self.tipo_mutacion = "HORIZONTAL (DERECHA)"
        elif 3 <= columna < len(adn[fila]):  
            for i in range(4):
                adn[fila][columna - i] = base_nitrogenada
            self.tipo_mutacion = "HORIZONTAL (IZQUIERDA)"
        else:
            raise IndexError("La mutación excede los límites de la matriz horizontalmente.")
        return adn

    def _mutacion_vertical(self, adn: list[list[str]], base_nitrogenada: str, fila: int, columna: int) -> list[list[str]]:
        """
        Realiza una mutación vertical en la matriz ADN.

        :param adn: Matriz ADN como lista de listas.
        :param base_nitrogenada: Base nitrogenada para realizar la mutación.
        :param fila: Fila inicial de la mutación.
        :param columna: Columna inicial de la mutación.
        :return: Matriz ADN mutada.
        """
        if 0 <= fila <= len(adn) - 4: 
            for i in range(4):
                adn[fila + i][columna] = base_nitrogenada
            self.tipo_mutacion = "VERTICAL (ABAJO)"
        elif 3 <= fila < len(adn):  
            for i in range(4):
                adn[fila - i][columna] = base_nitrogenada
            self.tipo_mutacion = "VERTICAL (ARRIBA)"
        else:
            raise IndexError("La mutación excede los límites de la matriz verticalmente.")
        return adn


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
        """
        Realiza una mutación diagonal en la matriz ADN.

        :param base_nitrogenada: Base nitrogenada para realizar la mutación.
        :param posicion_inicial: Coordenadas (fila, columna) de inicio de la mutación.
        :return: Matriz ADN mutada como lista de cadenas.
        """
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
            return None