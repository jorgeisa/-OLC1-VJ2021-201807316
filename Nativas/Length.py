
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import TIPO
from Instrucciones.Funcion import Funcion


class Length(Funcion):
    def __init__(self, idFuncion, parametros, instrucciones, fila, columna):
        self.__idFuncion = idFuncion.lower()
        self.__parametros = parametros
        self.__instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.NULO  # Nos puede retornar un valor

    def interpretar(self, tree, table):
        simbolo = table.getTabla("length##Parametro1")
        if simbolo is None:
            return Excepcion("Semantico", "> Excepcion LENGTH: No se encontro parametro. <", self.fila, self.columna)

        if isinstance(simbolo.getValor(), list):
            self.tipo = TIPO.ENTERO
            return len(simbolo.getValor())

        if simbolo.getTipo() is not TIPO.CADENA:
            return Excepcion("Semantico", "> Excepcion LENGTH: Tipo no es cadena o arreglo. <", self.fila, self.columna)

        self.tipo = simbolo.getTipo()
        return len(simbolo.getValor())

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