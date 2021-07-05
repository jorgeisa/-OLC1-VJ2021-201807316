from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Simbolo import Simbolo
from Abstract.Instruccion import Instruccion
from Tabla_Simbolo.Tipo import TIPO
from Tabla_Simbolo.TablaSimbolos import lista_variables


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

        try:
            identificador_d = self.identificador
            tipo_d = str(self.obtenerTipo(self.tipo))
            tipo_d2 = str(simbolo.getBanderaArreglo())
            entorno_d = "declaracion_" + str(self.fila) + "_" + str(self.columna)
            valor_d = str(value)
            linea_d = str(self.fila)
            columna_d = str(self.columna)

            diccion = {'identificador': identificador_d, 'tipo1': tipo_d, 'tipo2': tipo_d2, 'entorno': entorno_d,
                       'valor': valor_d, 'linea': linea_d, 'columna': columna_d}
            lista_variables.append(diccion)
        except:
            print("error al agregar a la lista de tabla de simbolos")
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

    def obtenerTipo(self, tipo):
        if tipo == TIPO.ENTERO:
            return "Int"
        elif tipo == TIPO.DECIMAL:
            return "Double"
        elif tipo == TIPO.BOOLEANO:
            return "Boolean"
        elif tipo == TIPO.CARACTER:
            return "Char"
        elif tipo == TIPO.CADENA:
            return "String"
        elif tipo == TIPO.NULO:
            return "Null"
        elif tipo == TIPO.ARREGLO:
            return "Array"
