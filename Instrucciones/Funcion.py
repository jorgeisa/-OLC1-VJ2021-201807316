from Abstract.NodoArbol import NodoArbol
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.TablaSimbolos import TablaSimbolos
from Tabla_Simbolo.Tipo import TIPO
from Abstract.Instruccion import Instruccion
from Instrucciones.Break import Break


class Funcion(Instruccion):
    def __init__(self, idFuncion, parametros, instrucciones, fila, columna):
        self.__idFuncion = idFuncion.lower()
        self.__parametros = parametros
        self.__instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO  # Nos puede retornar un valor

    def interpretar(self, tree, table):
        # Creando el nuevo ambito para la funcion.
        tabla_nueva = TablaSimbolos(table)
        # Recorriendo la lista de instrucciones de la funcion.
        for instruccionFunc in self.__instrucciones:
            # Interpretar cada elemento de la lista de instrucciones de la funcion
            valorInstruccion = instruccionFunc.interpretar(tree, tabla_nueva)
            # Si la instancia es una Excepcion, entonces error.
            if isinstance(valorInstruccion, Excepcion):
                tree.getExcepciones().append(valorInstruccion)
                tree.updateConsola(valorInstruccion.toString())
            # Si la instruccion del metodo es una instancia BREAK, entonces error.
            if isinstance(valorInstruccion, Break):
                no_break = Excepcion("Semantico", "> Excepcion FUNCION (" + self.__idFuncion +
                                     ") : Sentencia break encontrada.<",
                                     self.fila, self.columna)
                tree.getExcepciones().append(no_break)
                tree.updateConsola(no_break.toString())
            if isinstance(valorInstruccion, Continue):
                no_continue = Excepcion("Semantico", "> Excepcion FUNCION (" + self.__idFuncion +
                                        ") : Sentencia continue encontrada.<",
                                        self.fila, self.columna)
                tree.getExcepciones().append(no_continue)
                tree.updateConsola(no_continue.toString())
            # Si la funcion tiene un return
            if isinstance(valorInstruccion, Return):
                self.tipo = valorInstruccion.tipo
                return valorInstruccion.valorExpresion

        return None

    def get_idFuncion(self):
        return self.__idFuncion

    def set_idFuncion(self, id_Funcion):
        self.__idFuncion = id_Funcion

    def get_parametros(self):
        return self.__parametros

    def set_parametros(self, parametros):
        self.__parametros = parametros

    def get_instrucciones(self):
        return self.__instrucciones

    def set_instrucciones(self, instrucciones):
        self.__instrucciones = instrucciones

    def get_fila(self):
        return self.fila

    def set_fila(self, fila):
        self.fila = fila

    def get_columna(self):
        return self.columna

    def set_columna(self, columna):
        self.columna = columna

    def get_tipo(self):
        return self.tipo

    def set_tipo(self, tipo):
        self.tipo = tipo

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
        return "None"

    def getNodo(self):
        nodo = NodoArbol("FUNCION")
        nodo.addHijoValor("func")
        nodo.addHijoValor(str(self.__idFuncion))

        if self.__parametros is not None:
            nodo_parametros = NodoArbol("PARAMETROS")
            for parametro in self.__parametros:
                nodo_parametro = NodoArbol("PARAMETRO")
                nodo_parametro.addHijoValor(str(self.obtenerTipo(parametro["tipo"])))
                nodo_parametro.addHijoValor(parametro["identificador"])
                nodo_parametros.addHijoNodo(nodo_parametro)
            nodo.addHijoNodo(nodo_parametros)

        if self.__instrucciones is not None:
            nodo_instrucciones = NodoArbol("INSTRUCCIONES FUNCION")
            for instruccion in self.__instrucciones:
                nodo_instrucciones.addHijoNodo(instruccion.getNodo())
            nodo.addHijoNodo(nodo_instrucciones)
        return nodo
