from bacteria_ambiente import Bacteria, Ambiente

class Colonia:
    def __init__(self, bacterias, ambiente):
        self.__bacterias = bacterias
        self.__ambiente = ambiente 
    
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

    def paso():
        pass

    def reporte_estado():
        pass

    def exportar_csv():
        pass