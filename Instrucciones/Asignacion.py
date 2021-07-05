from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Simbolo import Simbolo


class Asignacion(Instruccion):
    #
    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value

        simbolo = Simbolo(self.identificador, self.expresion.tipo, self.fila, self.columna, value)

        result = table.actualizarTabla(simbolo)

        if isinstance(result, Excepcion): return result
        return None

    def getNodo(self):
        nodo = NodoArbol("ASIGNACION")
        nodo.addHijoValor(str(self.identificador))
        nodo.addHijoValor("=")
        nodo.addHijoNodo(self.expresion.getNodo())
        return nodo
