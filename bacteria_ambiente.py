import numpy as np
import random

class Bacteria:
    def __init__(self, id, raza):
        self.__id = id
        self.__raza = raza
        self.__energia = 10 #0 -> mueren| 25 -> dividen
        self.__resistencia = False
        self.__estado = 'activa' #activa|inactiva
    
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
    
    def alimentar(self, nutrientes):
        #Recibe nutrientes de la matriz de nutrientes
        if nutrientes >= 20:
            while True:
                nutrientes_consumir = random.uniform(20, 25)
                if nutrientes_consumir <= nutrientes:
                    break
            self.__energia += nutrientes_consumir
            nutrientes -= nutrientes_consumir
            #Devuelve los nutrientes restantes a la matriz
            return nutrientes

        elif 0 < nutrientes < 20:
            self.__energia += nutrientes
            #Consume todos los nutrientes, devuelve 0
            return 0
    
    def falta_de_alimento(self):
        self.__energia -= random.uniform(10, 15) #Pierde energia por falta de nutrientes 

    def dividirse(self, id_nueva_bacteria):
        #Dividirse resta 15 de energia
        self.__energia -= 15
        nueva_bacteria = Bacteria(id_nueva_bacteria, self.__raza)
        if self.__resistencia:
            #La bacteria hija heredará resistencia
            nueva_bacteria.set_resistencia(True)
        #Devuelve la bacteria 
        return nueva_bacteria
        
    def mutar(self):
        mutacion = random.random()
        if mutacion <= 0.01:
            self.__energia = 0
            self.__estado = "inactiva"
            self.__resistencia = False
        if mutacion > 0.01 and mutacion <= 0.02:
            self.__resistencia = True
        if mutacion > 0.02 and mutacion <= 0.03:
            energia_extra = random.uniform(1, 5)
            self.__energia += energia_extra
        else:
            pass

    def efecto_factor_ambiental(self, factor_ambiental):
        if factor_ambiental == 'Antibiótico':
            #Si no hay resistencia en la bacteria viva, tiene dos opciones:
            if not self.__resistencia and self.__estado == "activa":
                p = 0.15
                #Muere: 85% probabilidad
                if random.random() > p:
                    self.__estado = 'inactiva'
                    self.__energia = 0
                else:
                    #Genera resistencia al antibiótico: 15% probabilidad
                    self.__resistencia = True

    def morir(self):
        #Muere cuando tiene poca energía
        if self.__energia < 10:
            self.__estado = 'inactiva'
            self.__energia = 0
            return True
    
    def desgaste_x_ciclo(self):
        #Entre ciclos, hay un gasto de energía mínimo
        energia_gastada = random.uniform(1, 5)
        self.__energia -= energia_gastada

        if self.__energia < 10:
            self.__energia = 0
            self.__estado = 'inactiva'

class Ambiente:
    def __init__(self, factor_ambiental):
        self.__grilla = np.zeros((10, 10), dtype=int) #Grilla de numeros -> Es la que se grafica
        self.__grilla_nutrientes = [[50 for i in range(10)] for j in range(10)] #Matriz de nutrientes
        self.__factor_ambiental = factor_ambiental #Nada/Antibiótico
    
    def get_grilla(self):
        return self.__grilla
    
    def set_grilla(self, grilla):
        try:
            if isinstance(grilla, np.ndarray):
                self.__grilla = grilla
            else:
                raise ValueError("La grilla debe ser una lista.")
        except ValueError as e:
            print(f"Error: {e}")

    def get_nutrientes(self):
        return self.__grilla_nutrientes

    def set_nutrientes(self, nutrientes):
        try:
            if isinstance(nutrientes, int):
                self.__nutrientes = nutrientes
            else:
                raise ValueError("Los nutrientes deben ser un numero entero.")
        except ValueError as e:
            print(f"Error: {e}")

    def set_nutrientes_coordenada(self, i, j, nutrientes_restantes):
        self.__grilla_nutrientes[i][j] = nutrientes_restantes

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

    def difundir_nutrientes(self):
        #Suma los nutrientes de la grilla y los redistribuye uniformemente
        total_nutrientes = 0
        for i in range(10):
            for j in range(10):
                total_nutrientes += self.__grilla_nutrientes[i][j]
        nutrientes_x_casilla = total_nutrientes / 100
        for i in range(10):
            for j in range(10):
                self.__grilla_nutrientes[i][j] = nutrientes_x_casilla