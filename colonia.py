import matplotlib.pyplot as plt
import random, io, csv, math
import numpy as np
from PIL import Image
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
from bacteria_ambiente import Bacteria, Ambiente

class Colonia:
    def __init__(self, bacterias, ambiente):
        self.__bacterias = bacterias #list de Bacterias
        self.__ambiente = ambiente #Ambiente
        self.__matriz_bacteriana = None #Matriz de objetos
    
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
            #Primera bacteria en zona superior izquierda
            matriz[0][0] = self.get_bacterias()[0]
            ocupado.append([0,0])
            #Asigna en la matriz el resto de bacterias alrededor de una existente
            for bacteria in self.get_bacterias()[1:]:
                while True:
                    x1, y1 = random.choice(ocupado)
                    x2, y2 = random.choice(direcciones_posibles)
                    nueva_posicion = [x1 + x2, y1 + y2]
                    #Evita una coordenada fuera de la matriz y una coordenada ocupada
                    if nueva_posicion[0] < 0 or nueva_posicion[0] > 9 or nueva_posicion[1] < 0 or nueva_posicion[1] > 9:
                        pass
                    elif matriz[nueva_posicion[0]][nueva_posicion[1]] != 0:
                        pass
                    else:
                        matriz[nueva_posicion[0]][nueva_posicion[1]] = bacteria
                        ocupado.append(nueva_posicion)
                        break
            
            #Añade biofilm a la matriz
            while True:
                pase =  True
                pase_2 = True
                i = random.randint(0,9)
                j = random.randint(0,9)
                ubicaciones_biofilm = [(i,j), (i,j+1), (i-1,j), (i-1,j+1)]
                for ubicacion in ubicaciones_biofilm:
                    #Evita salir de la matriz y una coordenada ocupada
                    if ubicacion[0] < 0 or ubicacion[0] > 9 or ubicacion[1] > 9 or ubicacion[1] < 0:
                        pase = False
                        break
                if pase:
                    for ubicacion in ubicaciones_biofilm:
                        if matriz[ubicacion[0]][ubicacion[1]] != 0:
                            pase_2 = False
                            break
                if pase == True and pase_2 == True:
                    matriz[i][j] = "biofilm"
                    matriz[i][j+1] = "biofilm"
                    matriz[i-1][j] = "biofilm"
                    matriz[i-1][j+1] = "biofilm"
                    break

            #Añade factor ambiental a la matriz
            factor_ambiental = self.get_ambiente().get_factor_ambiental()
            if factor_ambiental == 'Antibiótico': #Añade antibiotico a 5 casillas aleatorias de la matriz
                for i in range(5):
                    while True:
                        x = random.randint(0, 9)
                        y = random.randint(0, 9)
                        #Solo se añadirá si el espacio de la matriz esta vacío
                        if matriz[x][y] == 0:
                            matriz[x][y] = factor_ambiental
                            break
            
            #Asigna la matriz de objetos al atributo de la clase
            self.__matriz_bacteriana = matriz

            #Obtiene la grilla numpy de Ambiente
            grilla = self.get_ambiente().get_grilla()
            #Lee la matriz y asigna a la grilla los valores correspondientes
            for i in range(10):
                for j in range(10):
                    if isinstance(matriz[i][j], Bacteria):
                        grilla[i,j] = 1
                    elif matriz[i][j] == factor_ambiental:
                        grilla[i,j] = 4
                    elif matriz[i][j] == "biofilm":
                        grilla[i,j] = 5 

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

            #Exporta un csv con los resultados del primer paso
            self.exportar_csv(paso_contador)

            #Guardar la imagen
            #Guarda archivo en memoria -> bytes
            fig_bytes = io.BytesIO()
            #Guarda la grafica en formato png en el espacio de memoria asignado
            fig.savefig(fig_bytes, format='png')
            #Libera el espacio de memoria de la grafica
            plt.close(fig)
            fig_bytes.seek(0)

            #Realiza el reporte de estado del paso actual (1)
            self.reporte_estado(paso_contador)
            
            return fig_bytes

        #Si no es el primer paso, se actualiza la matriz y luego la grilla
        else:
            matriz = self.__matriz_bacteriana
            factor_ambiental = self.get_ambiente().get_factor_ambiental()
            ubicacion_bacterias_hijas = [] #IMPORTANTE: Las bacterias hijas no ejecutan funcion hasta el siguiente paso
            for i in range(10):
                for j in range(10):
                    #Efecto de factor ambiental
                    if isinstance(matriz[i][j], str):
                        #Si detecta antibiótico, busca bacterias alrededor y ocurre el evento para antibióticos
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
                        #Si esta activa y no es una bacteria hija del paso actual
                        if bacteria.get_estado() == "activa" and (i,j) not in ubicacion_bacterias_hijas:
                            #Come si no ha llegado al umbral de energia para dividirse
                            if bacteria.get_energia() < 25:
                                #Recibe los nutrientes en la ubicacion de la bacteria
                                nutrientes = self.get_ambiente().get_nutrientes()[i][j]
                                if nutrientes > 0:
                                    #La bacteria se alimenta
                                    nutrientes_restantes = bacteria.alimentar(nutrientes)   
                                    #Los nutrientes sobrantes se devuelven a la matriz                                 
                                    self.get_ambiente().set_nutrientes_coordenada(i, j, nutrientes_restantes)
                                    #Se difunden los nutrientes
                                    self.get_ambiente().difundir_nutrientes()
                                else:
                                    #La bacteria no se alimenta, pierde energía
                                    bacteria.falta_de_alimento()

                            #Reunir coordenadas hacia donde podría haber biofilm
                            ubicaciones_posibles = [[i-1,j], [i+1,j], [i,j-1], [i,j+1], [i-1,j-1], [i-1,j+1], [i+1,j-1], [i+1,j+1]]
                            for ubicacion in ubicaciones_posibles:
                                #El biofilm entrega una cantidad de nutrientes
                                if ubicacion == "biofilm":
                                    nutrientes_bioflm = random.uniform(10,20)
                                    bacteria.alimentar(nutrientes_biofilm)

                            #Se divide alcanzando energía 25
                            if bacteria.get_energia() >= 25:
                                #Reunir coordenadas hacia donde podría dividirse la bacteria
                                ubicaciones_posibles = [i-1,j], [i+1,j], [i,j-1], [i,j+1], [i-1,j-1], [i-1,j+1], [i+1,j-1], [i+1,j+1]
                                #Filtrar ubicaciones
                                ubicaciones_validas = []
                                #Evita coordenadas ocupadas
                                for ubicacion in ubicaciones_posibles:
                                    if ubicacion[0] < 0 or ubicacion[0] > 9 or ubicacion[1] < 0 or ubicacion[1] > 9:
                                        pass
                                    elif isinstance(matriz[ubicacion[0]][ubicacion[1]], Bacteria):
                                        pass
                                    elif isinstance(matriz[ubicacion[0]][ubicacion[1]], str): #en caso de que haya factor ambiental o biofilm
                                        pass
                                    else:
                                        #Guarda la ubicación válida
                                        ubicaciones_validas.append(ubicacion)
                                #Si hay ubicaciones donde dividirse, elige una al azar
                                if len(ubicaciones_validas) > 0:
                                    x, y = random.choice(ubicaciones_validas)
                                    id_nueva_bacteria = self.get_bacterias()[-1].get_id() + 1
                                    nueva_bacteria = bacteria.dividirse(id_nueva_bacteria)
                                    self.__bacterias.append(nueva_bacteria)
                                    matriz[x][y] = nueva_bacteria
                                    self.get_ambiente().get_grilla()[x][y] = 1
                                    ubicacion_bacterias_hijas.append((x,y))

                            #Probabilidad de mutacion
                            #Si estan cerca de biofilm no mutan
                            muta = True
                            ubicaciones_posibles = [i-1,j], [i+1,j], [i,j-1], [i,j+1], [i-1,j-1], [i-1,j+1], [i+1,j-1], [i+1,j+1]
                            #Busca biofilm alrededor de la bacteria
                            #Hay biofilm -> no muta / No hay biofilm -> puede mutar
                            for ubicacion in ubicaciones_posibles:
                                if ubicacion[0] < 0 or ubicacion[0] > 9 or ubicacion[1] < 0 or ubicacion[1] > 9:
                                        pass
                                else:
                                    if matriz[ubicacion[0]][ubicacion[1]] == "biofilm":
                                        muta = False
                            if muta == True:
                                bacteria.mutar()                   

                            #Inactiva bacterias sin suficiente energia
                            if bacteria.morir():
                                self.get_ambiente().get_grilla()[i][j] = 2

                            #Costo de energia por ciclo
                            bacteria.desgaste_x_ciclo()

            #Actualizar valores/numeros de grilla numpy
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

            #Exporta un csv con los resultados del paso
            self.exportar_csv(paso_contador)

            #Guardar la imagen
            fig_bytes = io.BytesIO()
            fig.savefig(fig_bytes, format='png')
            plt.close(fig)
            fig_bytes.seek(0)

            #Realiza el reporte de estado del paso actual 
            self.reporte_estado(paso_contador)

            return fig_bytes
                        
    def reporte_estado(self, paso_contador):
        bacterias_activas = 0
        bacterias_inactivas = 0
        bacterias_resistentes = 0
        #Cuenta bacterias activas, resistentes e inactivas
        for bacteria in self.get_bacterias():
            if bacteria.get_estado() == "activa":
                bacterias_activas += 1
            if bacteria.get_estado() == "inactiva":
                bacterias_inactivas += 1
            if bacteria.get_resistencia() == True and bacteria.get_estado() == "activa":
                bacterias_resistentes += 1
        print(f"############ Reporte de estado {paso_contador + 1} ############")
        if paso_contador == 0:
            print(f"Bacterias iniciales: {bacterias_activas}")
            print("---> Energía base: 10")
        else:
            print(f"Bacterias activas: {bacterias_activas}")
            print(f"Bacterias inactivas: {bacterias_inactivas}")
            print(f"Bacterias resistentes: {bacterias_resistentes}")

    def exportar_csv(self, paso_contador):
        #Si es el primer paso abre el csv,
        #haya o no algo escrito, se dejará el csv vacío
        if paso_contador == 0:
            open('bacterias.csv', 'w').close()
        #Se escribe el csv en 'a' (append)
        #para que se guarden todos los pasos en el mismo csv
        with open(f'bacterias.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if paso_contador == 0:
                writer.writerow(['paso', 'id', 'raza', 'energia', 'estado', 'resistencia'])
            for bacteria in self.get_bacterias():
                writer.writerow([paso_contador + 1 ,bacteria.get_id(), bacteria.get_raza(), math.trunc(bacteria.get_energia()), bacteria.get_estado(), bacteria.get_resistencia()])