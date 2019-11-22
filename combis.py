#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
  
import sqlite3
from fpdf import FPDF

conn = sqlite3.connect('combis.db')

conn.execute('''CREATE TABLE if not exists COMBIS
     (id       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      nombre   TEXT             NOT NULL,      
      telefono TEXT             NOT NULL,
      subeEn   TEXT,
      bajaEn   TEXT,
      nroAsiento  INT, 
      pago     INT             
     );''')
    
conn.execute('''CREATE TABLE if not exists LUGARES
     (id       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      nombre   TEXT             NOT NULL,
      codpost  TEXT             
     );''')

# qry = f'''INSERT INTO combis ( nombre, telefono, subeEn, bajaEn, nroAsiento, pago) VALUES
             # ( 'Francisco', '427325', '9 de julio 222', 'Abasto', 8, 600)
            # '''
# conn.execute(qry)

# qry = f'''INSERT INTO LUGARES( nombre) VALUES
          # ( 'CABA') '''
# conn.execute(qry)
# qry = f'''INSERT INTO LUGARES( nombre) VALUES
          # ( 'Lujan') '''        
# conn.execute(qry)
# conn.commit()    
      
def dar_lugares():
    cc = conn.execute("SELECT * FROM lugares")
    
    return list(cc)    

def agregar(valores):
    qry = '''INSERT INTO combis 
                (nombre, telefono, subeEn, 
                bajaEn, nroAsiento, pago) 
          VALUES
                ('{}', '{}', '{}', '{}', {}, {})                
        '''.format(valores['nombre'],\
        valores['tele'],valores['sube'],\
        valores['baja'],valores['asiento'],\
                        int(valores['pagado']))
                        
    # print(qry)                        
                        
    conn.execute(qry)
    conn.commit()    

def modificar(valores, ide):
    print(" ", valores)
    qry = '''UPDATE combis SET
                nombre = '{}', 
                telefono = '{}', 
                subeEn = '{}', 
                bajaEn = '{}', 
                nroAsiento = {},
                pago = {} 
            where id = {}
            '''.format(valores['nombre'],\
        valores['tele'],valores['sube'],\
        valores['baja'],valores['asiento'],\
                        int(valores['pagado']), int(ide))
                        
    print(qry)                      
                        
    conn.execute(qry)
    conn.commit()    
    
      
def borrar(rid):
    qry = '''DELETE FROM combis WHERE id = {}'''.format(rid)
                            
    print(qry)
                            
    conn.execute(qry)
    conn.commit()            
      
def listar(condi = ""):
    if condi != "":
        condi = " where " + condi
        
    cc = conn.execute("SELECT * FROM combis" + condi)
    
    return list(cc)

    cc.close()        
      
def lista_a_pdf():
    lis = listar()

    print(lis)
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    pdf.cell(0, 0, 'Lista de pasajeros', 0, 1, 'C')
    linea = 0
    pdf.set_font('Arial', 'B', 10)
    
    pdf.cell(0, 20, "", 0, 1, 'L')
    
    alto = 10
    
    pdf.cell(40, alto, "nombre", 0, 0, 'L')
    pdf.cell(30, alto, "teléfono", 0, 0, 'L')
    pdf.cell(30, alto, "origen", 0, 0, 'L')
    pdf.cell(30, alto, "destino", 0, 0, 'L')
    pdf.cell(20, alto, "asiento", 0, 0, 'C')
    pdf.cell(20, alto, "pagó", 0, 1, 'C')
    
    pdf.line(pdf.get_x(), pdf.get_y(), 200, pdf.get_y())
    
    for p in lis:       
        pdf.cell(40, alto, p[1], 0, 0, 'L')
        pdf.cell(30, alto, p[2], 0, 0, 'L')
        pdf.cell(30, alto, p[3], 0, 0, 'L')
        pdf.cell(30, alto, p[4], 0, 0, 'L')
        pdf.cell(20, alto, str(p[5]), 0, 0, 'R')
        pdf.cell(20, alto, "%.2f"%(p[6]), 0, 1, 'R')
        
        #linea += 15
                         
    pdf.output('lista_pasajeros.pdf', 'F')

if __name__ == '__main__':
    print(listar())
    print("------")
    print(listar(" nombre like 'A%'"))
    print("------")
    print(listar(" dni > 40000000"))
    print(dar_lugares())
    
    lista_a_pdf()

        


