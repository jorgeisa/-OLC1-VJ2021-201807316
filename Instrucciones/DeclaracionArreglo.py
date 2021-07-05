from Tabla_Simbolo.Tipo import TIPO
from Expresiones.Primitivos import Primitivos
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Simbolo import Simbolo
from Abstract.NodoArbol import NodoArbol
from Abstract.Instruccion import Instruccion
import copy


class DeclaracionArreglo(Instruccion):
    def __init__(self, tipo_dato1, dimensiones, identificador, tipo_dato2, lista_expresiones, identificador_2, fila, columna):
        self.tipo_dato1 = tipo_dato1            # Tipo de dato del arreglo declarado
        self.dimensiones = dimensiones          # Tipo entero para verificar con len(lista_expresiones)
        self.identificador = identificador      # Identificador del arreglo declarado
        self.tipo_dato2 = tipo_dato2            # Tipo de dato del new
        self.lista_expresiones = lista_expresiones  # [1][2][3][4] del new
        self.identificador_2 = identificador_2  # En caso venga un ID en vez del NEW
        self.fila = fila
        self.columna = columna
        self.arreglo = True
        self.tipo = TIPO.ARREGLO

    def interpretar(self, tree, table):
        # Si trae NEW la declaracion
        if (self.tipo_dato2 is not None) and (self.lista_expresiones is not None):
            # Verificacion de tipos
            if self.tipo_dato1 != self.tipo_dato2:
                return Excepcion("Semantico", "Tipo de dato diferente en Arreglo.", self.fila, self.columna)
            # Verificacion de dimensiones
            if self.dimensiones != len(self.lista_expresiones):
                return Excepcion("Semantico", "Dimensiones diferentes en Arreglo.", self.fila, self.columna)

            # Creacion de arreglo
            valor_dimensiones = self.crearDimensiones(tree, table, copy.copy(self.lista_expresiones))  # RETORNA EL ARREGLO DE DIMENSIONES
            if isinstance(valor_dimensiones, Excepcion): return valor_dimensiones

            # Creacion del simbolo para agregarlo a la tabla
            simbolo = Simbolo(str(self.identificador), self.tipo_dato1, self.fila, self.columna, valor_dimensiones)
            # Colocandole True a la bandera del simbolo para indicar que es un arreglo
            simbolo.setBanderaArreglo(True)
            simbolo.setDimensionArreglo(self.dimensiones)
            longitud = self.obtenerLongitud(tree, table, self.lista_expresiones)
            simbolo.setLongitudArreglo(longitud)
            # Verificando que se haya agregado a la tabla bien.
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
        else:
            # Vamos a traer el arreglo al que se le asignara (identificador 2)
            simbolo_2 = table.getTabla(self.identificador_2.lower())
            # Verificando que se haya encontrado la variable
            if simbolo_2 is None:
                return Excepcion("Semantico", "> Excepcion ARREGLO, variable (ID) " +
                                 self.identificador_2 + " no encontrada.<", self.fila,
                                 self.columna)
            # Verificando que se igualo a un arreglo
            if simbolo_2.getBanderaArreglo() is False:
                return Excepcion("Semantico", "> Excepcion ARREGLO, variable (ID) " +
                                 self.identificador_2 + " no es de tipo arreglo.<", self.fila,
                                 self.columna)

            # Verificar que tengan la misma longitud de dimensionales
            if simbolo_2.getDimensionArreglo() != self.dimensiones:
                return Excepcion("Semantico", "> Excepcion ARREGLO, variable (ID) " +
                                 self.identificador_2 + " no tiene las mismas dimensiones. <", self.fila, self.columna)

            simbolo = Simbolo(str(self.identificador), self.tipo_dato1, self.fila, self.columna, simbolo_2.getValor())
            simbolo.setBanderaArreglo(True)
            simbolo.setDimensionArreglo(self.dimensiones)
            longitud = simbolo_2.getLongitudArreglo()
            simbolo.setLongitudArreglo(longitud)
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
        return None

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

    def obtenerLongitud(self, tree, table , listaExpresiones):
        longitud = 1
        for expresion in listaExpresiones:
            numero = expresion.interpretar(tree, table)
            longitud = longitud * numero
        return longitud

    def getNodo(self):
        nodo = NodoArbol("DECLARACION ARREGLO")
        nodo.addHijoValor(str(self.obtenerTipo(self.tipo_dato1)))
        for i in range(self.dimensiones):
            nodo.addHijoValor(str("[]"))
        nodo.addHijoValor(str(self.identificador))
        nodo.addHijoValor("=")
        if (self.tipo_dato2 is not None) and (self.lista_expresiones is not None):
            nodo.addHijoValor("new")
            nodo.addHijoValor(str(self.obtenerTipo(self.tipo_dato2)))
            exp = NodoArbol("EXPRESIONES DE LAS DIMENSIONES")
            for expresion in self.lista_expresiones:
                exp.addHijoValor("[")
                exp.addHijoNodo(expresion.getNodo())
                exp.addHijoValor("]")
            nodo.addHijoNodo(exp)
        else:
            nodo.addHijoValor(str(self.identificador_2))

        return nodo

    # Metodo recursivo que genera listas de listas segun la dimension (expresiones TIPO.ENTERO) que encuentre.
    def crearDimensiones(self, tree, table, lista_expresiones):
        arr = []
        if len(lista_expresiones) == 0:
            primitivo = Primitivos(TIPO.NULO, "null", self.fila, self.columna)
            primitivo.setBanderaArreglo(True)
            return primitivo
        dimension = lista_expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        # Si la expresion no es error
        if isinstance(num, Excepcion): return num
        # Si la expresion no es de tipo entero
        if dimension.tipo != TIPO.ENTERO:
            return Excepcion("Semantico", "> Excepcion ARREGLO: Expresion diferente a ENTERO en Arreglo.<", self.fila, self.columna)
        contador = 0
        while contador < num:
            arr.append(self.crearDimensiones(tree, table, copy.copy(lista_expresiones)))
            contador += 1
        return arr
#

