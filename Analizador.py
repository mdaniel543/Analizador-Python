import re

class Analizador:

    def inicio(self, texto):
        print(texto)
        tokens = inic(texto)
        Reserved(tokens)
        for token in tokens:
            print(token)
        print('ERRORES')
        for error in Errores:
            print(error)