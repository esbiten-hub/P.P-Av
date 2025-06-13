import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

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
        self.__grilla = set_grilla()
        self.__nutrientes = 50
        self.__factor_ambiental = factor_ambiental
    
    def get_grilla(self):
        return self.__grilla
    
    def set_grilla(self):

        #Crea una grilla 50x50
        grilla = np.zeros((50, 50))

        #Crea mapa de colores con 5 categorías
        cmap = plt.cm.get_cmap('Set1', 5)

        fig, ax = plt.subplots(figsize=(6,6))
        cax = ax.matshow(grilla, cmap=cmap)

        #Agrega leyenda
        legend_elements = [
            Patch(facecolor = cmap (1/5), label = 'Bacteria activa'),
            Patch(facecolor = cmap (2/5), label = 'Bacteria muerta'),
            Patch(facecolor = cmap (3/5), label = 'Bacteria resistente'),
            Patch(facecolor = cmap (4/5), label = 'Biofilm'),
        ]

        ax.legend(handless = legend_elements, loc = 'upper right', bbox_to_anchor =  (1.45, 1))

        #Configuracion de la grilla
        ax.set_xticks(np.arange(0, 50, 1))
        ax.set_yticks(np.arange(0, 50, 1))
        ax.set_xticklabels([])
        ax.set_ytickslabels([])
        ax.grid(color = 'gray', linestyle = '-', linewidth = 0.5)

        for i in range(50):
            for j in range(50):
                val = grilla [i, j]
                if val > 0:
                    ax.text(j, i, int(val), va = 'center', ha = 'center', color = 'white')

        plt.title("Colonia de bacterias")
        plt.tight_layout()
        plt.show()

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