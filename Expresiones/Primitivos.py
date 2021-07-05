from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol

class Primitivos(Instruccion):
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna
        self.bandera_arreglo = False

    def interpretar(self, tree, table):
        return self.valor

    def getNodo(self):
        nodo = NodoArbol("PRIMITIVO")
        nodo.addHijoValor(str(self.valor))
        return nodo

    def getBanderaArreglo(self):
        return self.bandera_arreglo

    def setBanderaArreglo(self, bandera_arreglo):
        self.bandera_arreglo = bandera_arreglo
