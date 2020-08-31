class AnalizadorHTML:
    linea = 0
    columna = 0
    counter = 0
    bandera = False
    Errores = []
    reservadas = ['src', 'href', 'style']

    Definiciones = ['<title>', '<body>', '<br>','<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<p>', 
                    '<li>', '<caption>', '<th>', '<td>', '<thead>', '<tbody>', '<tfoot>']


    signos = {"IGUAL": '=' , "Cierra": '>'}

    def scanner(self, text):
        global linea, columna, counter, Errores, bandera
        linea = 1
        columna = 1
        listaTokens = []

        while self.counter < len(text):
            if self.bandera:
                if text[self.counter] == "\n":
                    self.counter += 1
                    linea += 1
                    columna = 1
                    self.Supuesto(linea, columna, text, text[self.counter])
                else:
                    listaTokens.append(self.Contenido(linea, columna, text, text[self.counter]))
            elif text[self.counter].isalpha(): #IDENTIFICADOR
                listaTokens.append(self.StateIdentifier(linea, columna, text, text[self.counter]))
            elif text[self.counter] == '<':
                listaTokens.append(self.Etiqueta(linea, columna, text, text[self.counter]))
            elif text[self.counter] == '"':
                listaTokens.append(self.Cadena(linea, columna, text, text[self.counter]))
            elif text[self.counter].isdigit(): #NUMERO
                listaTokens.append(self.StateNumber(linea, columna, text, text[self.counter]))
            elif text[self.counter] == "\n":#SALTO DE LINEA
                self.counter += 1
                linea += 1
                columna = 1 
            elif text[self.counter] == "\t":#ESPACIOS Y TABULACIONES
                self.counter += 1
                columna += 1 
            elif text[self.counter] == " ":#ESPACIOS Y TABULACIONES
                self.counter += 1
                columna += 1 
            else:

                #SIGNOS
                isSign = False
                for clave in self.signos:
                    valor = self.signos[clave]
                    if text[self.counter] == valor:
                        listaTokens.append([linea, columna, clave, valor.replace('\\','')])
                        self.counter += 1
                        columna += 1
                        isSign = True
                        break
                if not isSign:
                    self.Errores.append([linea, columna, text[self.counter]])
                    columna += 1
                    self.counter += 1
        linea = 0
        columna = 0
        counter = 0    
        return listaTokens

    def Etiqueta(self, line, column, text, word):
        global counter, columna, bandera
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == '>':
                Aux = [line, column, 'Etiqueta Abre', word + text[self.counter]]
                for con in self.Definiciones:
                    if con == word + text[self.counter]:
                        self.bandera = True
                        break
                self.counter += 1
                return Aux
            elif text[self.counter] == " ":
                return [line, column, 'Etiqueta Abre', word]
            elif text[self.counter] == "/":
                return self.Etiqueta2(line, column, text, word + text[self.counter])
            else:
                return self.Etiqueta(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Etiqueta', word]
    
    def Etiqueta2(self, line, column, text, word):
        global counter, columna, bandera
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == '>':
                Aux = [line, column, 'Etiqueta Cierra', word + text[self.counter]]
                self.counter += 1
                self.bandera = False
                return Aux
            elif text[self.counter] == " ":
                return [line, column, 'Etiqueta Cierra', word]    
            else:
                return self.Etiqueta2(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Etiqueta', word]
    
    def Supuesto(self, line, column, text, word):
        global counter, columna, bandera
        self.counter += 1 
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "<":
                self.bandera = False
                return
            elif text[self.counter].isalpha() or text[self.counter].isdigit():
                self.bandera = True
                return 
            else:
                self.Supuesto(line, column, text, word + text[self.counter])
                return
        else:
            return

    def Contenido(self, line, column, text, word):
        global counter, columna, bandera
        self.counter += 1 
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "<":
                self.bandera = False
                return [line, column, 'Contenido Visible', word]
            elif text[self.counter] == "\n":
                self.bandera = False
                return self.Contenido(line, column, text, " ")
            else:
                return self.Contenido(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Contenido Visible', word]

    def Clinea(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "\n":
                return [line, column, 'Comentario Unilinea', word]
            elif word == "// PATHW:":
                rr = self.Ruta(line, columna, text, "")
                return [line, column, 'Ruta', rr]
            else:
                return self.Clinea(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Comentario Unilinea', word]

    def Ruta(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "\n":
                return word
            else:
                return self.Ruta(line, column, text, word + text[self.counter])
        else:
            return word


    def StateIdentifier(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit() or text[self.counter] == " ":#IDENTIFICADOR
                return self.StateIdentifier(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'ID', word]
        else:
            return [line, column, 'ID', word]

    def Cadena(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == '"':
                Aux = [line, column, 'Cadena', word + text[self.counter]]
                self.counter += 1
                return Aux
            if text[self.counter] == '\'':
                Aux = [line, column, 'Cadena', word + text[self.counter]]
                self.counter += 1
                return Aux
            elif text[self.counter] == "\n":
                return [line, column, 'Cadena', word]
            else:
                return self.Cadena(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Cadena', word]

    
        
    def StateNumber(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#ENTERO
                return self.StateNumber(line, column, text, word + text[self.counter])
            elif text[self.counter] == ".":#DECIMAL
                return self.StateDecimal(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'Int', word]
                #agregar automata de numero en el arbol, con el valor
        else:
            return [line, column, 'Int', word]

    def StateDecimal(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#DECIMAL
                return self.StateDecimal(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'Decimal', word]
                #agregar automata de decimal en el arbol, con el valor
        else:
            return [line, column, 'Decimal', word]

    def Reserved(self, TokenList):
        for token in TokenList:
            if token[2] == 'ID':
                for reservada in self.reservadas:
                    if token[3] == reservada:
                        token[2] = 'RESERVADA: ' + '<' + token[3] +'>'
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