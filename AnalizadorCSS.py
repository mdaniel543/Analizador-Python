class AnalizadorCSS:
    unida = ""
    y = ""
    linea = 0
    columna = 0
    counter = 0
    Errores = []
    reservadas = ['color', 'border', 'text-align', 'font-weight','padding-left', 'padding-top', 'line-height', 'margin-top', 'margin-left','display', 'top', 'float', 'min-width'
                    'background-color', 'Opacity', 'font-family', 'font-size', 'padding-right', 'padding', 'width', 'margin-right', 'margin', 'position', 'right', 'clear', 'max-height'
                    'background-image', 'background', 'font-style', 'font', 'padding-bottom', 'display', 'height', 'margin-bottom', 'border-style', 'bottom', 'left', 'max-width', 'min-height']

    signos = {"PUNTOCOMA":';', "LLAVE ABRE":'{', "LLAVE CIERRA":'}', "SELECTOR": '*', "COMA": ',', "DOS PUNTOS": ':' ,"NUMERAL": '#', "PUNTO": '.'}

    med = ['px', 'em', 'vh', 'vw', 'in', 'cm', ' mm', 'pt', 'pc']

    def scanner(self, text):
        global linea, columna, counter, Errores
        linea = 1
        columna = 1
        listaTokens = []

        while self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter] == "-" : #IDENTIFICADOR
                listaTokens.append(self.StateIdentifier(linea, columna, text, text[self.counter]))            
            elif text[self.counter] == '"':
                listaTokens.append(self.Cadena(linea, columna, text, text[self.counter]))
            elif text[self.counter] == "-":
                listaTokens.append(self.StateNumberN(linea, columna, text, text[self.counter]))
            elif text[self.counter].isdigit(): #NUMERO
                listaTokens.append(self.StateNumber(linea, columna, text, text[self.counter]))
            elif text[self.counter] == "/": #COMENTARIO
                listaTokens.append(self.comentario(linea, columna, text, text[self.counter]))
            elif text[self.counter] == '#': #Codigo
                listaTokens.append(self.codigo(linea, columna, text, text[self.counter]))
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

    def StateNumberN(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#ENTERO
                return self.StateNumber(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'GUION', word]
                #agregar automata de numero en el arbol, con el valor
        else:
            return [line, column, 'GUION', word]

    #[linea, columna, tipo, valor]
    def codigo(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit():
                return self.codigo(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'CODIGO DE COLOR', word]
        else:
            return [line, column, 'CODIGO DE COLOR', word]
  
    def comentario(self, line, column, text, word):
        global counter, columna
        self.counter += 1 
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "*": #Comentario Multilinea
                return self.CMlinea(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'Barra', word]
        else:
            return [line, column, 'Barra', word]

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

    def CMlinea(self, line, column, text, word):
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
                    return self.CMlinea(line, column, text, word + text[self.counter-1] + text[self.counter])
            elif text[self.counter] == "\n":
                return self.CMlinea(line, column, text, word + " ")
            elif word == "// PATHW:":
                rr = self.Ruta(line, columna, text, "")
                return [line, column, 'Ruta', rr]
            else:
                return self.CMlinea(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Comentario', word]

    def StateIdentifier(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit() or text[self.counter] == "-":
                return self.StateIdentifier(line, column, text, word + text[self.counter])
            else:
                if word == "url":
                    self.counter -= 1
                    Aux = [line, column, 'URL', self.u(line, column, text, word)]
                    self.counter += 1
                    return Aux
                elif word == "rgba":
                    self.counter -= 1
                    Aux = [line, column, 'RGBA', self.rg(line, column, text, word)]
                    self.counter += 1
                    return Aux
                return [line, column, 'ID', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [line, column, 'ID', word]
    def u(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "(":#IDENTIFICADOR
                self.counter += 1
                columna += 1
                if text[self.counter] == '"':
                    return self.Ca(line, column, text, word + text[self.counter-1]  + text[self.counter])
                else:
                    self.Errores.append([linea, columna, text[self.counter]])
                    columna += 1
                    self.counter += 1
                    return word
            else:
                self.Errores.append([linea, columna, text[self.counter]])
                columna += 1
                self.counter += 1
                return word
        else: 
            return word
    def Ca(self, line, column, text, word):
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
                return  self.Ca(line, column, text, word + text[self.counter])
            else:
                return self.Ca(line, column, text, word + text[self.counter]) 
        else:       
            return word

    def rg(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "(":
                return self.separa(line, column, text, word + text[self.counter])
            else:
                self.Errores.append([linea, columna, text[self.counter]])
                columna += 1
                self.counter += 1
                return word
        else:
            return word
    def separa(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == ')':
                return word + text[self.counter]
            elif text[self.counter] == "\n":
                return word
            elif text[self.counter].isdigit():
                return self.separa(line, column, text, word + text[self.counter])
            elif text[self.counter] == ",":
                return self.separa(line, column, text, word + text[self.counter])
            elif text[self.counter] == " ":
                return self.separa(line, column, text, word + text[self.counter])
            elif text[self.counter] == ".":
                return self.separa(line, column, text, word + text[self.counter])
            else:
                self.Errores.append([linea, columna, text[self.counter]])
                return self.separa(line, column, text, word)
        else:
            return word

    def Cadena(self, line, column, text, word):
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
                return self.Cadena(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Cadena', word]

    
        
    def StateNumber(self, line, column, text, word):
        global counter, columna, unida, y
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#ENTERO
                return self.StateNumber(line, column, text, word + text[self.counter])
            elif text[self.counter] == ".":#DECIMAL
                return self.StateDecimal(line, column, text, word + text[self.counter])
            elif text[self.counter] == "%":#Porcentaje
                Aux = [line, column, 'Porcentaje', word + text[self.counter]]
                self.counter +=1
                return Aux
            elif text[self.counter].isalpha():
                self.counter -= 1 
                x = self.counter
                self.medida(line, column, text, "")
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

    def StateDecimal(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#DECIMAL
                return self.StateDecimal(line, column, text, word + text[self.counter])
            elif text[self.counter] == "%":#Porcentaje
                Aux = [line, column, 'Porcentaje', word + text[self.counter]]
                self.counter +=1
                return Aux
            elif text[self.counter].isalpha():
                self.counter -=1 
                x = self.counter
                self.medida(line, column, text, "")
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
    def medida(self, line, column, text, word):
        global counter, columna, unida, y
        self.counter +=1
        columna +=1 
        if self.counter < len(text):
            if text[self.counter].isalpha():
                self.medida(line, column, text, word + text[self.counter]) 
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