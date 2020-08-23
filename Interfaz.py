from tkinter import Tk, Menu, messagebox, filedialog, ttk, Label, scrolledtext, INSERT, END, Button, Scrollbar, RIGHT, Y, Frame, Canvas, HORIZONTAL, VERTICAL, simpledialog
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import re
from Analizador import Analizador

class T(Analizador):
    archivo = ""
    

    #***********************************
    def analizar(self):
        t = self.editor.get(1.0, END)
        Analizador().INICIO(t)   
        ListaErrores = Analizador().getErrores()
        V = "Finalizo el analisis\n\n"
        if not ListaErrores:
            self.consola.insert(INSERT, V)
            messagebox.showinfo("Exito", "El analisis no tuvo errores")
        else:
            self.consola.insert(INSERT, V)
            e = "Errores en:\n"
            self.consola.insert(INSERT, e)
            for error in ListaErrores:
                imprimir = "Fila: " + str(error[0]) + ", Columna: " + str(error[1]) + ", Caracter: " + str(error[2]) + "\n"
                self.consola.insert(INSERT, imprimir)
            messagebox.showerror("Error", "El analisis termino con errores:")
    
    #END
    #*********************************************
    

    def nuevo(self):
        global archivo
        self.editor.delete(1.0, END)#ELIMINAR EL CONTENIDO
        archivo = ""

    def abrir(self):
        global archivo
        archivo = filedialog.askopenfilename(title = "Abrir Archivo")
        entrada = open(archivo)
        content = entrada.read()

        self.editor.delete(1.0, END)
        self.editor.insert(INSERT, content)
        self.editor.insert(1.0,"1)       ")
        entrada.close()

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
        guardar = filedialog.asksaveasfilename(title = "Guardar Archivo", initialdir = "C:/")
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


