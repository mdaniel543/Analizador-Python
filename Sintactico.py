class Sintactico:
    linea = 0
    columna = 0
    counter = 0
    ErroresR = []
    listaTokensa = []
    ErrorSintactico = False
    BanderaR = False
    ErroresS = []
    Index = 0
    TokenActual = ""
    RrS = []
    cons = ""
    temp = -1
    ciclo = 0
    aux = "Correcto"
    

    signosR = {"Menos": '-', "Mas": '+', "Division": '/', "Multiplicacion": '*', "Parentesis Abre": '(', "Parentesis Cierra": ')'}

    def scannerR(self, text):
        global linea, columna, counter, Errores, bandera, listaTokens
        linea = 1
        columna = 1
        while self.counter < len(text):
            if text[self.counter].isdigit(): #NUMERO
                self.listaTokensa.append(self.StateNumberR(linea, columna, text, text[self.counter]))
            elif text[self.counter].isalpha() or text[self.counter].isdigit(): #IDENTIFICADOR
                self.listaTokensa.append(self.StateIdentifierR(linea, columna, text, text[self.counter]))
            elif text[self.counter] == "\n":#SALTO DE LINEA
                self.listaTokensa.append([linea, columna, 'TerminaLinea', '#'])
                self.counter += 1
                linea += 1
                columna = 1 
                self.ciclo += 1
            elif text[self.counter] == "\t":#ESPACIOS Y TABULACIONES
                self.counter += 1
                columna += 1 
            elif text[self.counter] == " ":#ESPACIOS Y TABULACIONES
                self.counter += 1
                columna += 1 
            else:
                #SIGNOS
                isSign = False
                for clave in self.signosR:
                    valor = self.signosR[clave]
                    if text[self.counter] == valor:
                        self.listaTokensa.append([linea, columna, clave, valor.replace('\\','')])
                        self.counter += 1
                        columna += 1
                        isSign = True
                        break
                if not isSign:
                    self.ErroresR.append([linea, columna, text[self.counter]])
                    columna += 1
                    self.counter += 1
        linea = 0
        columna = 0
        counter = 0    
        return self.listaTokensa

    def StateIdentifierR(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isalpha() or text[self.counter].isdigit():#IDENTIFICADOR
                return self.StateIdentifierR(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'ID', word]
        else:
            return [line, column, 'ID', word]

        
    def StateNumberR(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#ENTERO
                return self.StateNumberR(line, column, text, word + text[self.counter])
            elif text[self.counter] == ".":#DECIMAL
                return self.StateDecimalR(line, column, text, word + text[self.counter])
            elif text[self.counter].isalpha():
                return self.StateIdentifierR(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'DIGITO', word]
                #agregar automata de numero en el arbol, con el valor
        else:
            return [line, column, 'DIGITO', word]

    def StateDecimalR(self, line, column, text, word):
        global counter, columna
        self.counter += 1
        columna += 1
        if self.counter < len(text):
            if text[self.counter].isdigit():#DECIMAL
                return self.StateDecimalR(line, column, text, word + text[self.counter])
            else:
                return [line, column, 'DECIMAL', word]
                #agregar automata de decimal en el arbol, con el valor
        else:
            return [line, column, 'DECIMAL', word]

    def INICIORMT(self, texto):
        print(texto)
        self.ErroresS.clear()
        self.listaTokensa.clear()
        self.RrS.clear()
        tokens = self.scannerR(texto) 
        for token in tokens:
            print(token)
        print('ERRORES\n')
        for error in self.ErroresR:
            print(error)
        self.InicioSintactico()
        for errors in self.ErroresS:
            print(errors)


    def getErroresRMT (self):
        return self.ErroresR

    def verficar(self):
        global Index, TokenActual, ErrorSintactico
        if self.TokenActual == 'TerminaLinea':
            print('Exito')
        elif self.TokenActual == 'Parentesis Cierra': 
            self.Parea('Aceptacion')
            

    def InicioSintactico(self):
        global Index, TokenActual, ErrorSintactico, listaTokensa
        self.Index = 0
        self.TokenActual = self.listaTokensa[self.Index][2]
        self.cons += self.listaTokensa[self.Index][3]
        i = -1
        while i < self.ciclo:
            i += 1
            self.S0()
            self.verficar()
        
        print("Se concluyo analisis sintactico")


    def S0(self):
        global Index, TokenActual, Bandera
        if self.TokenActual == 'ID':
            self.Parea('ID')
            self.S1()
        elif self.TokenActual == 'DIGITO':
            self.Parea('DIGITO')
            self.S1()
        elif self.TokenActual == 'DECIMAL':
            self.Parea('DIGITO')
            self.S1()
        elif self.TokenActual == 'Parentesis Abre':
            self.Parea('Parentesis Abre')
            #self.Bandera = True
            self.S0()
            self.Parea('Parentesis Cierra')
            self.S1()
        else:
            #Epsilon
            pass

    def S1(self):
        global Index, TokenActual
        if self.TokenActual == 'Menos':
            self.Parea('Menos')
            self.S0()
        elif self.TokenActual == 'Mas':
            self.Parea('Mas')
            self.S0()
        elif self.TokenActual == 'Multiplicacion':
            self.Parea('Multiplicacion')
            self.S0()
        elif self.TokenActual == 'Division':
            self.Parea('Division')
            self.S0()
        elif self.TokenActual == 'TerminaLinea':
            self.Parea('TerminaLinea')
        else:
            pass


    def Parea(self, token):
        global Index, TokenActual, ErrorSintactico, ErroresS, listaTokensa, Bandera, cons
        if(self.ErrorSintactico):
            if(self.Index < len(self.listaTokensa)):
                self.Index += 1
                self.TokenActual = self.listaTokensa[self.Index][2]
                self.cons += self.listaTokensa[self.Index][3]
                if self.TokenActual == 'TerminaLinea':
                    self.ErrorSintactico = False
                    self.RrS.append([self.cons, "Incorrecto"])
                    self.cons = ""
                    self.aux = "Correcto"
                    self.temp += 1
                    print("HOLA")
                    self.Parea('TerminaLinea')
        else:
            if (self.Index <= len(self.listaTokensa) -1):
                if self.TokenActual == token:
                    if self.Index == len(self.listaTokensa)-1:
                        self.Index += 1
                    elif self.Index > len(self.listaTokensa)-1:
                        self.Index += 1
                    else:
                        self.Index += 1
                        self.TokenActual = self.listaTokensa[self.Index][2]
                        self.cons += self.listaTokensa[self.Index][3]
                        if self.TokenActual == 'TerminaLinea':
                            self.RrS.append([self.cons, self.aux])
                            self.cons = ""
                            self.aux = "Correcto"
                            self.temp +=1
                else: 
                    self.ErroresS.append(['>> Error sintactico', token, self.listaTokensa[self.Index][2], self.listaTokensa[self.Index][3]])
                    print ('>> Error sintactico se esperaba [' + token + '] en lugar de [' +  self.listaTokensa[self.Index][2] + 
                            '] con valor de \"' + self.listaTokensa[self.Index][3] + '\"' + 'en la linea ' + str(self.listaTokensa[self.Index][0]))
                    self.ErrorSintactico = True
                    self.aux = "Incorrecto"
                    if 'TerminaLinea' == self.listaTokensa[self.Index-1][2]:
                        self.RrS[self.temp-1][1] = self.aux
                        self.ErrorSintactico = False
            else:        
                print ('>> Error sintactico se esperaba [' + token + ']' )
                self.ErroresS.append(['>> Error sintactico', token, "", ""])
                self.ErrorSintactico = True
                self.aux = "Incorrecto"
                self.RrS[self.temp][1] = self.aux
        

    def getErroresS(self):
        return self.ErroresS



                


