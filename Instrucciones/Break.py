from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol


class Break(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoArbol("BREAK")
        return nodo