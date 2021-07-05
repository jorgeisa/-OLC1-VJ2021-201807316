from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import TIPO


class Imprimir(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.fila = fila
        self.columna = columna
        self.expresion = expresion

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table) # retorna cualquier valor

        if isinstance(value, Excepcion):  # Los errores se realizan hasta por ultimo, entonces hay que validarlo
            return value

        if self.expresion.tipo == TIPO.ARREGLO:
            return Excepcion("Semantico", ">No se puede imprimir un arreglo completo<", self.fila, self.columna)
        elif self.expresion.tipo == TIPO.NULO:
            return Excepcion("Semantico", ">Null Pointer. No se puede imprimir un Tipo Nulo<", self.fila, self.columna)

        tree.updateConsola(value)
        return None

    def getNodo(self):
        nodo = NodoArbol("PRINT")
        nodo.addHijoNodo(self.expresion.getNodo())
        return nodo


























