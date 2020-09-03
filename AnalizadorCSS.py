class AnalizadorCSS:
    unida = ""
    y = ""
    prs = ""
    linea = 0
    columna = 0
    rrs = ""
    counter = 0
    ErroresC = []
    reservadasC = ['color', 'border', 'text-align', 'font-weight','padding-left', 'padding-top', 'line-height', 'margin-top', 'margin-left','display', 'top', 'float', 'min-width',
                    'background-color', 'Opacity', 'font-family', 'font-size', 'padding-right', 'padding', 'width', 'margin-right', 'margin', 'position', 'right', 'clear', 'max-height',
                    'background-image', 'background', 'font-style', 'font', 'padding-bottom', 'display', 'height', 'margin-bottom', 'border-style', 'bottom', 'left', 'max-width', 'min-height']

    signosC = {"PUNTOCOMA":';', "LLAVE ABRE":'{', "LLAVE CIERRA":'}', "SELECTOR": '*', "COMA": ',', "DOS PUNTOS": ':' ,"NUMERAL": '#', "PUNTO": '.', "Menos": '-', "Mas": '+', "Parentesis Abre": '(', "Parentesis Cierra": ')'}

    med = ['px', 'em', 'vh', 'vw', 'in', 'cm', ' mm', 'pt', 'pc']

    def scannerC(self, text):
        global linea, columna, counter, ErroresC
        linea = 1
        columna = 1
        listaTokens = []

        while self.counter < len(text):
            if text[self.counter].isalpha(): #IDENTIFICADOR
                listaTokens.append(self.StateIdentifierC(linea, columna, text, text[self.counter]))            
            elif text[self.counter] == '"':
                listaTokens.append(self.CadenaC(linea, columna, text, text[self.counter]))
            elif text[self.counter] == "-":
                listaTokens.append(self.StateNumberNC(linea, columna, text, text[self.counter]))
            elif text[self.counter].isdigit(): #NUMERO
                listaTokens.append(self.StateNumberC(linea, columna, text, text[self.counter]))
            elif text[self.counter] == "/": #COMENTARIO
                listaTokens.append(self.comentarioC(linea, columna, text, text[self.counter]))
            elif text[self.counter] == '#': #Codigo
                listaTokens.append(self.codigoC(linea, columna, text, text[self.counter]))
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
                for clave in self.signosC:
                    valor = self.signosC[clave]
                    if text[self.counter] == valor:
                        listaTokens.append([linea, columna, clave, valor.replace('\\','')])
                        self.counter += 1
                        columna += 1
                        isSign = True
                        break
                if not isSign:
                    self.ErroresC.append([linea, columna, text[self.counter]])
                    columna += 1
                    self.counter += 1
        linea = 0
        columna = 0
        counter = 0    
        return listaTokens

    def StateNumberNC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#ENTERO
                return self.StateNumberC(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'GUION', word]
                #agregar automata de numero en el arbol, con el valor
        else:
            return [line, column, 'GUION', word]

    #[linea, columna, tipo, valor]
    def codigoC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit():
                return self.codigoC(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'CODIGO', word]

        else:
            return [line, column, 'CODIGO', word]
  
    def comentarioC(self, line, column, text, word):
        global counter, columna
        self.counter += 1 
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "*": #Comentario Multilinea
                return self.CMlineaC(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'Barra', word]
        else:
            return [line, column, 'Barra', word]

    def RutaC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == 'c':
                return self.GuardarRC(line, column, text, text[self.counter])
            else:
                return self.RutaC(line, column, text, word + text[self.counter])
        else:
            return word

    def GuardarRC(self, line, column, text, word):
        global counter, columna, RUTA, prt
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == '\n':
                return word
            else:
                return self.GuardarRC(line, column, text, word + text[self.counter])
        else:
            return word

    def CMlineaC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "*":
                self.counter += 1
                if text[self.counter] == "/":
                    Aux = [line, column, 'Comentario', word + text[self.counter-1] + text[self.counter]]
                    self.counter += 1
                    return Aux
                else:
                    return self.CMlineaC(line, column, text, word + text[self.counter-1] + text[self.counter])
            elif text[self.counter] == "\n":
                return self.CMlineaC(line, column, text, word + " ")
            elif text[self.counter].isalpha():
                self.prs += text[self.counter]
                if self.prs == 'PATHW':
                    self.rrs = self.RutaC(line, columna, text, "")
                    return [line, column, 'Ruta', self.rrs]
                return self.CMlineaC(line, column, text, word + text[self.counter])
            else:
                self.prs = ""
                return self.CMlineaC(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Comentario', word]

    def StateIdentifierC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit() or text[self.counter] == "-":
                return self.StateIdentifierC(line, column, text, word + text[self.counter])
            else:
                if word == "url":
                    self.counter -= 1
                    Aux = [line, column, 'URL', self.uC(line, column, text, word)]
                    self.counter += 1
                    return Aux
                elif word == "rgba":
                    self.counter -= 1
                    Aux = [line, column, 'RGBA', self.rgC(line, column, text, word)]
                    self.counter += 1
                    return Aux
                return [line, column, 'ID', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [line, column, 'ID', word]
    def uC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "(":#IDENTIFICADOR
                self.counter += 1
                columna += 1
                if text[self.counter] == '"':
                    return self.CaC(line, column, text, word + text[self.counter-1]  + text[self.counter])
                else:
                    self.ErroresC.append([linea, columna, text[self.counter]])
                    columna += 1
                    self.counter += 1
                    return word
            else:
                self.ErroresC.append([linea, columna, text[self.counter]])
                columna += 1
                self.counter += 1
                return word
        else: 
            return word
    def CaC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == '"':
                self.counter += 1
                if text[self.counter] == ")":
                    return word + text [self.counter - 1] + text[self.counter]
            elif text[self.counter] == "\n":
                return  word
            elif text[self.counter] == " ":
                return  self.CaC(line, column, text, word + text[self.counter])
            else:
                return self.CaC(line, column, text, word + text[self.counter]) 
        else:       
            return word

    def rgC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "(":
                return self.separaC(line, column, text, word + text[self.counter])
            else:
                self.ErroresC.append([linea, columna, text[self.counter]])
                columna += 1
                self.counter += 1
                return word
        else:
            return word
    def separaC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == ')':
                return word + text[self.counter]
            elif text[self.counter] == "\n":
                return word
            elif text[self.counter].isdigit():
                return self.separaC(line, column, text, word + text[self.counter])
            elif text[self.counter] == ",":
                return self.separaC(line, column, text, word + text[self.counter])
            elif text[self.counter] == " ":
                return self.separaC(line, column, text, word + text[self.counter])
            elif text[self.counter] == ".":
                return self.separaC(line, column, text, word + text[self.counter])
            else:
                self.Errores.append([linea, columna, text[self.counter]])
                return self.separaC(line, column, text, word)
        else:
            return word

    def CadenaC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == '"':
                Aux = [line, column, 'Cadena', word + text[self.counter]]
                self.counter += 1
                return Aux
            elif text[self.counter] == "\n":
                return [line, column, 'Cadena', word]
            else:
                return self.CadenaC(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Cadena', word]

    
        
    def StateNumberC(self, line, column, text, word):
        global counter, columna, unida, y
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#ENTERO
                return self.StateNumberC(line, column, text, word + text[self.counter])
            elif text[self.counter] == ".":#DECIMAL
                return self.StateDecimalC(line, column, text, word + text[self.counter])
            elif text[self.counter] == "%":#Porcentaje
                Aux = [line, column, 'Porcentaje', word + text[self.counter]]
                self.counter +=1
                return Aux
            elif text[self.counter].isalpha():
                self.counter -= 1 
                x = self.counter
                self.medidaC(line, column, text, "")
                if y == "p":
                    return [line, column, 'UNIDAD DE MEDIDA', word + unida]
                else:
                    self.counter = x + 1 
                    return [line, column, 'NUMERO', word]
            else:
                return [line, column, 'NUMERO', word]
                #agregar automata de numero en el arbol, con el valor
        else:
            return [line, column, 'NUMERO', word]

    def StateDecimalC(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#DECIMAL
                return self.StateDecimalC(line, column, text, word + text[self.counter])
            elif text[self.counter] == "%":#Porcentaje
                Aux = [line, column, 'Porcentaje', word + text[self.counter]]
                self.counter +=1
                return Aux
            elif text[self.counter].isalpha():
                self.counter -=1 
                x = self.counter
                self.medidaC(line, column, text, "")
                if y == "p":
                    return [line, column, 'UNIDAD DE MEDIDA', word + unida]
                else:
                    self.counter = x + 1 
                    return [line, column, 'NUMERO', word]
            else:
                return [line, column, 'Decimal', word]
                #agregar automata de decimal en el arbol, con el valor
        else:
            return [line, column, 'Decimal', word]
    def medidaC(self, line, column, text, word):
        global counter, columna, unida, y
        self.counter +=1
        columna +=1 
        if self.counter < len(text):
            if text[self.counter].isalpha():
                self.medidaC(line, column, text, word + text[self.counter]) 
            else:
                for unidad in self.med:
                    if unidad == word:
                        unida = word
                        y = "p"
                        return 
                y = "x"
                return
        else:
            y = "x"
            return

    def ReservedC(self, TokenList):
        for token in TokenList:
            if token[2] == 'ID':
                for reservadaC in self.reservadasC:
                    if token[3] == reservadaC:
                        token[2] = 'RESERVADA: ' + '<' + token[3] +'>'
                        break

    def INICIOCSS(self, texto):
        print("HOLA")
        print(texto)
        tokens = self.scannerC(texto)
        self.ReservedC(tokens)
        for token in tokens:
            print(token)
        print('ERRORES\n')
        for error in self.ErroresC:
            print(error)

    def getErroresCSS(self):
        return self.ErroresC