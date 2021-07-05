import re
import webbrowser

import Tabla_Simbolo.Arbol
import os
import tkinter as tk
from tkinter import *  # ventana
from tkinter import Menu, ttk  # barra de tareas
from tkinter import filedialog  # filechooser
from tkinter import scrolledtext  # textarea
from tkinter import messagebox  # message box
from tkinter.messagebox import showinfo

# --------- Importaciones Gramatica ----------
import grammar
from Tabla_Simbolo.Arbol import Arbol
from Tabla_Simbolo.TablaSimbolos import TablaSimbolos
from Tabla_Simbolo.TablaSimbolos import lista_variables
from grammar import grammar_analisis
from grammar import realizar_dot



class MainScreen:

    # Metodo que contiene la definicion de la interfaz grafica
    def getInfo(self, event):
        string = self.txtEntrada.text.index(INSERT) # fila.columna
        print(string)
        self.lblPosition.destroy()
        self.lblPosition = Label(self.window, text=f"Posicion (V, H): {string}")
        self.lblPosition.place(x=200, y=430)

    # Metodo que contiene la definicion de la interfaz grafica
    def updateLabelName(self, nameLabel):
        self.lblNameFile.destroy()
        self.lblNameFile = Label(self.window, text=f"Nombre Archivo: {nameLabel}")
        self.lblNameFile.place(x=300, y=40)

    def runAnalisis(self):
        entradaTexto = self.txtEntrada.text.get("1.0", END)
        print('----------------------------------')

        ast_retun = grammar_analisis(entradaTexto, self.txtSalida)

        self.ast_tree = ast_retun
        consola = ast_retun.getConsola()
        self.txtSalida.delete("1.0", END)  # Borramos la consola
        self.txtSalida.insert("1.0", consola)  # Insertamos el contenido del path

    def actualizar_pintar(self, *args):
        posicion = self.txtEntrada.text.index(INSERT)
        entradaTexto = self.txtEntrada.text.get("1.0", "end")
        self.txtEntrada.text.delete("1.0", "end")

        for s in self.pintar_palabras(entradaTexto[0:len(entradaTexto)-1]):
            self.txtEntrada.text.insert(INSERT, s[1], s[0])
        self.txtEntrada.text.mark_set(INSERT, posicion)
        self.txtEntrada.text.see(INSERT)

    def __init__(self):
        # --------------------- VARIABLES PARA EL ANALISIS Y EXTRAS -------------------
        self.last_Open_Path = ""
        self.last_Open_Extension = ""
        self.ast_tree = None
        self.cadena_entrada = ""

        self.window = Tk()
        self.txtEntrada = Entry(self.window, width=15)
        self.txtSalida = Entry(self.window, width=15)

        # PROPIEDADES DE LA VENTANA, CENTRADO, TAMANIO, etc
        self.window.title("Proyecto - JPR")  # Titulo de la ventana
        widthTK = 800  # Ancho predeterminado de la ventana
        heightTK = 700  # Alura predeterminada de la ventana
        widthScreen = self.window.winfo_screenwidth()  # Ancho de la pantalla
        heightScreen = self.window.winfo_screenheight()  # Altura de la pantalla

        x = (widthScreen / 2) - (widthTK / 2)  # Posicion de centrado en x
        y = (heightScreen / 2) - (heightTK / 2)  # Posicion de centrado en y

        self.window.geometry(
            '%dx%d+%d+%d' % (widthTK + 550, heightTK, x - 280, y - 25))  # Colocarle la vetana en el centro

        self.window.configure(bg='#1C2833')  # Darle color a la ventana (fondo)
        # #212F3C
        # ------------------------------- LABEL TITULO PROPIEDADES -------------------------------
        # Posicionandolo en la ventana, texto a mostrar, tipo letra, fondo del label
        self.lbl = Label(self.window, text="Proyecto 1 - JPR", font=("Arial Bold", 15), bg='#1A5276', fg="#FFFFFF")
        self.lbl.pack(fill=X)  # Label estirado por el eje X en su posicion

        # ------------------------ PROPIEDADES DEL MENU DESPLEGABLE --------------------------------------

        # Agregando las opciones en el menu desplegable
        self.barra_menu = Menu(self.window)  # Creando el objeto barra (donde iran todos los "botones"
        self.file_item = Menu(self.barra_menu, bg='#1A5276', fg="#FFFFFF")  # Creando el "Boton" File que contendra cascada
        self.file_item.add_command(label='Nuevo', command=self.menu_New_Option)
        self.file_item.add_separator()
        self.file_item.add_command(label='Abrir Archivo (Pintar)', command=self.menu_Open_File)
        self.file_item.add_separator()
        self.file_item.add_command(label='Abrir Archivo (Sin Pintar)', command=self.menu_Open_File2)
        self.file_item.add_separator()
        self.file_item.add_command(label='Guardar Archivo', command=self.saveFile_PreviousOpen)
        self.file_item.add_separator()
        self.file_item.add_command(label='Guardar archivo como...', command=self.saveFile_SaveAs)
        self.file_item.add_separator()
        self.file_item.add_command(label='Ejecutar Analisis', command=self.runAnalisis)
        self.file_item.add_separator()
        self.file_item.add_command(label='Exit', command=exit)

        # Agregando estilo de menu - cascada
        self.barra_menu.add_cascade(label='Opciones Archivo', menu=self.file_item)

        # CREANDO OTRA PESTAÑA PARA REPORTES
        self.report_item = Menu(self.barra_menu, bg='#1A5276', fg="#FFFFFF")  # Agregando al mismo objeto barra otro "Boton"
        self.report_item.add_command(label='Reporte Errores (Html)', command=self.reporte_errores)
        self.report_item.add_separator()
        self.report_item.add_command(label='Reporte Errores (Tablas)', command=self.llenar_TablaErrores)
        self.report_item.add_separator()
        self.report_item.add_command(label='Reporte Simbolos (Tablas)', command=self.llenar_TablaSimbolos)
        self.report_item.add_separator()
        self.report_item.add_command(label='Reporte Arbol', command=self.reporte_arbol)
        self.report_item.add_separator()

        # Agregando el estilo menu - cascada
        self.barra_menu.add_cascade(label='Reportes', menu=self.report_item)

        # CREANDO OTRA PESTAÑA PARA ABRIR PDFS
        self.report_item = Menu(self.barra_menu, bg='#1A5276',
                                fg="#FFFFFF")  # Agregando al mismo objeto barra otro "Boton"
        self.report_item.add_command(label='Abrir PDF/HTML', command=self.menu_open_pdfhtml)
        self.report_item.add_separator()

        # Agregando el estilo menu - cascada
        self.barra_menu.add_cascade(label='Abrir PDF/HTML', menu=self.report_item)

        # COLOCANDO EL MENU CON OPCIONES DENTRO DEL WINDOW
        self.window.config(menu=self.barra_menu)

        # -------------------- PROPIEDADES DEL TXTENTRADA (TEXTO A ANALIZAR) -------------------------
        self.lblEntrada = Label(self.window, text="Entrada: ")
        self.lblEntrada.place(x=25, y=40)

        self.lblNameFile = Label(self.window, text="Nombre Archivo: ")
        self.lblNameFile.place(x=300, y=40)

        self.txtEntrada = ScrollTextUwU(self.window)  # 80,25

        # self.txtEntrada.configure(width=100, height=22)
        self.txtEntrada.pack()
        self.txtEntrada.place(x=25, y=70)

        # LABEL QUE NOS INDICA LA POSICION
        self.lblPosition = Label(self.window, text=f"Posicion (V, H): --")
        self.lblPosition.place(x=300, y=430)

        # BOTON PARA ANALISIS
        self.btn = Button(self.window, text="Analizar Archivo", bg='#1A5276', fg="white",
                          command=self.runAnalisis)  # boton ANALYZE
        self.btn.place(x=620, y=430)

        # --------------------  PROPIEDADES DEL TXT SALIDA  -----------------------------------
        self.lblSalida = Label(self.window, text=f"Salida: ")
        self.lblSalida.place(x=780, y=40)
        self.txtSalida = scrolledtext.ScrolledText(self.window, width=66, height=22, bg='#1C1D40', foreground="#FFFFFF",
                                                   selectbackground="#0256FF", insertbackground='#F8C471')  # 80,25
        self.txtSalida.pack()
        self.txtSalida.place(x=775, y=70)

        # -------------------------------- COLOCANDO EL NOTEBOOK ------------------------------

        self.notebook_tablas = ttk.Notebook(self.window)
        self.notebook_tablas.pack()
        self.notebook_tablas.place(x=150, y=470)

        # -------------------------------- COLOCANDO TABLAS ---------------------------
        # Colocando estilo
        estilo = ttk.Style()
        estilo.theme_use("default")  # alt, clam, default, vista
        estilo.configure("mystyle.Treeview",
                         background="silver",  # Fondo de la tabla
                         rowheight=20,  # Altura de la celda
                         foreground="#FF00F3",
                         fieldbackground="#1C1D40")  # Orilla de la tabla

        # Cambiando el estilo de seleccion
        estilo.map('mystyle.Treeview', background=[('selected', 'green')])
        # ---------------- TABLA DE SIMBOLOS -----------------
        # Relaizando un Frame
        self.frame_SymTable = Frame(self.notebook_tablas, width=500, height=175, bg="white")    # Agregando el Frame al Window
        self.frame_SymTable.pack(fill="both", expand=1)
        self.notebook_tablas.add(self.frame_SymTable, text="Tabla Simbolos")


        # Definiendo las columnas de la tabla
        columnss = ("Identificador", "Tipo", "Tipo2", "Entorno", "Valor", "Linea", "Columna")

        # Realizando la tabla con ttk.Treeview
        self.table_symbolTable = ttk.Treeview(self.frame_SymTable, height=8, columns=columnss, show='headings', style="mystyle.Treeview")
        self.table_symbolTable.pack(side=LEFT)   # Pegando la tabla hacia la izquierda del Frame realizado arriba

        # Configurando los encabezador Texto y Ancho del encabezado
        self.table_symbolTable.column("Identificador", anchor=W, width=100)
        self.table_symbolTable.column("Tipo", anchor=W, width=200)
        self.table_symbolTable.column("Tipo2", anchor=W, width=200)
        self.table_symbolTable.column("Entorno", anchor=W, width=200)
        self.table_symbolTable.column("Valor", anchor=W, width=200)
        self.table_symbolTable.column("Linea", anchor=W, width=70)
        self.table_symbolTable.column("Columna", anchor=W, width=70)  # Total: 1040

        # Colocando los encabezados en la tabla, texto de los encabezador y como iran colocados
        self.table_symbolTable.heading("Identificador", text="Identificador", anchor=CENTER)
        self.table_symbolTable.heading("Tipo", text="Tipo", anchor=CENTER)
        self.table_symbolTable.heading("Tipo2", text="Tipo2", anchor=CENTER)
        self.table_symbolTable.heading("Entorno", text="Entorno", anchor=CENTER)
        self.table_symbolTable.heading("Valor", text="Valor", anchor=CENTER)
        self.table_symbolTable.heading("Linea", text="Linea", anchor=CENTER)
        self.table_symbolTable.heading("Columna", text="Columna", anchor=CENTER)

        # Realizando Scrollbar del frame para la tabla
        sb = Scrollbar(self.frame_SymTable, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)     # Pegando el scroll de lado derecho de la tabla

        # Configurando el scroll en la tabla verticalmente
        self.table_symbolTable.config(yscrollcommand=sb.set)
        sb.config(command=self.table_symbolTable.yview)

        # --------------------------------------------------- TABLA DE ERRORES ---------------------------------------
        # Relaizando un Frame
        self.frame_ErrorTable = Frame(self.notebook_tablas, width=500, height=175, bg="white")  # Agregando el Frame al Window
        self.frame_ErrorTable.pack(fill="both", expand=1)
        self.notebook_tablas.add(self.frame_ErrorTable, text="Tabla Errores")


        # Definiendo las columnas de la tabla
        columnss2 = ("Numero", "Tipo Error", "Descripcion", "Linea", "Columna")

        # Realizando la tabla con ttk.Treeview

        self.table_errorTable = ttk.Treeview(self.frame_ErrorTable, height=8, columns=columnss2, show='headings', style="mystyle.Treeview")
        self.table_errorTable.pack(side=LEFT)  # Pegando la tabla hacia la izquierda del Frame realizado arriba

        # Configurando los encabezador Texto y Ancho del encabezado
        self.table_errorTable.column("Numero", anchor=W, width=150)
        self.table_errorTable.column("Tipo Error", anchor=W, width=245)
        self.table_errorTable.column("Descripcion", anchor=W, width=245)
        self.table_errorTable.column("Linea", anchor=W, width=200)
        self.table_errorTable.column("Columna", anchor=W, width=200)  # Total: 1040

        # Colocando los encabezados en la tabla, texto de los encabezador y como iran colocados
        self.table_errorTable.heading("Numero", text="#", anchor=CENTER)
        self.table_errorTable.heading("Tipo Error", text="Tipo Error", anchor=CENTER)
        self.table_errorTable.heading("Descripcion", text="Descripcion", anchor=CENTER)
        self.table_errorTable.heading("Linea", text="Linea", anchor=CENTER)
        self.table_errorTable.heading("Columna", text="Columna", anchor=CENTER)

        # Realizando Scrollbar del frame para la tabla
        sb2 = Scrollbar(self.frame_ErrorTable, orient=VERTICAL)
        sb2.pack(side=RIGHT, fill=Y)  # Pegando el scroll de lado derecho de la tabla

        # Configurando el scroll en la tabla verticalmente
        self.table_errorTable.config(yscrollcommand=sb2.set)
        sb.config(command=self.table_errorTable.yview)

        # #  --------------------------- COLORES ---------------------------
        self.txtEntrada.text.tag_config('c_reservada', foreground='#00BFFF') # blue
        self.txtEntrada.text.tag_config('c_cadena', foreground='#FFA500')  # orange
        self.txtEntrada.text.tag_config('c_numero', foreground='#FF00F7')  # purple
        self.txtEntrada.text.tag_config('c_comentario', foreground='#ACACAC')  # gris#BABABA#C5C5C5
        self.txtEntrada.text.tag_config('c_concatenacion', foreground='#00FF36')
        self.txtEntrada.text.tag_config('c_otro', foreground='#FFFFFF')  # negro

        self.txtEntrada.text.bind("<Button-1>", self.getInfo) # Clik derecho
        self.txtEntrada.text.bind("<Button-2>", self.getInfo) # Click izquierdo
        self.txtEntrada.text.bind("<Button-3>", self.getInfo) # ruedita

        # self.txtEntrada.text.bind('<KeyRelease>', self.actualizar_pintar)

        # self.txtEntrada.index('end')

        # Dispara la interfaz y la mantiene abierta
        self.window.mainloop()

    # ABRIR PDF y HTML EN EL NAVEGADOR
    def menu_open_pdfhtml(self):
        pathFile = filedialog.askopenfilename(title="Seleccione archivo (Abrir Navegador)", filetypes=
        (("PDF Files", "*.pdf"), ("HTML Files", "*.html"), ("SVG Files", "*.svg")))
        if pathFile != "":
            print("Su archivo es " + pathFile)
            webbrowser.open_new_tab(pathFile)
        else:
            print("No se ha seleccionado ningun HTML o PDF. :)")

    # Dispara el Filechooser
    def menu_Open_File(self):
        pathFile = filedialog.askopenfilename(title="Seleccione archivo", filetypes=
        (("jpr files", "*.jpr"), ("All Files", "*.*")))

        if pathFile != '':
            self.last_Open_Path = pathFile

            baseNameFile = os.path.basename(pathFile)               # Obteniendo el nombre base del archivo
            # archi1 = open(pathFile, "r", encoding="windows-1252")          # Lectura del archivo
            archi1 = open(pathFile, "r", encoding="utf-8")  # Lectura del archivo
            contenido = archi1.read()                               # Obteniendo el texto / contenido
            archi1.close()

            self.updateLabelName(baseNameFile)                      # Actualizar el label de nombre del archivo
            self.txtEntrada.text.delete("1.0", END)                 # Borramos la consola
            self.cadena_entrada = contenido
            # self.txtEntrada.text.insert("1.0", contenido)                # Insertamos el contenido del path
            for s in self.pintar_palabras(contenido):
                self.txtEntrada.text.insert(INSERT, s[1], s[0])

    def menu_Open_File2(self):
        pathFile = filedialog.askopenfilename(title="Seleccione archivo", filetypes=
        (("jpr files", "*.jpr"), ("All Files", "*.*")))

        if pathFile != '':
            self.last_Open_Path = pathFile

            baseNameFile = os.path.basename(pathFile)               # Obteniendo el nombre base del archivo
            # archi1 = open(pathFile, "r", encoding="windows-1252")          # Lectura del archivo
            archi1 = open(pathFile, "r", encoding="utf-8")  # Lectura del archivo
            contenido = archi1.read()                               # Obteniendo el texto / contenido
            archi1.close()

            self.updateLabelName(baseNameFile)                      # Actualizar el label de nombre del archivo
            self.txtEntrada.text.delete("1.0", END)
            self.cadena_entrada = contenido# Borramos la consola
            self.txtEntrada.text.insert("1.0", contenido)                # Insertamos el contenido del path

    def menu_New_Option(self):
        self.txtEntrada.text.delete("1.0", END)  # limpio entrada de texto
        self.txtSalida.delete("1.0", END)  # limpio salida
        self.last_Open_Path = ""  # limpio el path guardado
        self.last_Open_Extension = ""  # Limpiar la extension
        self.updateLabelName("Archivo Nuevo.")
        self.ast_tree = None

    # Crear un archivo de extension en el nombre
    def create_File(self, path, textoCorregido):
        # C:/Users/Isaac/Desktop/nombrexd.txt Ejemplo de como se pasa el path para crear el archivo
        # PATHL: C:\Users\Isaac\Desktop\Destino Prueba\CorregidoHtml.html
        file = open(f"{path}", "w", encoding="utf-8")
        file.write(f"{textoCorregido}")
        file.close()

    def saveFile_PreviousOpen(self):
        if self.last_Open_Path != "":
            entradaTexto = self.txtEntrada.text.get("1.0", END)
            self.create_File(self.last_Open_Path, entradaTexto)
        else:
            print("No hay path aun!... >:[")

    # Para colocarle un nombre y extension al archivo que quiero guardar
    def saveFile_SaveAs(self):
        nameFile = filedialog.asksaveasfilename(title="Seleccione archivo", defaultextension='.jpr',
                                                filetypes=[("jpr files", '*.jpr'), ("txt files", '*.txt')])
        if nameFile != '':
            extension = os.path.splitext(nameFile)[1]
            baseNameFile = os.path.basename(nameFile)  # Obteniendo el nombre base del archivo

            self.last_Open_Extension = extension
            self.last_Open_Path = nameFile
            print(f"\nSu archivo tiene extension: {extension}\nSu archivo tiene nombre {nameFile}")
            self.updateLabelName(baseNameFile)
            entradaTexto = self.txtEntrada.text.get("1.0", END)
            self.create_File(nameFile, entradaTexto)
        else:
            print("No se escogio o se cancelo!.")

    def limpiarTablaSimbolo(self):
        for record in self.table_symbolTable.get_children():
            self.table_symbolTable.delete(record)

    def limpiarTablaErrores(self):
        for record in self.table_errorTable.get_children():
            self.table_errorTable.delete(record)


    def reporte_errores(self):
        print("----------------------Generando reporte de errores ----------------------")
        nameFile = filedialog.asksaveasfilename(title="Seleccione archivo", defaultextension='.html',
                                                filetypes=[("html files", '*.html')])

        if (self.ast_tree != "") and (self.ast_tree is not None):
            file = open(f"{nameFile}", "w")
            file.write(f"<!DOCTYPE html>\n"
                       f"<html lang = \"en\">\n"
                       f"<head>\n"
                       f"   <meta charset = \"UTF-8\">\n"
                       f"   <title> Proyecto 1 OLC1 JPR - 201807316 </title>\n"
                       f"   <link rel = \"stylesheet\" href = \"tabla.css\">\n"
                       f"</head>\n"
                       f"<body>\n"
                       f"   <div id= \"main-container\">\n"
                       f"   <H2 align=\"center\" style=\"color: #FFFFFF;\">Reporte de Errores</H2>\n"
                       f"   <table>\n"
                       f"       <thead>\n"
                       f"       <tr>\n"
                       f"       <th>No.</th><th>Tipo</th><th>Descripcion</th><th>Linea</th><th>Columna</th>\n"
                       f"       </tr>\n"
                       f"       </thead>\n"
                       f"\n")

            contador_errores = 1
            for error in self.ast_tree.getExcepciones():
                if error.getTipo() == "lexico":
                    descripcion = error.getDescripcion()
                    fila = error.getFila()
                    columna = error.getColumna()
                    file.write(
                        f"       <tr>\n"
                        f"           <td>{contador_errores}</td>\n"
                        f"           <td>Lexico</td>\n"
                        f"           <td>{descripcion}</td>\n"
                        f"           <td>{fila}</td>\n"
                        f"           <td>{columna}</td>\n"
                        f"       </tr>\n"
                    )
                    contador_errores += 1

            for error in self.ast_tree.getExcepciones():
                if error.getTipo() == "sintactico":
                    descripcion = error.getDescripcion()
                    fila = error.getFila()
                    columna = error.getColumna()
                    file.write(
                        f"       <tr>\n"
                        f"           <td>{contador_errores}</td>\n"
                        f"           <td>Sintactico</td>\n"
                        f"           <td>{descripcion}</td>\n"
                        f"           <td>{fila}</td>\n"
                        f"           <td>{columna}</td>\n"
                        f"       </tr>\n"
                    )
                    contador_errores += 1
            for error in self.ast_tree.getExcepciones():
                if error.getTipo().lower() == "Semantico".lower():
                    descripcion = error.getDescripcion()
                    fila = error.getFila()
                    columna = error.getColumna()
                    file.write(
                        f"       <tr>\n"
                        f"           <td>{contador_errores}</td>\n"
                        f"           <td>Semantico</td>\n"
                        f"           <td>{descripcion}</td>\n"
                        f"           <td>{fila}</td>\n"
                        f"           <td>{columna}</td>\n"
                        f"       </tr>\n"
                    )
                    contador_errores += 1

            file.write(f""
                       f"       </table>\n"
                       f"   </div>\n"
                       f"</body>\n"
                       f"</html>\n"
                       f"")
            file.close()
            print(nameFile)
            webbrowser.open_new_tab(nameFile)
        else:
            print("Falta analizar una entrada!")

    def llenar_TablaSimbolos(self):
        self.limpiarTablaSimbolo()
        print("Reporte tabla")
        contadorVar = 0
        for variable in lista_variables:
            self.table_symbolTable.insert(parent='', index='end', iid=contadorVar, text="Parent",
                                         values=(
                                         f"{variable['identificador']}",
                                         f"{variable['tipo1']}",
                                         f"{variable['tipo2']}",
                                         f"{variable['entorno']}",
                                         f"{variable['valor']}",
                                         f"{variable['linea']}",
                                         f"{variable['columna']}")
                                          )
            contadorVar += 1

    def llenar_TablaErrores(self):
        self.limpiarTablaErrores()
        contador_errores = 0
        if (self.ast_tree != "") and (self.ast_tree is not None):
            for error in self.ast_tree.getExcepciones():
                if error.getTipo().lower() == "lexico".lower():
                    contador_errores += 1
                    descripcion = error.getDescripcion()
                    fila = error.getFila()
                    columna = error.getColumna()
                    self.table_errorTable.insert(parent='', index='end', iid=contador_errores, text="Parent",
                                                 values=(f"{contador_errores}", f"Lexico", f"{descripcion}", f"{fila}", f"{columna}"))

            for error in self.ast_tree.getExcepciones():
                if error.getTipo().lower() == "sintactico".lower():
                    contador_errores += 1
                    descripcion = error.getDescripcion()
                    fila = error.getFila()
                    columna = error.getColumna()
                    self.table_errorTable.insert(parent='', index='end', iid=contador_errores, text="Parent",
                                                 values=(f"{contador_errores}", f"Sintactico", f"{descripcion}", f"{fila}",
                                                         f"{columna}"))

            for error in self.ast_tree.getExcepciones():
                if error.getTipo().lower() == "Semantico".lower():
                    contador_errores += 1
                    descripcion = error.getDescripcion()
                    fila = error.getFila()
                    columna = error.getColumna()
                    self.table_errorTable.insert(parent='', index='end', iid=contador_errores, text="Parent",
                                                 values=(f"{contador_errores}", f"Semantico", f"{descripcion}", f"{fila}", f"{columna}"))
        else:
            print("Falta analizar una entrada!")

    def reporte_arbol(self):
        realizar_dot(self.ast_tree)

    def pintar_palabras(self, entrada):
        entrada = entrada + "    \n"
        lista_general = []
        valor_con = ""
        contador = 0

        while contador < len(entrada):
            if re.search(r"[0-9]", entrada[contador]):
                valor_con += entrada[contador]
                contador += 1
                while contador != len(entrada):
                    if re.search(r"[0-9]", entrada[contador]):
                        valor_con += entrada[contador]
                        contador += 1
                    elif entrada[contador] == ".":
                        valor_con += entrada[contador]
                        contador += 1
                    if (not entrada[contador].isnumeric()) and (entrada[contador] != "."):
                        lista_in = ["c_numero", valor_con]
                        lista_general.append(lista_in)
                        valor_con = ""
                        contador -= 1
                        break
                if len(valor_con) != 0:
                    lista_in = ["c_numero", valor_con]
                    lista_general.append(lista_in)
                    valor_con = ""

            # Si el caracter leido es una letra o numero, concatenar  ID
            elif re.search(r"[a-zA-Z0-9_]", entrada[contador]):
                valor_con += entrada[contador]
                contador += 1
                while contador != len(entrada):
                    if contador + 1 != len(entrada):
                        if not (re.search(r"[a-zA-Z0-9_]", entrada[contador + 1])):
                            valor_con += entrada[contador]
                            lista_in =["c_concatenacion", valor_con]
                            lista_general.append(lista_in)
                            valor_con = ""
                            break
                    valor_con += entrada[contador]
                    contador += 1
                if len(valor_con) != 0:
                    lista_in = ["c_concatenacion", valor_con]
                    lista_general.append(lista_in)
                    valor_con = ""

            # Si es una cadena
            elif entrada[contador] == "\"":
                valor_con += entrada[contador]  # concateno de nuevo al val para la cadena
                contador += 1                   # Una posicion despues del "
                while contador != len(entrada):
                    # if entrada[contador] == "\"" or (contador == len(entrada) - 1):   # En caso venga la terminacion de la cadena
                    if re.search(r"""\"(\\"|\\'|\\\\|\\n|\\t|\\r|[^\\\'\"])*?\"""", valor_con) and (contador <= (len(entrada)) - 1):
                        lista_in = ["c_cadena", valor_con]
                        lista_general.append(lista_in)
                        valor_con = ""
                        contador -= 1
                        break
                    valor_con += entrada[contador]
                    contador += 1
                if len(valor_con) != 0:
                    lista_in = ["c_cadena", valor_con]
                    lista_general.append(lista_in)
                    valor_con = ""
            # En dado caso venga un caracter
            elif entrada[contador] == "\'":
                valor_con += entrada[contador]  # concateno de nuevo al val para la cadena
                contador += 1
                while contador != len(entrada):
                    if re.search(r"""\'(\\'|\\\\|\\n|\\t|\\r|\\"|.)?\'""", valor_con) and (contador <= (len(entrada)) - 1):
                    # if entrada[contador] == "\'":  # En caso venga la terminacion de la cadena
                        lista_in = ["c_cadena", valor_con]
                        lista_general.append(lista_in)
                        valor_con = ""
                        contador -= 1
                        break
                    valor_con += entrada[contador]
                    contador += 1
                if len(valor_con) != 0:
                    lista_in = ["c_cadena", valor_con]
                    lista_general.append(lista_in)
                    valor_con = ""
            # en dado caso venga un comentario
            elif entrada[contador] == "#":
                valor_con += entrada[contador]  # concateno de nuevo al val para la cadena
                contador += 1
                if entrada[contador] == "*":  # Entonces buscara un multilinea
                    while contador != len(entrada):
                        if entrada[contador] == "*" and (contador <= len(entrada) - 1):
                            valor_con += entrada[contador]
                            contador += 1
                            valor_con += entrada[contador]
                            if re.search(r"#*\*(.|\n)*?\*#", valor_con):
                                lista_in = ["c_comentario", valor_con]
                                lista_general.append(lista_in)
                                valor_con = ""
                                break
                        valor_con += entrada[contador]
                        contador += 1
                else:
                    while contador != len(entrada):
                        if entrada[contador] == "\n" and (contador <= len(entrada) - 1):
                            valor_con += entrada[contador]
                            if re.search(r'#.*\n', valor_con):
                                lista_in = ["c_comentario", valor_con]
                                lista_general.append(lista_in)
                                valor_con = ""
                                break
                        valor_con += entrada[contador]
                        contador += 1
                if len(valor_con) != 0:
                    lista_in = ["c_comentario", valor_con]
                    lista_general.append(lista_in)
                    valor_con = ""

            else:
                # Validar la concatenacion
                if len(valor_con) != 0:
                    lista_in = ["c_otro", valor_con]
                    lista_general.append(lista_in)
                # En este momento se ha encontrado con algun otro signo
                lista_in = ["c_otro", entrada[contador]]
                lista_general.append(lista_in)
                valor_con = ""
            contador += 1

        # Se revisa en la lista de reservadas
        for tok in lista_general:
            if (tok[1].lower() == "if") or (tok[1].lower() == "var") or (tok[1].lower() == "false") or \
                    (tok[1].lower() == "true") or (tok[1].lower() == "print") or (tok[1].lower() == "else") or\
                    (tok[1].lower() == "switch") or (tok[1].lower() == "case") or (tok[1].lower() == "default") or\
                    (tok[1].lower() == "while") or (tok[1].lower() == "for") or (tok[1].lower() == "continue") or\
                    (tok[1].lower() == "break") or (tok[1].lower() == "return") or (tok[1].lower() == "func") or\
                    (tok[1].lower() == "read") or (tok[1].lower() == "main"):
                tok[0] = "c_reservada"
        return lista_general


# ------------------------ METODOS PARA LA LINEAS DEL EDITOR  ----------------------------
# -------- CLASE PARA PODER COLOCAR NUMEROS EN LA CONSOLA DE ENTRADA -----------
class ScrollTextUwU(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        # bg -> color de fondo --- foreground -> color al texto --- selectbrackgroud -> color a lo que seleccione ---
        # inserbackgroud -> color al puntero
        self.text = tk.Text(self, bg='#242B51', foreground="#FFFFFF", selectbackground="#0256FF",
                            insertbackground='#F8C471',  width=85, height=22)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        # self.numero_lineas = TextoLinea(self, width=35, bg='#D5D5D5')
        self.numero_lineas = TextoLinea(self, width=35, bg='#1C1D40')
        self.numero_lineas.attach(self.text)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.numero_lineas.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numero_lineas.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numero_lineas.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numero_lineas.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numero_lineas.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numero_lineas.redraw()

class TextoLinea(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs, highlightthickness=0)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")
        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill="#FFFFFF")
            i = self.textwidget.index("%s+1line" % i)