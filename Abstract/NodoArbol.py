class NodoArbol():
    # El valor sera la cadena del label
    def __init__(self, valor):
        self.__listaHijos = []
        self.__valor = valor

    # Agregar un nodo hijo mandandole un valor (string)
    def addHijoValor(self, valorHijo):
        self.__listaHijos.append(NodoArbol(valorHijo))

    # Agregando hijos mandandole una lista de nodos hijo (cuando ya se tiene una lista hecha)
    def addHijosNodos(self, hijos):
        for hijo in hijos:
            self.__listaHijos.append(hijo)

    # Enviarle un objeto nodoAST
    def addHijoNodo(self, hijoNodo):
        self.__listaHijos.append(hijoNodo)

    # Agregar un nodo al inicio, mandandole un valor (string)
    def addPrimerHijo(self, valorHijo):
        self.__listaHijos.insert(0, NodoArbol(valorHijo))

    # Agregar un nodo al inicio, mandandole el NodoAST ya hecho
    def addPrimerHijoNodo(self, hijoNodo):
        self.__listaHijos.insert(0, hijoNodo)

    def getValor(self):
        return str(self.__valor)

    def setValor(self, valor):
        self.__valor = valor

    def getListaHijos(self):
        return self.__listaHijos

    def setListaHijos(self, listaHijos):
        self.__listaHijos = listaHijos
