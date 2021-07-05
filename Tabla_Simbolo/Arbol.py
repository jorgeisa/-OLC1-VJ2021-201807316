from tkinter import END
from tkinter import INSERT


class Arbol:
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.__funciones = []
        self.excepciones = []
        self.consola = ""
        self.TSglobal = None
        self.__texto_interfaz = None
        self.dot = ""
        self.contador_dot = 0
        self.listaTablas = []

    def getListaTablas(self):
        return self.listaTablas

    def setListaTablas(self, listaTablas):
        self.listaTablas = listaTablas

    def addToListaTablas(self, tabla):
        self.listaTablas.append(tabla)

    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def getExcepciones(self):
        return self.excepciones

    def setExcepciones(self, excepciones):
        self.excepciones = excepciones

    def getConsola(self):
        return self.consola

    def getTextoInterfaz(self):
        return self.__texto_interfaz

    def setTextoInterfaz(self, texto):
        self.__texto_interfaz = texto

    def setTextoActual(self, textoActual):
        self.__texto_interfaz.delete("1.0", END)  # Borramos la consola
        self.__texto_interfaz.insert("insert", textoActual)  # Insertamos el contenido del path

    def setConsola(self, consola):
        self.consola = consola

    def updateConsola(self, cadena):
        self.consola += str(cadena) + '\n'

    def getTSGlobal(self):
        return self.TSglobal

    def setTSglobal(self, TSglobal):
        self.TSglobal = TSglobal

    # ------------------- FUNCIONES ---------------------
    def getFunciones(self):
        return self.__funciones

    def setFunciones(self, funciones):
        self.__funciones = funciones

    # Obtener funcion
    def getFuncion(self, idFuncion):
        # Recorremos la lista de funciones guardadas
        for funcion in self.__funciones:
            # Verificamos si el nombre es el mismo
            if funcion.get_idFuncion().lower() == idFuncion.lower():
                return funcion
        # Si no encuentra ninguna funcion con ese nombre
        return None

    # Agregar una funcion
    def addFuncion(self, funcion):
        self.__funciones.append(funcion)

    def getDot(self, raiz):  # Retorna la cadena de la grafica
        self.dot = ""
        self.dot += "digraph {\n" \
                    "bgcolor=\"#F2F4F4\"; node[style=bold, color=\"#27AE60\", style=\"filled,setlinewidth(2)\", " \
                    "fillcolor=white];\n"
        self.dot += "n0[label=\"" + raiz.getValor().replace("\"", "\\\"") + "\"];\n"
        self.contador_dot = 1
        self.recorrerAST("n0", raiz)
        self.dot += "}"
        return self.dot

    def recorrerAST(self, idPadre, nodoPadre):
        for hijo in nodoPadre.getListaHijos():
            nombreHijo = "n" + str(self.contador_dot)
            self.dot += nombreHijo + "[label=\"" + hijo.getValor().replace("\"", "\\\"") + "\"];\n"
            self.dot += idPadre + "->" + nombreHijo + ";\n"
            self.contador_dot += 1
            self.recorrerAST(nombreHijo, hijo)
