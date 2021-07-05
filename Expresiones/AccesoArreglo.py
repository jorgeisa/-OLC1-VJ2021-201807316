from Expresiones.Primitivos import Primitivos
from Tabla_Simbolo.Tipo import TIPO
from Tabla_Simbolo.Excepcion import Excepcion
from Abstract.NodoArbol import NodoArbol
from Abstract.Instruccion import Instruccion
import copy


class AccesoArreglo(Instruccion):
    def __init__(self, identificador, lista_expresiones, fila, columna):
        self.identificador = identificador
        self.lista_expresiones = lista_expresiones
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        # Obtenemos el arreglo
        simbolo = table.getTabla(self.identificador.lower())

        # Si no lo encontro
        if simbolo is None:
            return Excepcion("Semantico", "> Excepcion VARIABLE (ID) " + self.identificador + " no encontrado. <", self.fila, self.columna)

        # verificando si es un arreglo

        if not simbolo.getBanderaArreglo():
            return Excepcion("Semantico", "> Excepcion VARIABLE (ID) " + self.identificador + " no es un arreglo. <", self.fila,
                             self.columna)

        # Buscando en el arreglo encontrado (Posiciones)
        # Retorna el valor en la posicion del arreglo
        value = self.buscarDimensiones(tree, table, copy.copy(self.lista_expresiones),
                                       simbolo.getValor())
        if isinstance(value, Excepcion): return value
        if isinstance(value, list):
            return Excepcion("Semantico", "Acceso a Arreglo incompleto.", self.fila, self.columna)
        self.tipo = simbolo.getTipo()

        if value.interpretar(tree,table) == "null":
            return Excepcion("Semantico", "Excepcion ARREGLO: Posicion con valor null." , self.fila, self.columna)

        return value.interpretar(tree, table)

    def getNodo(self):
        nodo = NodoArbol("ACCESO ARREGLO")
        nodo.addHijoValor(str(self.identificador))
        exp = NodoArbol("EXPRESIONES DE LAS DIMENSIONES")
        if self.lista_expresiones is not None:
            for expresion in self.lista_expresiones:
                exp.addHijoValor("[")
                exp.addHijoNodo(expresion.getNodo())
                exp.addHijoValor("]")
            nodo.addHijoNodo(exp)
        return nodo

    def buscarDimensiones(self, tree, table, expresiones, arreglo):
        valor_retornado = None
        if len(expresiones) == 0:
            return arreglo
        if not isinstance(arreglo, list):
            return Excepcion("Semantico", "> Excepcion ACCESO de más en un Arreglo. <", self.fila, self.columna)
        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): return num
        if dimension.tipo != TIPO.ENTERO:
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)

        try:
            valor_retornado = self.buscarDimensiones(tree, table, copy.copy(expresiones), arreglo[num])
        except:
            return Excepcion("Semantico", "> Excepcion ARREGLO, error en indice de arreglo. <", self.fila, self.columna)
        return valor_retornado
