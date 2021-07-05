from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion


class Return(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.valorExpresion = None

    def interpretar(self, tree, table):
        # Evaluando si el valor no es un error
        valor_exp = self.expresion.interpretar(tree, table)
        if isinstance(valor_exp, Excepcion): return valor_exp

        self.tipo = self.expresion.tipo  # Guardando el tipo en return
        self.valorExpresion = valor_exp  # Guardando el valor en return
        return self

    def get_valorExpresion(self):
        return self.valorExpresion

    def set_valorExpresion(self, valorExpresion):
        self.valorExpresion = valorExpresion

    def getNodo(self):
        nodo = NodoArbol("RETURN")
        nodo.addHijoNodo(self.expresion.getNodo())
        return nodo
