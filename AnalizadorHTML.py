class AnalizadorHTML:
    linea = 0
    columna = 0
    counter = 0
    prvs = ""
    bandera = False
    ErroresH = []
    rrv = ""
    reservadasH = ['src', 'href', 'style']

    Definiciones = ['<title>', '<body>', '<br>','<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<p>', 
                    '<li>', '<caption>', '<th>', '<td>', '<thead>', '<tbody>', '<tfoot>']


    signosH = {"IGUAL": '=' , "Cierra": '>'}

    def scannerH(self, text):
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
                    self.SupuestoH(linea, columna, text, text[self.counter])
                else:
                    listaTokens.append(self.ContenidoH(linea, columna, text, text[self.counter]))
            elif text[self.counter].isalpha(): #IDENTIFICADOR
                listaTokens.append(self.StateIdentifierH(linea, columna, text, text[self.counter]))
            elif text[self.counter] == '<':
                listaTokens.append(self.EtiquetaH(linea, columna, text, text[self.counter]))
            elif text[self.counter] == '"':
                listaTokens.append(self.CadenaH(linea, columna, text, text[self.counter]))
            elif text[self.counter].isdigit(): #NUMERO
                listaTokens.append(self.StateNumberH(linea, columna, text, text[self.counter]))
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
                for clave in self.signosH:
                    valor = self.signosH[clave]
                    if text[self.counter] == valor:
                        listaTokens.append([linea, columna, clave, valor.replace('\\','')])
                        self.counter += 1
                        columna += 1
                        isSign = True
                        break
                if not isSign:
                    self.ErroresH.append([linea, columna, text[self.counter]])
                    columna += 1
                    self.counter += 1
        linea = 0
        columna = 0
        counter = 0    
        return listaTokens

    def EtiquetaH(self, line, column, text, word):
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
            elif text[self.counter] == "!":
                return self.CMlineaH(line, column, text, word + text[self.counter])
            elif text[self.counter] == "/":
                return self.Etiqueta2H(line, column, text, word + text[self.counter])
            else:
                return self.EtiquetaH(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Etiqueta', word]
    
    def Etiqueta2H(self, line, column, text, word):
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
                return self.Etiqueta2H(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Etiqueta', word]
    
    def SupuestoH(self, line, column, text, word):
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
                self.SupuestoH(line, column, text, word + text[self.counter])
                return
        else:
            return

    def ContenidoH(self, line, column, text, word):
        global counter, columna, bandera
        self.counter += 1 
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "<":
                self.bandera = False
                return [line, column, 'Contenido Visible', word]
            elif text[self.counter] == "\n":
                self.bandera = False
                return self.ContenidoH(line, column, text, " ")
            else:
                return self.ContenidoH(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Contenido Visible', word]


    def CMlineaH(self, line, column, text, word):
        global counter, columna, pr, rr
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == ">":
                return [line, column, 'Comentario', word]
            elif text[self.counter].isalpha():
                self.prvs += text[self.counter]
                if self.prvs == 'PATHW':
                    self.rrv = self.RutaH(line, columna, text, "")
                    self.counter += 1
                    return [line, column, 'Ruta', self.rrv]
                return self.CMlineaH(line, column, text, word + text[self.counter])            
            else:
                return self.CMlineaH(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Comentario', word]

    def RutaH(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isalpha():
                return self.GuardarRH(line, column, text, text[self.counter])
            else:
                return self.RutaH(line, column, text, word + text[self.counter])
        else:
            return word

    def GuardarRH(self, line, column, text, word):
        global counter, columna, RUTA, prt
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == ">":
                return word
            elif text[self.counter] == '-':
                return self.GuardarRH(line, column, text, word)
            else:
                return self.GuardarRH(line, column, text, word + text[self.counter])
        else:
            return word

    def StateIdentifierH(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit() or text[self.counter] == " ":#IDENTIFICADOR
                return self.StateIdentifierH(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'ID', word]
        else:
            return [line, column, 'ID', word]

    def CadenaH(self, line, column, text, word):
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
                return self.CadenaH(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Cadena', word]

    
        
    def StateNumberH(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#ENTERO
                return self.StateNumberH(line, column, text, word + text[self.counter])
            elif text[self.counter] == ".":#DECIMAL
                return self.StateDecimalH(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'Int', word]
                #agregar automata de numero en el arbol, con el valor
        else:
            return [line, column, 'Int', word]

    def StateDecimalH(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#DECIMAL
                return self.StateDecimalH(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'Decimal', word]
                #agregar automata de decimal en el arbol, con el valor
        else:
            return [line, column, 'Decimal', word]

    def ReservedH(self, TokenList):
        for token in TokenList:
            if token[2] == 'ID':
                for reservada in self.reservadasH:
                    if token[3] == reservada:
                        token[2] = 'RESERVADA: ' + '<' + token[3] +'>'
                        break

    def INICIOHTML(self, texto):
        print(texto)
        tokens = self.scannerH(texto)
        self.ReservedH(tokens)
        for token in tokens:
            print(token)
        print('ERRORES\n')
        for error in self.ErroresH:
            print(error)
        return tokens

    def getErroresHTML (self):
        return self.ErroresH