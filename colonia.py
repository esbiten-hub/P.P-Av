import matplotlib.pyplot as plt
import random, io
import numpy as np
from PIL import Image
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
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
            grilla[0,0,0] = 1
            #grilla[0,0,0] = self.get_bacterias()[0].get_id()
            #grilla[0,0,0] = self.get_bacterias()[0].get_estado()
            ocupado.append([0,0])
            for bacteria in self.get_bacterias()[1:]:
                while True:
                    x1, y1 = random.choice(ocupado)
                    x2, y2 = random.choice(direcciones_posibles)
                    nueva_posicion = [x1 + x2, y1 + y2]
                    if nueva_posicion[0] < 0 or nueva_posicion[0] > 9 or nueva_posicion[1] < 0 or nueva_posicion[1] > 9:
                        pass
                    elif grilla[nueva_posicion[0], nueva_posicion[1], 0] != 0:
                        pass
                    else:
                        #grilla[nueva_posicion[0], nueva_posicion[1], 0] = bacteria.get_id()
                        grilla[nueva_posicion[0], nueva_posicion[1], 0] = 1
                        #grilla[nueva_posicion[0], nueva_posicion[1], 0] = bacteria.get_estado()
                        ocupado.append(nueva_posicion)
                        break
            
            #Extrae capa de bacterias
            bacterias = grilla[:,:,0]
            #Crear el mapa de colores
            colores = ['#e41a1c', '#4daf4a', '#ff7f00', '#a65628', '#999999']
            cmap = ListedColormap(colores)
            fig, ax = plt.subplots(figsize=(6,6))
            cax = ax.imshow(bacterias, cmap=cmap, vmin=0, vmax=4)

            #Agrega leyenda
            legend_elements = [
                Patch(facecolor='#4daf4a', label='Bacteria activa'),
                Patch(facecolor='#ff7f00', label='Bacteria muerta'),
                Patch(facecolor='#a65628', label='Bacteria resistente'),
                Patch(facecolor='#999999', label='Biofilm'),
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
                    val = grilla[i,j,0]
                    if val > 0:
                        ax.text(j, i, int(val), va='center', ha='center', color='white')
            plt.title("Colonia de bacterias - Paso 1")
            plt.tight_layout()

            #################################################################
            #Aqui deberia salir un CSV con el estado inicial de las bacterias
            #################################################################

            #Guardar la imagen
            fig_bytes = io.BytesIO()
            fig.savefig(fig_bytes, format='png')
            plt.close(fig)
            fig_bytes.seek(0)

            return fig_bytes

        #Si no es el primer paso, se actualiza la grilla según sea el caso
        else:
            grilla = self.get_ambiente().get_grilla()
            for i in range(10):
                for j in range(10):
                    pass
                        
            
            
                
    def reporte_estado(self):
        pass

    def exportar_csv(self):
        pass