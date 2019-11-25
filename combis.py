#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
  
import sqlite3
from fpdf import FPDF


conn = sqlite3.connect('combis.db')

# si no existe la tabla reservas la crea
conn.execute('''CREATE TABLE if not exists RESERVAS
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             nombre TEXT NOT NULL,      
             telefono TEXT NOT NULL,
             subeEn TEXT,
             bajaEn TEXT,
             nroAsiento  INT, 
             pago INT             
            );''')
    
# si no existe la tabla lugares la crea
conn.execute('''CREATE TABLE if not exists LUGARES
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             nombre   TEXT  NOT NULL,
             codpost  TEXT             
            );''')


""" 
qry = f'''INSERT INTO reservas (nombre, 
                                telefono, 
                                subeEn, 
                                bajaEn, 
                                nroAsiento, 
                                pago) 
                 VALUES
                                ('Francisco', 
                                 '427325', 
                                 '9 de julio 222', 
                                 'Abasto', 
                                 8, 
                                 600)'''
conn.execute(qry)

qry = f'''INSERT INTO LUGARES( nombre) VALUES ('CABA')'''
conn.execute(qry)

qry = f'''INSERT INTO LUGARES( nombre) VALUES ('Lujan')'''        
conn.execute(qry)

conn.commit()    
"""


def dar_lugares():
    """ devuelve una lista de filas de la tabla 
        lugares: (id, nombre, codpost)
    """
    cc = conn.execute("SELECT * FROM lugares")
    
    return list(cc)    


def agregar(valores):
    """ agrega una fila a la tabla reservas
        recibe un diccionario con los valores a insertar
    """   
    qry = '''INSERT INTO reservas
                (nombre, telefono, subeEn, 
                bajaEn, nroAsiento, pago) 
             VALUES
                ('{}', '{}', '{}', '{}', {}, {})                
          '''.format(valores['nombre'],   
                   valores['tele'],
                   valores['sube'],
                   valores['baja'],
                   valores['asiento'],
                   int(valores['pagado']))
                        
    # print(qry)
                        
    conn.execute(qry)
    conn.commit()    


def modificar(valores):
    """ modifica una fila de reservas
        recibe los datos en un diccionario
    """
    qry = '''UPDATE reservas SET
                nombre = '{}', 
                telefono = '{}', 
                subeEn = '{}', 
                bajaEn = '{}', 
                nroAsiento = {},
                pago = {} 
            where id = {}
            '''.format(valores['nombre'],
                       valores['tele'],
                       valores['sube'],
                       valores['baja'],
                       valores['asiento'],
                       int(valores['pagado']
            ), int(valores["id"]))
                        
    # print(qry)                      
                        
    conn.execute(qry)
    conn.commit()    
    
      
def borrar(rid):
    """ borra la reserva con el id indicado 
    """    
    qry = '''DELETE FROM reservas WHERE id = {}'''.format(rid)
                            
    # print(qry)
                            
    conn.execute(qry)
    conn.commit()            

      
def listar(condi = ""):
    """ devuelve la lista de filas que cumplen con el criterio indicado
        en condi. 
        si no se especifica condi devuelve todas las filas
    """
    qry = "SELECT * FROM reservas"
    
    if condi != "":
        qry += " where " + condi
        
    # print(qry)
        
    cc = conn.execute(qry)
    
    return list(cc)

    cc.close()        

 
class PDF(FPDF): 
    """ extiende clase FPDF para definir encabezado y pie de página
        define página A4, medidas en mm y orientación vertical
        agrega atributos para alto y ancho máximos 
        y para tamaño de márgen superior e inferior
    """        
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.max_x = 210
        self.max_y = 297
        self.m_inf = 15
        self.m_sup = 10
        
    def header(self):
        """ encanezado de página para listado"""
        # letra para el título
        self.set_font('Arial', 'B', 16)
        
        # título (ancho máximo, alto automático, sin borde, 
        # deja x,y abajo a la izquierda,  centrado)
        self.cell(0, 0, 'Lista de pasajeros', 0, 1, 'C')
        
        # linea = 0
        # letra para el contenido de la lista
        self.set_font('Arial', '', 10)
        
        self.cell(0, 20, "", 0, 1, 'L')

        # alto del renglón
        alto = 10

        # encabezado de la lista
        self.cell(40, alto, "nombre", 0, 0, 'L')
        self.cell(30, alto, "teléfono", 0, 0, 'L')
        self.cell(30, alto, "origen", 0, 0, 'L')
        self.cell(30, alto, "destino", 0, 0, 'L')
        self.cell(20, alto, "asiento", 0, 0, 'C')
        self.cell(20, alto, "pagó", 0, 1, 'C')
        
        # línea horizontal 
        self.line(self.get_x(), self.get_y(), self.max_x, self.get_y())


    def footer(self):
        # 15 mm desde abajo
        self.set_y(-15)
        
        # línea horizontal 
        self.line(self.get_x(), self.get_y(), self.max_x, self.get_y())
        
        # Select Arial italic 8
        self.set_font('Arial', '', 8)
        
        # Print centered page number
        self.cell(0, 10, '%s' % self.page_no(), 0, 0, 'C')        
              
              
def lista_a_pdf():
    """ genera un archivo en PDF con la lista de reservas
    """
    lis = listar()

    # print(lis)
    
    # crea instancia FPDF
    pdf = PDF()

    # agrega página
    pdf.add_page()
    
    # alto del renglón
    alto = 10
    
    # líneas de contenido
    for p in lis:       
        pdf.cell(40, alto, p[1], 0, 0, 'L')
        pdf.cell(30, alto, p[2], 0, 0, 'L')
        pdf.cell(30, alto, p[3], 0, 0, 'L')
        pdf.cell(30, alto, p[4], 0, 0, 'L')
        pdf.cell(20, alto, str(p[5]), 0, 0, 'R')
        pdf.cell(20, alto, "%.2f"%(p[6]), 0, 1, 'R')
        
        # si la próxima posición vertical es mayor al alto de página
        # menos el margen inferior menos el alto de un renglón
        # agrega una página (genera pie de pagina en página actual y 
        # encabezado en la nueva)
        if pdf.get_y() > (pdf.max_y - pdf.m_inf - alto):
            pdf.add_page()
                    
    # genera el archivo
    pdf.output('lista_pasajeros.pdf', 'F')


if __name__ == '__main__':
    # print(listar())
    # print("------")
    # print(listar(" nombre like 'A%'"))
    # print("------")
    # print(listar(" dni > 40000000"))
    # print(dar_lugares())
    
    lista_a_pdf()

        


