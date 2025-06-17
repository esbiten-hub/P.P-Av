import io
from PIL import Image
from colonia import Colonia
from bacteria_ambiente import Bacteria, Ambiente

class Simulador():
    def __init__(self, especie_bacteria, cantidad_bacterias, factor_ambiental, pasos):
        self.especie_bacteria = especie_bacteria #str
        self.cantidad_bacterias = cantidad_bacterias #int
        self.factor_ambiental = factor_ambiental #str
        self.pasos = pasos #int
        self.colonia = None #Class Colonia
    
    def inicia_simulacion(self):
        lista_bacterias = []
        for i in range(self.cantidad_bacterias):
            bacteria = Bacteria( i+1, self.especie_bacteria)
            lista_bacterias.append(bacteria)
        ambiente = Ambiente(self.factor_ambiental)
        self.colonia = Colonia(lista_bacterias, ambiente)

    def run(self):
        for i in range(self.pasos):
            buf = self.colonia.paso(i)
            return buf

    def graficar_crecimiento(self):
        pass

    def graficar_resistencia(self):
        pass