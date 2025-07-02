import io
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from colonia import Colonia
from bacteria_ambiente import Bacteria, Ambiente

class Simulador():
    def __init__(self, especie_bacteria, cantidad_bacterias, factor_ambiental, pasos):
        self.especie_bacteria = especie_bacteria #str
        self.cantidad_bacterias = cantidad_bacterias #int
        self.factor_ambiental = factor_ambiental #Nada/Antibiótio
        self.pasos = pasos #int
        self.colonia = None #Class Colonia
    
    def inicia_simulacion(self):
        #Inicia Ambiente y Colonia
        lista_bacterias = []
        for i in range(self.cantidad_bacterias):
            bacteria = Bacteria( i+1, self.especie_bacteria)
            lista_bacterias.append(bacteria)
        ambiente = Ambiente(self.factor_ambiental)
        self.colonia = Colonia(lista_bacterias, ambiente)

    def run(self):
        #Recibe las graficas de los pasos realizados
        bytes_por_simulacion = []
        for i in range(self.pasos):
            fig_bytes = self.colonia.paso(i)
            bytes_por_simulacion.append(fig_bytes)

        #Envia las gráficas a la interfaz gráfica
        return bytes_por_simulacion

    def graficar_crecimiento(self, archivo):

        #Leer los datos
        datos = pd.read_csv(archivo.get_path())
        
        #Filtrar solo bacterias activas
        activas = datos[datos["estado"] == "activa"]

        #Contar bacterias activas por paso
        activas_por_paso = activas.groupby("paso").size()

        #Grafica de crecimiento
        plt.figure(figsize=(10, 10))
        plt.plot(activas_por_paso.index, activas_por_paso.values, label = "Bacterias activas")
        plt.title("Crecimiento de las bacterias")
        plt.xlabel("Pasos")
        plt.ylabel("Cantidad de bacterias activas")
        plt.legend()
        plt.tight_layout()
        plt.grid(True)
        
        #Guardar la imagen
        fig_bytes = io.BytesIO()
        plt.savefig(fig_bytes, format='png')
        plt.close()
        fig_bytes.seek(0)

        #Cargar imagen con PIL
        image = Image.open(fig_bytes)
        width, height = image.size

        return image, width, height

    def graficar_resistencia(self, archivo):

        #Leer los datos
        datos = pd.read_csv(archivo.get_path())

        #Filtrar solo bacterias resistentes
        resistentes = datos[datos["resistencia"] == True]

        #Contar bacterias resistentes por paso
        resistentes_por_paso = resistentes.groupby("paso").size()

        #Grafica de resistencia
        plt.figure(figsize=(10, 10))
        plt.plot(resistentes_por_paso.index, resistentes_por_paso.values, label = "Bacterias resistentes")
        plt.title("Resistencia de las bacterias")
        plt.xlabel("Pasos")
        plt.ylabel("Cantidad de bacterias resistentes")
        plt.legend()
        plt.tight_layout()
        plt.grid(True)
        
        #Guardar la imagen
        fig_bytes = io.BytesIO()
        plt.savefig(fig_bytes, format='png')
        plt.close()
        fig_bytes.seek(0)

        #Cargar imagen con PIL
        image = Image.open(fig_bytes)
        width, height = image.size

        return image, width, height