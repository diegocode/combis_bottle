#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 

import combis

from bottle import route, run, template, request, static_file


@route('/<filepath:path>')
def server_static(filepath):
    """ para archivos estáticos (.css, imagenes, etc.) """
    return static_file(filepath, root='.')


@route('/')
def menu():
    """ index """
    return template("index.html")


@route('/lista_pdf')
def lista_pdf():
    """ listado en pdf """
    
    combis.lista_a_pdf()
    
    # obtiene la lista de reservas
    listita = combis.listar()
    
    return template('lista_combis.html', listado = listita)


@route('/lista')
def listado():
    """ lista reservas """
    
    # obtiene la lista de reservas
    listita = combis.listar()   
    
    return template('lista_combis.html', listado = listita)


@route('/reserva')        
@route('/editar', method='get')       
def editar():
    """ alta o modificación de reserva """
    
    if len(request.GET) > 0:
        # si hay datos en el GET es modificación
        
        # del GET obtiene id de la reserva...
        rid = request.GET.get("id")
        
        # ...y obtiene los datos correspondientes
        datos = combis.listar(" id = {}".format(rid))
    else:
        # si el GET está vacío es alta        
        datos = []
        datos.append([""] * 10) # arma una lista de 10 elementos vacíos 
                                # para pasar a modificar.html
                                # (en lugar de 10 se puede usar cualquier número mayor a
                                # la cantidad de columnas de la tabla reservas*)
        
    return template('modificar.html', datorig = datos[0], lista_lugares=combis.dar_lugares())   
  

@route('/editar_post', method='post')
def editar_post():
    """ alta o modificación de reserva """
    
    # obtiene los datos enviados desde el formulario
    d = dict(request.POST)
    
    # por si "pagado" no es número...
    try:
        d["pagado"] = float(d["pagado"])
    except:
        d["pagado"] = 0
  
    if len(d["id"]) == 0:        
        # si el id recibido es vacío, se agrega
        combis.agregar(d)
    else:
        # si el id no es nulo (ya existe) 
        # se modifica
        combis.modificar(d)
    
    # obtiene la lista de reservas
    listita = combis.listar()    
   
    return template('lista_combis.html', listado = listita)        


@route('/borrar', method='get')
def borrar_reserva():
    """ borra reserva """
    
    # del GET, obiene id de la reserva 
    rid = request.GET.get("id")
    
    # borra la reserva con id = rid
    combis.borrar(rid)        

    # obtiene la lista de reservas
    listita = combis.listar()    
   
    return template('lista_combis.html', listado = listita)    


@route('/buscar_resultado', method='get')
def consulta_combis():
    """ busca reserva """

    # del GET obtiene el teléfono 
    abuscar = request.GET.get("telbuscar")
    
    # obtiene lista de reservas con el teléfono indicado...     
    listita = combis.listar(" telefono like '%{}%'".format(abuscar))    
        
    return template('lista_combis.html', listado = listita)


if __name__ == '__main__':    
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)

