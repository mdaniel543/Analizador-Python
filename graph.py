import os
from graphviz import Digraph

class graph:
    
    def inicioG(self, listado, ruta):
        self.estados = []
        self.cont = -1
        i = -1

        # [ nombre, elementos, transiciones, Aceptacion]
        for lista in listado:
            i += 1
            self.cont += 1
            if self.cont == 0:
                self.estados.append(["S"+str(self.cont),  [], False]) 
                self.cont += 1
                self.estados.append(["S"+str(self.cont),  [], True])
            else: 
                self.estados.append(["S"+str(self.cont),  [], True]) 

            self.estados[i][1].append([self.estados[i][0], lista[2], self.estados[i+1][0]])

            
            if lista[2] == 'Comentario Multilinea':
                self.estados[i][1].append([self.estados[i+1][0], lista[2], self.estados[i+1][0]])
            elif lista[2] == 'Ruta':
                self.estados[i][1].append([self.estados[i+1][0], lista[2], self.estados[i+1][0]])
            else:
                self.estados[i][1].append([self.estados[i+1][0], lista[3], self.estados[i+1][0]])
        self.grafo(ruta)
    #END


    def grafo(self, ruta):
        dot = Digraph(comment='Estados')
        dot.attr('node', shape='circle')

        # Creamos los nodos
        for e in self.estados:
            dot.node(e[0],e[0])
            if e[2]:
                dot.node(e[0], shape='doublecircle')

        #Creamos las transiciones
        for e in self.estados:
            for t in e[1]:
                dot.edge(t[0], t[2], label=t[1])

        dot.render(ruta + "\\ Reporte.gv" , view=False)
        print("Grafo de Estados Generado")
        os.startfile(ruta + "\\ Reporte.gv"+".pdf")

