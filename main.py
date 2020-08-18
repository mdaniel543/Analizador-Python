from os import system
from io import open

Encabezado = """USAC
Facultad de Ingenieria
Escuela de Ciencias y sistemas
Organizacion de Lenguajes y Compiladores 1\n
\t\t PROYECTO 1 \n
"""
print(Encabezado)


Menu = """---------------------------------------------

\t MENU: 
1. Nuevo 
2. Abrir
3. Guardar
4. Guardar como
5. Ejecutar analisis
6. Salir
"""


def abrirarchivo():
    Abrir = """ 
    *****************************************

    Que tipo de archivo desea abrir:
    1) .js
    2) .css
    3) .html
    4) .rmt
    """
    print(Abrir)
    a = int(input("Ingrese numero del archivo que desea abrir: "))
    print("\n **************************************** \n")
    print("\t SU ARCHIVO CONTIENE: \n\n")
    if a == 1:
        archivoJS = open("comentario.js", "r")
        texto = archivoJS.read()
        archivoJS.close()
        print(texto)
    else:
        print("Incorrecto")




val = True;
while val == True:
    print(Menu)
    ingreso = int(input("Ingrese numero de la accion que desea realizar: "))
    
    if ingreso == 1:
        print(1)
    elif ingreso == 2:
        abrirarchivo()
    elif ingreso == 3:
        print(3)
    elif ingreso == 4:
        print(4)
    elif ingreso == 5:
        print(5)
    elif ingreso == 6:
        print(6)
        val = False;
    else:
        print("Numero de accion invalido! ")





    



