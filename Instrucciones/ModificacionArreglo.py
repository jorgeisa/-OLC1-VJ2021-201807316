from Expresiones.Primitivos import Primitivos
from Tabla_Simbolo.Tipo import TIPO
from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Abstract.Instruccion import Instruccion
import copy


class ModificarArreglo(Instruccion):
    def __init__(self, identificador, lista_expresiones, expresion, fila, columna):
        self.identificador = identificador
        self.lista_expresiones = lista_expresiones
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        # Interpretando la expresion a la que se quiere modificar la posicion del arreglo
        valor_expresion = self.expresion.interpretar(tree, table)  # Valor a asignar a la variable
        if isinstance(valor_expresion, Excepcion): return valor_expresion

        # Obteniendo el arreglo que se quiere modificar
        simbolo = table.getTabla(self.identificador.lower())

        # Si no encontro el arreglo
        if simbolo is None:
            return Excepcion("Semantico", "> Excepcion VARIABLE (ID) " + self.identificador + " no encontrada. <", self.fila, self.columna)

        # Verificando que si sea un arreglo
        if not simbolo.getBanderaArreglo():
            return Excepcion("Semantico", "> Excepcion VARIABLE (ID) " + self.identificador + " no es un arreglo. <", self.fila,
                             self.columna)

        # Verificando si la expresion y el tipo de array es el mismo
        if simbolo.getTipo() != self.expresion.tipo:
            return Excepcion("Semantico", "> Tipos de dato diferente en Modificacion de arreglo. <", self.fila,
                             self.columna)

        # BUSQUEDA DEL ARREGLO
        value = self.modificarDimensiones(tree, table, copy.copy(self.lista_expresiones), simbolo.getValor(),
                                          valor_expresion)  # RETORNA EL VALOR SOLICITADO
        if isinstance(value, Excepcion): return value
        return value

    def getNodo(self):
        nodo = NodoArbol("MODIFICACION ARREGLO")
        nodo.addHijoValor(str(self.identificador))
        exp = NodoArbol("EXPRESIONES DE LAS DIMENSIONES")
        if self.lista_expresiones:
            for expresion_ in self.lista_expresiones:
                exp.addHijoValor("[")
                exp.addHijoNodo(expresion_.getNodo())
                exp.addHijoValor("]")
            nodo.addHijoNodo(exp)
        nodo.addHijoNodo(self.expresion.getNodo())
        return nodo

    def modificarDimensiones(self, tree, table, expresiones, arreglo, valor):
        if len(expresiones) == 0:
            if isinstance(arreglo, list):
                return Excepcion("Semantico", "> Excepcion ARREGLO, modificacion a arreglo incompleto. <", self.fila, self.columna)
            return valor
        if not isinstance(arreglo, list):
            return Excepcion("Semantico", "> Excepcion ARREGLO, accesos de más en un arreglo. <", self.fila, self.columna)

        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): return num
        if dimension.tipo != TIPO.ENTERO:
            return Excepcion("Semantico", "> Excepcion ARREGLO, expresion no es de tipo INT en arreglo. <", self.fila, self.columna)

        try:
            value = self.modificarDimensiones(tree, table, copy.copy(expresiones), arreglo[num], valor)
            if isinstance(value, Excepcion): return value
        except:
            return Excepcion("Semantico", "> Excepcion ARREGLO, expresion fuera de limite. <", self.fila, self.columna)

        if value is not None:
            primitivo = Primitivos(self.expresion.tipo, value, self.fila, self.columna)
            primitivo.setBanderaArreglo(True)
            arreglo[num] = primitivo
        return None

