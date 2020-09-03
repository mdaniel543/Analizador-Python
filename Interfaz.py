from tkinter import Tk, Menu, messagebox, filedialog, ttk, Label, scrolledtext, INSERT, END, Button, Scrollbar, RIGHT, Y, Frame, Canvas, HORIZONTAL, VERTICAL, simpledialog
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
from Analizador import Analizador
from AnalizadorCSS import AnalizadorCSS
from AnalizadorHTML import AnalizadorHTML
from Sintactico import Sintactico

class T(Analizador, AnalizadorCSS, AnalizadorHTML, Sintactico):
    archivo = ""
    ti = ""
    u = ""
    Nombre = ""
    counter = 0
    reservadasa = ['.js','.css', '.html','.rmt']
    #***********************************
    def analizar(self):
        global ti, u, Nombre
        ListaErrores = self.Tanalisis()
        V = "Finalizo el analisis de "+ ti +"\n\n"
        F = "Tomamos de ruta para guardar : " + self.RUTA + "\\"+ "\n\n"
        if not ListaErrores:
            self.consola.insert(INSERT, V)
            self.consola.insert(INSERT, F)
            messagebox.showinfo("Exito", "El analisis del archivo "+ ti +" no tuvo errores")
            value = messagebox.askquestion("Guardar", "Desea guardar el archivo a la ruta establecida:")
            if value :
                if  not os.path.exists(self.RUTA):
                    os.system("mkdir " + self.RUTA)
                if ti == ".js":
                    if not os.path.exists(self.rr):
                        os.system("mkdir " + self.rr)
                    fguardar = open(self.rr + self.Nombre + ti, "w+")
                    fguardar.write(self.editor.get(1.0, END))
                    fguardar.close()
                    messagebox.showinfo("Exito", "Archivo guardado "+ self.Nombre + ti + " en ruta con exito")
                    return
                elif ti == ".css":
                    if not os.path.exists(self.rrs):
                        os.system("mkdir " + self.rrs)
                    fguardar = open(self.rrs + self.Nombre + ti, "w+")
                    fguardar.write(self.editor.get(1.0, END))
                    fguardar.close()
                    messagebox.showinfo("Exito", "Archivo guardado "+ self.Nombre + ti + " en ruta con exito")
                    return
                fguardar = open(self.RUTA + "\\" + self.Nombre + ti, "w+")
                fguardar.write(self.editor.get(1.0, END))
                fguardar.close()
                messagebox.showinfo("Exito", "Archivo guardado "+ self.Nombre + ti + " en ruta con exito")

        else:
            self.consola.insert(INSERT, V)
            self.consola.insert(INSERT, F)
            e = "Errores en:\n"
            self.consola.insert(INSERT, e)
            for error in ListaErrores:
                imprimir = "Fila: " + str(error[0]) + ", Columna: " + str(error[1]) + ", Caracter: " + str(error[2]) + "\n"
                self.consola.insert(INSERT, imprimir)
            messagebox.showerror("Error", "El analisis del archovo "+ ti +" termino con errores:")

        ListaErrores.clear()

    def Tanalisis(self):
        global ti
        if ti == ".js":
            t = self.editor.get(1.0, END)
            self.INICIO(t)
            ListaR = self.getErrores()    
            return ListaR
        elif ti == ".css":
            m = self.editor.get(1.0, END)
            self.INICIOCSS(m)
            ListaC = self.getErroresCSS()
            return ListaC
        elif ti == ".html":
            b = self.editor.get(1.0, END)
            self.INICIOHTML(b)
            ListaH = self.getErroresHTML()
            return ListaH
        elif ti == ".rmt":
            g = self.editor.get(1.0, END)
            self.INICIORMT(g)
            Posible = self.getErroresRMT()
            return Posible
        else:
            print("No ha reconocido archivo")
        
    #END
    #*********************************************

    def nuevo(self):
        global archivo
        self.editor.delete(1.0, END)#ELIMINAR EL CONTENIDO
        archivo = ""

    def abrir(self):
        global archivo, counter
        archivo = filedialog.askopenfilename(title = "Abrir Archivo")
        entrada = open(archivo)
        content = entrada.read()
        self.counter = 0
        nuevo = self.comp(archivo)
        self.counter = 0
        if nuevo:
            self.editor.delete(1.0, END)
            self.editor.insert(INSERT, content)
        else:
            messagebox.showerror("Error", "Archivo ingresado desconocido")
        nuevo = False
        entrada.close()
#************************************************************
    def comp(self, texto):
        global ti
        ti = self.tipo(texto)
        for reservada in self.reservadasa:
            if reservada == ti:
                return True
        return False

    def tipo(self, text):
        print(text)
        global counter, Nombre
        con = ""
        while self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit():
                self.Nombre += text[self.counter]
                self.counter += 1 
            elif text[self.counter] == "/":
                self.Nombre = ""
                self.counter += 1 
            elif text[self.counter] == ".": 
                con = self.nombre(text, text[self.counter]) 
                print(self.Nombre)   
                return con
                break
            else:
                self.counter += 1  
        return con
        
    def nombre(self, text, word):
        global counter
        self.counter += 1
        if self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit():
                return self.nombre(text, word + text[self.counter])
            else:
                return word
        else: 
            return word
#**************************************************************


        
#**************************************************************
    def salir(self):
        value = messagebox.askokcancel("Salir", "Está seguro que desea salir?")
        if value :
            root.destroy()

    def guardarArchivo(self):
        global archivo
        if archivo == "":
            guardarComo()
        else:
            guardarc = open(archivo, "w")
            guardarc.write(self.editor.get(1.0, END))
            guardarc.close()

    def guardarComo(self):
        global archivo
        guardar = filedialog.asksaveasfilename(title = "Guardar Archivo")
        fguardar = open(guardar, "w+")
        fguardar.write(self.editor.get(1.0, END))
        fguardar.close()
        archivo = guardar
    #END

    def __init__(self, root):
        root.title("Proyecto 1") 
        root.configure(background = "lightgray")
        self.barraMenu = Menu(root)
        root.config(menu = self.barraMenu, width = 1375, height = 600)

        self.archivoMenu = Menu(self.barraMenu, tearoff=0)
        self.archivoMenu.add_command(label = "Nuevo", command = self.nuevo)
        self.archivoMenu.add_command(label = "Abrir", command = self.abrir)
        self.archivoMenu.add_command(label = "Guardar", command = self.guardarArchivo)
        self.archivoMenu.add_command(label = "Guardar Como...", command = self.guardarComo)
        self.archivoMenu.add_separator()
        self.archivoMenu.add_command(label = "Salir", command = self.salir)

        self.barraMenu.add_cascade(label = "Archivo", menu = self.archivoMenu)
        self.barraMenu.add_separator()
        self.barraMenu.add_command(label = "Ejecutar analisis",  command = self.analizar)
        self.barraMenu.add_separator()
        self.barraMenu.add_command(label = "Reportes",  command = self.salir)
        self.barraMenu.add_command(label = "Salir",  command = self.salir)

        frame = Frame(root, bg="lightgray")
        canvas = Canvas(frame, bg="lightgray")
        scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
        scroll = Frame(canvas, bg="lightgray")

        scroll.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set, width = 1375, height = 600)

        Label(scroll,text='ML WEB EDITOR', font = ("Arial", 16), background='lightgray', foreground = "black").grid(row=0,column=1)

        Label(scroll,text='Lectura de archivo', font = ("Arial", 14), background='lightgray', foreground = "black").grid(row=1,column=0)
        Label(scroll,text='Consola', font = ("Arial", 14), background='lightgray', foreground = "black").grid(row=1,column=2)

        self.editor = scrolledtext.ScrolledText(scroll, undo = True, width = 80, height = 30, font = ("Arial", 10), background = 'lightblue',  foreground = "black")

        self.editor.grid(row = 2, column = 0)

        self.consola = scrolledtext.ScrolledText(scroll, undo = True, width = 80, height = 30, font = ("Arial", 10), background = 'black',  foreground = "white")

        self.consola.grid(row = 2, column = 2)

        frame.grid(sticky='news')
        canvas.grid(row=0,column=1)
        scrollbar.grid(row=0, column=2, sticky='ns')
        self.editor.focus()
        self.consola.focus()

###################################################################################################


if __name__ == '__main__':
    root = Tk()
    app = T(root)
    root.mainloop()


