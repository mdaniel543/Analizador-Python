import re

class Analizador:
    linea = 0
    columna = 0
    counter = 0
    Errores = []
    reservadas = ['if','while','do','switch','else','case', 'for', 'var']
    signos = {"PUNTOCOMA":';', "LLAVEA":'{', "LLAVEC":'}', "PARA":'\(', "PARC":'\)', "IGUAL":'='}

    def scanner(self, text):
        global linea, columna, counter, Errores
        linea = 1
        columna = 1
        listaTokens = []

        while self.counter < len(text):
            if re.search(r"[A-Za-z]", text[self.counter]): #IDENTIFICADOR
                listaTokens.append(self.StateIdentifier(linea, columna, text, text[self.counter]))
            elif re.search(r"[0-9]", text[self.counter]): #NUMERO
                listaTokens.append(self.StateNumber(linea, columna, text, text[self.counter]))
                
            elif re.search(r"[\n]", text[self.counter]):#SALTO DE LINEA
                self.counter += 1
                linea += 1
                columna = 1 
            elif re.search(r"[ \t]", text[self.counter]):#ESPACIOS Y TABULACIONES
                self.counter += 1
                columna += 1 
            else:
                #SIGNOS
                isSign = False
                for clave in self.signos:
                    valor = self.signos[clave]
                    if re.search(valor, text[self.counter]):
                        listaTokens.append([linea, columna, clave, valor.replace('\\','')])
                        self.counter += 1
                        columna += 1
                        isSign = True
                        break
                if not isSign:
                    self.Errores.append([linea, columna, text[self.counter]])
                    columna += 1
                    self.counter += 1
        return listaTokens

    #[linea, columna, tipo, valor]

    def StateIdentifier(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"[a-zA-Z_0-9]", text[self.counter]):#IDENTIFICADOR
                return self.StateIdentifier(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'identificador', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [line, column, 'identificador', word]
        
    def StateNumber(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):#ENTERO
                return self.StateNumber(line, column, text, word + text[self.counter])
            elif re.search(r"\.", text[self.counter]):#DECIMAL
                return self.StateDecimal(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'integer', word]
                #agregar automata de numero en el arbol, con el valor
        else:
            return [line, column, 'integer', word]

    def StateDecimal(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if re.search(r"[0-9]", text[self.counter]):#DECIMAL
                return self.StateDecimal(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'decimal', word]
                #agregar automata de decimal en el arbol, con el valor
        else:
            return [line, column, 'decimal', word]

    def Reserved(self, TokenList):
        for token in TokenList:
            if token[2] == 'identificador':
                for reservada in self.reservadas:
                    palabra = r"^" + reservada + "$"
                    if re.match(palabra, token[3], re.IGNORECASE):
                        token[2] = 'reservada'
                        break

    def INICIO(self, texto):
        print(texto)
        tokens = self.scanner(texto)
        self.Reserved(tokens)
        for token in tokens:
            print(token)
        print('ERRORES\n')
        for error in self.Errores:
            print(error)

    def getErrores (self):
        return self.Errores


