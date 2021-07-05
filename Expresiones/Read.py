import tkinter
from tkinter import simpledialog

from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Tipo import TIPO
import sys


class Read(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.CADENA

    def interpretar(self, tree, table):
        print(tree.getConsola())  # IMPRIME LA CONSOLA
        print("Ingreso a un READ. Ingrese el valor.\r")

        tree.setTextoActual(tree.getConsola())

        lectura = simpledialog.askstring("Read Function", "Ingrese el dato que se le pide: ", parent=tree.getTextoInterfaz())
        print(lectura)
        if lectura is None:
            return ""
        return lectura

    def getNodo(self):
        nodo = NodoArbol("READ")
        return nodo
