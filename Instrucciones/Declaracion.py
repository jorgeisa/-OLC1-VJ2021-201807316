from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Simbolo import Simbolo
from Abstract.Instruccion import Instruccion
from Tabla_Simbolo.Tipo import TIPO


class Declaracion(Instruccion):
    def __init__(self, identificador, fila, columna, expresion=None, tipo=None):
        self.identificador = identificador
        self.tipo = tipo  # No sabemos que tipo sera
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        if self.expresion is not None:
            value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
            if isinstance(value, Excepcion): return value
            self.tipo = self.expresion.tipo
        else:
            value = "null"

        simbolo = Simbolo(str(self.identificador), self.tipo, self.fila, self.columna, value)
        result = table.setTabla(simbolo)

        if isinstance(result, Excepcion): return result
        return None

    def getNodo(self):
        nodo = NodoArbol("DECLARACION")
        nodo.addHijoValor("var")
        nodo.addHijoValor(str(self.identificador))
        # Verificando si la declaracion no es solamente var i;
        if self.expresion is not None:
            nodo.addHijoValor("=")
            nodo.addHijoNodo(self.expresion.getNodo())
        else:
            pass
        return nodo
