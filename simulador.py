from colonia import Colonia
from bacteria_ambiente import Bacteria, Ambiente

class Simulador():
    def __init__(self, especie_bacteria, cantidad_bacterias, factor_ambiental, pasos):
        self.especie_bacteria = especie_bacteria
        self.cantidad_bacterias = cantidad_bacterias
        self.factor_ambiental = factor_ambiental
        self.pasos = pasos
        self.colonia = None
    
    def inicia_simulacion(self):
        lista_bacterias = []
        for i in range(self.cantidad_bacterias):
            bacteria = Bacteria( i+1, self.especie_bacteria)
            lista_bacterias.append(bacteria)
        ambiente = Ambiente(self.factor_ambiental)
        self.colonia = Colonia(lista_bacterias, ambiente)

        self.run(self.pasos)

    def run(self, pasos):
        pass

    def graficar_crecimiento(self):
        pass

    def graficar_resistencia(self):
        pass