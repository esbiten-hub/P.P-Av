import matplotlib.pyplot as plt
import random, io
import numpy as np
from PIL import Image
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
from bacteria_ambiente import Bacteria, Ambiente

class Colonia:
    def __init__(self, bacterias, ambiente):
        self.__bacterias = bacterias #list de Bacterias
        self.__ambiente = ambiente #Ambiente
        self.__matriz_bacteriana = None
    
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
        #Si es el primer paso, se colocan las bacterias
        if paso_contador == 0:

            #Direcciones posibles para bacterias
            ocupado = []
            direcciones_posibles = [[-1,0], [1,0], [0,-1], [0,1], [-1,-1], [-1,1], [1,-1], [1,1]]

            #Crea la matriz de Objetos Bacteria
            matriz = [[0 for i in range(10)] for j in range(10)]
            matriz[0][0] = self.get_bacterias()[0]
            ocupado.append([0,0])
            for bacteria in self.get_bacterias()[1:]:
                while True:
                    x1, y1 = random.choice(ocupado)
                    x2, y2 = random.choice(direcciones_posibles)
                    nueva_posicion = [x1 + x2, y1 + y2]
                    if nueva_posicion[0] < 0 or nueva_posicion[0] > 9 or nueva_posicion[1] < 0 or nueva_posicion[1] > 9:
                        pass
                    elif matriz[nueva_posicion[0]][nueva_posicion[1]] != 0:
                        pass
                    else:
                        matriz[nueva_posicion[0]][nueva_posicion[1]] = bacteria
                        ocupado.append(nueva_posicion)
                        break
            
            #Añade factor ambiental a la matriz
            factor_ambiental = self.get_ambiente().get_factor_ambiental()
            if factor_ambiental == 'Antibiótico': #Añade antibiotico a 5 casillas aleatorias de la matriz
                for i in range(5):
                    while True:
                        x = random.randint(0, 9)
                        y = random.randint(0, 9)
                        if matriz[x][y] == 0:
                            matriz[x][y] = factor_ambiental
                            break

            self.__matriz_bacteriana = matriz

            #Obtiene la matriz numpy de Ambiente
            grilla = self.get_ambiente().get_grilla()
            for i in range(10):
                for j in range(10):
                    if isinstance(matriz[i][j], Bacteria):
                        grilla[i,j] = 1
                    elif matriz[i][j] == factor_ambiental:
                        grilla[i,j] = 4

            #Grafica grilla
            #Crear el mapa de colores
            colores = ['#e41a1c', '#4daf4a', '#ff7f00', '#a65628', '#1f77b4','#999999']
            cmap = ListedColormap(colores)
            fig, ax = plt.subplots(figsize=(6,6))
            cax = ax.imshow(grilla, cmap=cmap, vmin=0, vmax=5)

            #Agrega leyenda
            legend_elements = [
                Patch(facecolor='#4daf4a', label='Bacteria activa'),
                Patch(facecolor='#ff7f00', label='Bacteria muerta'),
                Patch(facecolor='#a65628', label='Bacteria resistente'),
                Patch(facecolor='#1f77b4', label='Antibiótico'),
                Patch(facecolor='#999999', label='Biofilm')
            ]

            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.45, 1))
            
            #Configuracion de la grilla
            ax.set_xticks(np.arange(0, 10, 1))
            ax.set_yticks(np.arange (0 ,10, 1))
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.grid(color ='gray',linestyle='-', linewidth =0.5)

            #Mostrar valores en cada celda
            for i in range(10):
                for j in range(10):
                    val = grilla[i,j]
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
            matriz = self.__matriz_bacteriana
            factor_ambiental = self.get_ambiente().get_factor_ambiental()
            for i in range(10):
                for j in range(10):

                    #Efecto de factor ambiental
                    if isinstance(matriz[i][j], str):
                        if matriz[i][j] == 'Antibiótico':
                            ubicaciones_posibles = [i-1,j], [i+1,j], [i,j-1], [i,j+1], [i-1,j-1], [i-1,j+1], [i+1,j-1], [i+1,j+1]
                            for ubicacion in ubicaciones_posibles:
                                if ubicacion[0] < 0 or ubicacion[0] > 9 or ubicacion[1] < 0 or ubicacion[1] > 9:
                                    pass
                                elif isinstance(matriz[ubicacion[0]][ubicacion[1]], Bacteria):
                                    matriz[ubicacion[0]][ubicacion[1]].efecto_factor_ambiental(factor_ambiental)

                    #Accion de bacterias activas
                    elif isinstance(matriz[i][j], Bacteria):
                        bacteria = matriz[i][j]
                        if bacteria.get_estado() == "activa":
                            if bacteria.get_energia() < 25:
                                nutrientes = self.get_ambiente().get_nutrientes()[i][j]
                                if nutrientes > 0:
                                    nutrientes_restantes = bacteria.alimentar(nutrientes)                                    
                                    self.get_ambiente().set_nutrientes_coordenada(i, j, nutrientes_restantes)
                                    self.get_ambiente().difundir_nutrientes()
                                else:
                                    bacteria.falta_de_alimento()

                            if bacteria.get_energia() >= 25:
                                #Reunir coordenadas hacia donde podría dividirse la bacteria
                                ubicaciones_posibles = [i-1,j], [i+1,j], [i,j-1], [i,j+1], [i-1,j-1], [i-1,j+1], [i+1,j-1], [i+1,j+1]
                                #Filtrar ubicaciones
                                ubicaciones_validas = []
                                for ubicacion in ubicaciones_posibles:
                                    if ubicacion[0] < 0 or ubicacion[0] > 9 or ubicacion[1] < 0 or ubicacion[1] > 9:
                                        pass
                                    elif isinstance(matriz[ubicacion[0]][ubicacion[1]], Bacteria):
                                        pass
                                    elif isinstance(matriz[ubicacion[0]][ubicacion[1]], str): #en caso de que haya factor ambiental
                                        pass
                                    else:
                                        ubicaciones_validas.append(ubicacion)
                                if len(ubicaciones_validas) > 0:
                                    x, y = random.choice(ubicaciones_validas)
                                    id_nueva_bacteria = self.get_bacterias()[-1].get_id() + 1
                                    nueva_bacteria = bacteria.dividirse(id_nueva_bacteria)
                                    self.__bacterias.append(nueva_bacteria)
                                    matriz[x][y] = nueva_bacteria
                                    self.get_ambiente().get_grilla()[x][y] = 1

                            if bacteria.morir():
                                self.get_ambiente().get_grilla()[i][j] = 2
                            bacteria.desgaste_x_ciclo()

            #Actualizar valores de grilla numpy
            grilla = self.get_ambiente().get_grilla()
            for i in range(10):
                for j in range(10):
                    if isinstance(matriz[i][j], Bacteria):
                        bacteria = matriz[i][j]
                        if bacteria.get_estado() == "inactiva":
                            self.get_ambiente().get_grilla()[i][j] = 2
                        if bacteria.get_resistencia():
                            self.get_ambiente().get_grilla()[i][j] = 3

            #Grafica grilla
            grilla = self.get_ambiente().get_grilla()
            #Crear el mapa de colores
            colores = ['#e41a1c', '#4daf4a', '#ff7f00', '#a65628', '#1f77b4', '#999999']
            cmap = ListedColormap(colores)
            fig, ax = plt.subplots(figsize=(6,6))

            #Agrega leyenda
            cax = ax.imshow(grilla, cmap=cmap, vmin=0, vmax=5)
            legend_elements = [
                Patch(facecolor='#4daf4a', label='Bacteria activa'),
                Patch(facecolor='#ff7f00', label='Bacteria muerta'),
                Patch(facecolor='#a65628', label='Bacteria resistente'),
                Patch(facecolor='#1f77b4', label='Antibiótico'),
                Patch(facecolor='#999999', label='Biofilm')
            ]

            ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.45, 1))
            
            #Configuracion de la grilla
            ax.set_xticks(np.arange(0, 10, 1))
            ax.set_yticks(np.arange (0 ,10, 1))
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.grid(color ='gray',linestyle='-', linewidth =0.5)

            #Mostrar valores en cada celda
            for i in range(10):
                for j in range(10):
                    val = grilla[i,j]
                    if val > 0:
                        ax.text(j, i, int(val), va='center', ha='center', color='white')
            plt.title(f"Colonia de bacterias - Paso {paso_contador + 1}")
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
                        
    def reporte_estado(self):
        pass

    def exportar_csv(self):
        pass