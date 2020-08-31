class AnalizadorHTML:
    linea = 0
    columna = 0
    counter = 0
    Errores = []
    reservadas = []


    signos = {"IGUAL": '=' }

    def scanner(self, text):
        global linea, columna, counter, Errores
        linea = 1
        columna = 1
        listaTokens = []

        while self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit() or text[self.counter] == "_" : #IDENTIFICADOR
                listaTokens.append(self.StateIdentifier(linea, columna, text, text[self.counter]))
            elif text[self.counter] == '\'':
                listaTokens.append(self.Caracter(linea, columna, text, text[self.counter]))
            elif text[self.counter] == '"':
                listaTokens.append(self.Cadena(linea, columna, text, text[self.counter]))
            elif text[self.counter].isdigit(): #NUMERO
                listaTokens.append(self.StateNumber(linea, columna, text, text[self.counter]))
            elif text[self.counter] == "/": #COMENTARIO
                listaTokens.append(self.comentario(linea, columna, text, text[self.counter]))
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

    #[linea, columna, tipo, valor]
    def comentario(self, line, column, text, word):
        global counter, columna
        self.counter += 1 
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "/":#Comentario Unilinea
                return self.Clinea(line, column, text, word + text[self.counter])
            elif text[self.counter] == "*": #Comentario Multilinea
                return self.CMlinea(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'Barra', word]
        else:
            return [line, column, 'Barra', word]

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

    def CMlinea(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == "*":
                self.counter += 1
                if text[self.counter] == "/":
                    Aux = [line, column, 'Comentario Multilinea', word + text[self.counter-1] + text[self.counter]]
                    self.counter += 1
                    return Aux
                else:
                    return self.CMlinea(line, column, text, word + text[self.counter-1] + text[self.counter])
            elif text[self.counter] == "\n":
                return self.CMlinea(line, column, text, word + " ")
            else:
                return self.CMlinea(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Comentario Multilinea', word]

    def StateIdentifier(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit() or text[self.counter] == "_":#IDENTIFICADOR
                return self.StateIdentifier(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'ID', word]
                #agregar automata de identificador en el arbol, con el valor
        else:
            return [line, column, 'ID', word]

    def Cadena(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == '"':
                Aux = [line, column, 'String', word + text[self.counter]]
                self.counter += 1
                return Aux
            elif text[self.counter] == "\n":
                return [line, column, 'Cadena', word]
            else:
                return self.Cadena(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'String', word]

    def Caracter(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter] == '\'':
                Aux = [line, column, 'Char', word + text[self.counter]]
                self.counter += 1
                return Aux
            elif text[self.counter] == "\n":
                return [line, column, 'Char', word]
            else:
                return self.Caracter(line, column, text, word + text[self.counter])
        else:
            return [line, column, 'Char', word]
        
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