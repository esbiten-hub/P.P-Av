import matplotlib.pyplot as plt
import random, io
import numpy as np
from PIL import Image
from matplotlib.patches import Patch
from bacteria_ambiente import Bacteria, Ambiente

class Colonia:
    def __init__(self, bacterias, ambiente):
        self.__bacterias = bacterias #list de Class Bacteria
        self.__ambiente = ambiente #Class Ambiente
    
    def get_bacterias(self):
        return self.__bacterias

    def set_bacterias(self, bacterias):
        try:
            if isinstance(bacterias, list):
                self.__bacterias = bacterias
            else:
                raise ValueError("Las bacterias deben ser una lista de bacterias.")
        except ValueError as e:
            print(f"Error: {e}")
    
    def get_ambiente(self):
        return self.__ambiente

    def set_ambiente(self, ambiente):
        try:
            if isinstance(ambiente, Ambiente):
                self.__ambiente = ambiente
            else:
                raise ValueError("El ambiente debe ser una instancia de Ambiente.")
        except ValueError as e:
            print(f"Error: {e}")

    def paso(self, paso_contador):
        grilla = self.get_ambiente().get_grilla()

        #Si es el primer paso, se colocan las bacterias
        if paso_contador == 0:
            ocupado = []
            direcciones_posibles = [[-1,0], [1,0], [0,-1], [0,1]]
            #grilla[0,0] = self.get_bacterias()[0].get_id()
            grilla[0,0] = 1
            ocupado.append([0,0])
            for bacteria in self.get_bacterias()[1:]:
                while True:
                    x1, y1 = random.choice(ocupado)
                    x2, y2 = random.choice(direcciones_posibles)
                    nueva_posicion = [x1 + x2, y1 + y2]
                    if nueva_posicion[0] < 0 or nueva_posicion[0] > 9 or nueva_posicion[1] < 0 or nueva_posicion[1] > 9:
                        pass
                    else:
                        grilla[nueva_posicion[0], nueva_posicion[1]] = 1
                        #grilla[nueva_posicion[0], nueva_posicion[1]] = bacteria.get_id()
                        ocupado.append(nueva_posicion)
                        break
            
            #Crear el mapa de colores
            cmap = plt.cm.get_cmap('Set1', 5)
            fig, ax = plt.subplots(figsize=(6,6))
            cax = ax.matshow(grilla, cmap=cmap)

            #Agrega leyenda
            legend_elements = [
                Patch(facecolor = cmap (1/5) , label ='Bacteria activa'),
                Patch(facecolor = cmap (2/5) , label ='Bacteria muerta'),
                Patch(facecolor = cmap (3/5) , label ='Bacteria resistente'),
                Patch(facecolor = cmap (4/5) , label ='Biofilm'),
            ]

            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.45, 1))
            
            #Configuracion de la grilla
            ax.set_xticks(np.arange(0, 10, 1))
            ax.set_yticks(np.arange (0 ,10, 1))
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.grid(color ='gray',linestyle='-', linewidth =0.5)

            #Mostrar valores en cada celdda
            for i in range(10):
                for j in range(10):
                    val = grilla[i,j]
                    if val > 0:
                        ax.text(j, i, int(val), va='center', ha='center', color='white')
            plt.title("Colonia de bacterias - Paso 1")
            plt.tight_layout()

            #Guardar la imagen
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            plt.close(fig)
            buf.seek(0)

            return buf

        #Si no es el primer paso, se actualiza la grilla según sea el caso

            
                
    def reporte_estado(self):
        pass

    def exportar_csv(self):
        pass