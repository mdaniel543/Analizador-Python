import os

class ReporteErrores:
    HTML = ""
    FilaTabla = ""
    def realizarHTML(self, errores, nombre, ruta): 
        self.HTML = "<!DOCTYPE html>\n" 
        self.HTML += "<html lang=\"en\">\n" 
        self.HTML += "    <head>\n"
        self.HTML += "        <title>Tokens</title>\n"
        self.HTML += "        <style>\n"
        self.HTML += "            table.blueTable {\n"
        self.HTML += "                border: 1px solid #1C6EA4;\n"
        self.HTML += "                background-color: #EEEEEE;\n"
        self.HTML += "                width: 100%;\n"
        self.HTML += "                text-align: left;\n"
        self.HTML += "                border-collapse: collapse;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable td, table.blueTable th {\n"
        self.HTML += "                border: 1px solid #AAAAAA;\n"
        self.HTML += "                padding: 3px 2px;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable tbody td {\n"
        self.HTML += "                font-size: 13px;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable tr:nth-child(even) {\n"
        self.HTML += "                background: #D0E4F5;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable thead {\n"
        self.HTML += "                background: #1C6EA4;\n"
        self.HTML += "                background: -moz-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);\n"
        self.HTML += "                background: -webkit-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);\n"
        self.HTML += "                background: linear-gradient(to bottom, #5592bb 0%, #327cad 66%, #1C6EA4 100%);\n"
        self.HTML += "                border-bottom: 2px solid #444444;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable thead th {\n"
        self.HTML += "                font-size: 15px;\n"
        self.HTML += "                font-weight: bold;\n"
        self.HTML += "                color: #FFFFFF;\n"
        self.HTML += "                border-left: 2px solid #D0E4F5;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable thead th:first-child {\n"
        self.HTML += "                border-left: none;\n"
        self.HTML += "            }\n"
        self.HTML += "\n"
        self.HTML += "            table.blueTable tfoot {\n"
        self.HTML += "                font-size: 14px;\n"
        self.HTML += "                font-weight: bold;\n"
        self.HTML += "                color: #FFFFFF;\n"
        self.HTML += "                background: #D0E4F5;\n"
        self.HTML += "                background: -moz-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);\n"
        self.HTML += "                background: -webkit-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);\n"
        self.HTML += "                background: linear-gradient(to bottom, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);\n"
        self.HTML += "                border-top: 2px solid #444444;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable tfoot td {\n"
        self.HTML += "                font-size: 14px;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable tfoot .links {\n"
        self.HTML += "                text-align: right;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable tfoot .links a{\n"
        self.HTML += "                display: inline-block;\n"
        self.HTML += "                background: #1C6EA4;\n"
        self.HTML += "                color: #FFFFFF;\n"
        self.HTML += "                padding: 2px 8px;\n"
        self.HTML += "                border-radius: 5px;\n"
        self.HTML += "            }\n"
        self.HTML += "            body{\n"
        self.HTML += "                background: #FE9A2E;\n"
        self.HTML += "            }\n"
        self.HTML += "        </style>    \n"
        self.HTML += "    </head>\n"
        self.HTML += "    <body>\n"
        self.HTML += "    <center>\n"
        self.HTML += "        <h1> Lista de Tokens</h1>\n"
        self.HTML += "        <table class=\"blueTable\" style=\"width: 80%\" border=\"\">\n"
        self.HTML += "            <thead>\n"
        self.HTML += "                <tr>\n"
        self.HTML += "                    <td>No.</td>\n"
        self.HTML += "                    <td>Linea</td>\n"
        self.HTML += "                    <td>Columna</td>\n"
        self.HTML += "                    <td>Descripcion</td>\n"        
        self.HTML += "                </tr> \n"
        self.HTML += "            </thead>\n"
        self.HTML += "ContenidoTabla\n"
        self.HTML += "        </table>   \n"
        self.HTML += "    </center>\n"
        self.HTML += "</body>\n"
        self.HTML += "</html>"
        cont = 0
        for T in errores:
            cont += 1
            self.FilaTabla += " <tr>\n"
            self.FilaTabla += "    <td>" + str(cont) + "</td>\n"
            self.FilaTabla += "    <td>" + str(T[0]) + "</td>\n"
            self.FilaTabla += "    <td>" + str(T[1]) + "</td>\n"
            self.FilaTabla += "    <td> El caracter '" + T[2] + "' no pertenece al lenguaje </td>\n"     
            self.FilaTabla += "  </tr>\n"
        Reporte = self.HTML.replace("ContenidoTabla", self.FilaTabla)
        #print(Reporte)
        self.HTML = ""
        self.FilaTabla = ""
        self.Guardar(nombre, ruta, Reporte)

    def SintacticoHTML(self, errores, nombre, ruta): 
        self.HTML = "<!DOCTYPE html>\n" 
        self.HTML += "<html lang=\"en\">\n" 
        self.HTML += "    <head>\n"
        self.HTML += "        <title>Tokens</title>\n"
        self.HTML += "        <style>\n"
        self.HTML += "            table.blueTable {\n"
        self.HTML += "                border: 1px solid #1C6EA4;\n"
        self.HTML += "                background-color: #EEEEEE;\n"
        self.HTML += "                width: 100%;\n"
        self.HTML += "                text-align: left;\n"
        self.HTML += "                border-collapse: collapse;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable td, table.blueTable th {\n"
        self.HTML += "                border: 1px solid #AAAAAA;\n"
        self.HTML += "                padding: 3px 2px;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable tbody td {\n"
        self.HTML += "                font-size: 13px;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable tr:nth-child(even) {\n"
        self.HTML += "                background: #D0E4F5;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable thead {\n"
        self.HTML += "                background: #1C6EA4;\n"
        self.HTML += "                background: -moz-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);\n"
        self.HTML += "                background: -webkit-linear-gradient(top, #5592bb 0%, #327cad 66%, #1C6EA4 100%);\n"
        self.HTML += "                background: linear-gradient(to bottom, #5592bb 0%, #327cad 66%, #1C6EA4 100%);\n"
        self.HTML += "                border-bottom: 2px solid #444444;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable thead th {\n"
        self.HTML += "                font-size: 15px;\n"
        self.HTML += "                font-weight: bold;\n"
        self.HTML += "                color: #FFFFFF;\n"
        self.HTML += "                border-left: 2px solid #D0E4F5;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable thead th:first-child {\n"
        self.HTML += "                border-left: none;\n"
        self.HTML += "            }\n"
        self.HTML += "\n"
        self.HTML += "            table.blueTable tfoot {\n"
        self.HTML += "                font-size: 14px;\n"
        self.HTML += "                font-weight: bold;\n"
        self.HTML += "                color: #FFFFFF;\n"
        self.HTML += "                background: #D0E4F5;\n"
        self.HTML += "                background: -moz-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);\n"
        self.HTML += "                background: -webkit-linear-gradient(top, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);\n"
        self.HTML += "                background: linear-gradient(to bottom, #dcebf7 0%, #d4e6f6 66%, #D0E4F5 100%);\n"
        self.HTML += "                border-top: 2px solid #444444;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable tfoot td {\n"
        self.HTML += "                font-size: 14px;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable tfoot .links {\n"
        self.HTML += "                text-align: right;\n"
        self.HTML += "            }\n"
        self.HTML += "            table.blueTable tfoot .links a{\n"
        self.HTML += "                display: inline-block;\n"
        self.HTML += "                background: #1C6EA4;\n"
        self.HTML += "                color: #FFFFFF;\n"
        self.HTML += "                padding: 2px 8px;\n"
        self.HTML += "                border-radius: 5px;\n"
        self.HTML += "            }\n"
        self.HTML += "            body{\n"
        self.HTML += "                background: #FE9A2E;\n"
        self.HTML += "            }\n"
        self.HTML += "        </style>    \n"
        self.HTML += "    </head>\n"
        self.HTML += "    <body>\n"
        self.HTML += "    <center>\n"
        self.HTML += "        <h1> Lista de Tokens</h1>\n"
        self.HTML += "        <table class=\"blueTable\" style=\"width: 80%\" border=\"\">\n"
        self.HTML += "            <thead>\n"
        self.HTML += "                <tr>\n"
        self.HTML += "                    <td>Linea</td>\n"
        self.HTML += "                    <td>Operacion </td>\n"
        self.HTML += "                    <td>Analisis</td>\n"        
        self.HTML += "                </tr> \n"
        self.HTML += "            </thead>\n"
        self.HTML += "ContenidoTabla\n"
        self.HTML += "        </table>   \n"
        self.HTML += "    </center>\n"
        self.HTML += "</body>\n"
        self.HTML += "</html>"
        print("H")
        cont = 0
        for T in errores:
            cont += 1
            self.FilaTabla += " <tr>\n"
            self.FilaTabla += "    <td>" + str(cont) + "</td>\n"
            self.FilaTabla += "    <td>" + str(T[0]) + "</td>\n"
            self.FilaTabla += "    <td>" + str(T[1]) + "</td>\n"
            self.FilaTabla += "  </tr>\n"
        Reporte = self.HTML.replace("ContenidoTabla", self.FilaTabla)
        #print(Reporte)
        self.HTML = ""
        self.FilaTabla = ""
        self.Guardar(nombre, ruta, Reporte)
    

    def Guardar(self, nombre, ruta, contenido):
        if not os.path.exists(ruta):
            os.system("mkdir " + ruta)
        Rguardar = open(ruta + "\\" + "Errores_de_" + nombre + ".html", "w+")
        Rguardar.write(contenido)
        Rguardar.close()
        os.startfile(ruta + "\\" + "Errores_de_" + nombre + ".html")
        
    