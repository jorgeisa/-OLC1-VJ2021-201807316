from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion


class Identificador(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())

        if simbolo is None:
            return Excepcion("Semantico", ">Variable " + self.identificador + " no encontrada.<", self.fila, self.columna)

        self.tipo = simbolo.getTipo()

        return simbolo.getValor()

    def getNodo(self):
        nodo = NodoArbol("IDENTIFICADOR")
        nodo.addHijoValor(str(self.identificador))
        return nodo
