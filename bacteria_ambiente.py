import numpy as np

class Bacteria:
    def __init__(self, id, raza):
        self.__id = id
        self.__raza = raza
        self.__energia = 100
        self.__resistencia = False
        self.__estado = 'activa'
    
    def get_id(self):
        return self.__id
    
    def set_id(self, id):
        try:
            if isinstance(id, int):
                self.__id = id
            else:
                raise ValueError("El id debe ser un número entero.")
        except ValueError as e:
            print(f"Error: {e}")
    
    def get_raza(self):
        return self.__raza
    
    def set_raza(self, raza):
        try:
            if isinstance(raza, str):
                self.__raza = raza
            else:
                raise ValueError("La raza debe ser una cadena de texto.")
        except ValueError as e:
            print(f"Error: {e}")
    
    def get_energia(self):
        return self.__energia
    
    def set_energia(self, energia):
        try:
            if isinstance(energia, int):
                self.__energia = energia
            else:
                raise ValueError("La energía debe ser un número entero.")
        except ValueError as e:
            print(f"Error: {e}")
    
    def get_resistencia(self):
        return self.__resistencia
    
    def set_resistencia(self, resistencia):
        try:
            if isinstance(resistencia, bool):
                self.__resistencia = resistencia
            else:
                raise ValueError("La resistencia debe ser un valor booleano.")
        except ValueError as e:
            print(f"Error: {e}")
    
    def get_estado(self):
        return self.__estado

    def set_estado(self, estado):
        try:
            if isinstance(estado, str):
                self.__estado = estado
            else:
                raise ValueError("El estado debe ser una cadena de texto.")
        except ValueError as e:
            print(f"Error: {e}")
    
    def alimentar(self):
        pass

    def dividirse(self):
        
        pass

    def mutar(self):
        pass

    def morir(self):
        pass

class Ambiente:
    def __init__(self, factor_ambiental):
        self.__grilla = np.zeros((10, 10))
        self.__nutrientes = 50
        self.__factor_ambiental = factor_ambiental
    
    def get_grilla(self):
        return self.__grilla
    
    def set_grilla(self):
        try:
            if isinstance(grilla, list):
                self.__grilla = grilla
            else:
                raise ValueError("La grilla debe ser una lista.")
        except ValueError as e:
            print(f"Error: {e}")

    def get_nutrientes(self):
        return self.__nutrientes

    def set_nutrientes(self, nutrientes):
        try:
            if isinstance(nutrientes, int):
                self.__nutrientes = nutrientes
            else:
                raise ValueError("Los nutrientes deben ser un numero entero.")
        except ValueError as e:
            print(f"Error: {e}")

    def get_factor_ambiental(self):
        return self.__factor_ambiental

    def set_factor_ambiental(self, factor_ambiental):
        try:
            if isinstance(factor_ambiental, str):
                self.__factor_ambiental = factor_ambiental
            else:
                raise ValueError("El factor ambiental debe ser un número entero.")
        except ValueError as e:
            print(f"Error: {e}")

    def actualizar_nutrientes(self):
        pass

    def difundir_nutrientes(self):
        pass

    def aplicar_ambiente(self):
        pass