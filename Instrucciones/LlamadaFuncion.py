from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.TablaSimbolos import TablaSimbolos
from Tabla_Simbolo.Simbolo import Simbolo
from Abstract.Instruccion import Instruccion
from Instrucciones.Break import Break
from Tabla_Simbolo.Tipo import TIPO


class LlamadaFuncion(Instruccion):
    def __init__(self, idFuncion, parametros, fila, columna):
        self.__idFuncion = idFuncion.lower()
        self.__parametros = parametros
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        # Buscar la funcion
        # result_funcion = funcion que obtenemos de la lista de funciones contiene una lista de diccionarios
        result_funcion = tree.getFuncion(self.__idFuncion.lower())

        # VALIDACION DE BUSQUEDA DE FUNCION
        if result_funcion is None:  # SI NO SE ENCONTRO LA FUNCION
            nombreFuncion = str(self.__idFuncion)
            return Excepcion("Semantico", "> Funcion: " + nombreFuncion + " no encontrada. <", self.fila, self.columna)

        # NUEVA TABLA ( NUEVO AMBITO PARA LA FUNCION )
        new_table = TablaSimbolos(tree.getTSGlobal())

        # OBTENIENDO PARAMETROS
        # SI LOS PARAMETROS TIENEN EL MISMO NUMERO DE PARAMETROS
        if len(result_funcion.get_parametros()) == len(self.__parametros):
            contador_tipo = 0

            # parametro sera tipo expresion, ya que en la llamada debe venir una expresion
            # parametro = Objeto
            for parametro in self.__parametros:
                parametro_expresion = parametro.interpretar(tree, table)  # parametro_expresion = valor de Objeto

                # Verificando que no venga con errores la expresion
                if isinstance(parametro_expresion, Excepcion): return parametro_expresion

                if str(result_funcion.get_parametros()[contador_tipo]['identificador']) in ('round##Parametro1', 'truncate##Parametro1', 'length##Parametro1', "Typeof##Parametro1"):
                    # CREANDO EL SIMBOLO E INGRESANDOLO A LA NUEVA TABLA DE SIMBOLOS PARA LA FUNCION
                    identificador = str(result_funcion.get_parametros()[contador_tipo]['identificador']).lower()
                    tipo = parametro.tipo
                    simbolo = Simbolo(identificador, tipo, self.fila, self.columna, parametro_expresion)

                    agregarTabla = new_table.setTabla(simbolo)
                    if isinstance(agregarTabla, Excepcion): return agregarTabla
                    break

                # SI EL PARAMETRO ES UN ARREGLO
                if result_funcion.get_parametros()[contador_tipo]['tipo'] == TIPO.ARREGLO:
                    # Llamada - > funcion(arreglo)    funcion -> func (int [] arr)
                    simbolo_arr = table.getTabla(parametro.identificador.lower())
                    # Verificando si existe
                    if simbolo_arr is None:
                        return Excepcion("Semantico",
                                         "> Excepcion FUNCION, arreglo (ID) " + parametro.identificador
                                         + " no encontrada.<", self.fila, self.columna)
                    # Verificando que sea un arreglo
                    if simbolo_arr.getBanderaArreglo() is False:
                        return Excepcion("Semantico",
                                         "> Excepcion FUNCION, arreglo (ID) " + parametro.identificador
                                         + " no es un arreglo.<", self.fila, self.columna)
                    # verificando que las dimensiones sean iguales
                    if simbolo_arr.getDimensionArreglo() != result_funcion.get_parametros()[contador_tipo]['longitud']:
                        return Excepcion("Semantico",
                                         ">Excepcion LLAMADA Parametros: Arreglo no tiene las mismas dimensiones.<",
                                         self.fila, self.columna)
                    if parametro.tipo != result_funcion.get_parametros()[contador_tipo]['tipo_dato']:
                        return Excepcion("Semantico",
                                         ">Excepcion LLAMADA Parametros: Arreglo no es del mismo tipo.<",
                                         self.fila, self.columna)
                    # CREANDO EL SIMBOLO E INGRESANDOLO A LA NUEVA TABLA DE SIMBOLOS PARA LA FUNCION
                    identificador = str(result_funcion.get_parametros()[contador_tipo]['identificador']).lower()
                    tipo = result_funcion.get_parametros()[contador_tipo]['tipo_dato']
                    simbolo = Simbolo(identificador, tipo, self.fila, self.columna, parametro_expresion)
                    simbolo.setBanderaArreglo(True)
                    simbolo.setDimensionArreglo(simbolo_arr.getDimensionArreglo())
                    agregarTabla = new_table.setTabla(simbolo)
                    if isinstance(agregarTabla, Excepcion): return agregarTabla
                    contador_tipo += 1
                    continue

                # Si los tipos son iguales
                if result_funcion.get_parametros()[contador_tipo]['tipo'] == parametro.tipo:
                    # CREANDO EL SIMBOLO E INGRESANDOLO A LA NUEVA TABLA DE SIMBOLOS PARA LA FUNCION
                    identificador = str(result_funcion.get_parametros()[contador_tipo]['identificador']).lower()
                    tipo = result_funcion.get_parametros()[contador_tipo]['tipo']
                    simbolo = Simbolo(identificador, tipo, self.fila, self.columna, parametro_expresion)
                    agregarTabla = new_table.setTabla(simbolo)
                    if isinstance(agregarTabla, Excepcion): return agregarTabla
                else:
                    # tipo_funcion = str(result_funcion.get_parametros()[contador_tipo]['tipo']).lower()
                    # tipo_llamada = str(parametro.tipo)
                    return Excepcion("Semantico", "> Excepcion DISTINTOS TIPOS DE PARAMETROS: Funcion y Llamada. <", self.fila, self.columna)
                contador_tipo += 1
        else:
            return Excepcion("Semantico", "> Excepcion DISTINTO NUMERO DE PARAMETROS: Funcion y Llamada. <", self.fila, self.columna)

        # INTERPRETAR EL NODO FUNCION
        value_function = result_funcion.interpretar(tree, new_table)
        if isinstance(value_function, Excepcion): return value_function

        self.set_tipo(result_funcion.get_tipo())
        # self.tipo = result_funcion.get_tipo()

        return value_function

    def get_idFuncion(self):
        return self.__idFuncion

    def set_idFuncion(self, id_Funcion):
        self.__idFuncion = id_Funcion

    def get_parametros(self):
        return self.__parametros

    def set_parametros(self, parametros):
        self.__parametros = parametros

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

    def getNodo(self):
        nodo = NodoArbol("LLAMADA FUNCION")
        nodo.addHijoValor(str(self.__idFuncion))
        nodo.addHijoValor("(")
        nodo_parametros = NodoArbol("PARAMETROS")
        for parametro in self.__parametros:
            nodo_parametro = NodoArbol("PARAMETRO")
            nodo_parametro.addHijoNodo(parametro.getNodo())
            nodo_parametros.addHijoNodo(nodo_parametro)
        nodo.addHijoNodo(nodo_parametros)
        nodo.addHijoValor(")")
        return nodo
