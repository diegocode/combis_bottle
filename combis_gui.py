import combis

from bottle import route, run, template, request, static_file

@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='.')

@route('/')
def menu():
    return template("index.html")
    
@route('/lista_pdf')
def lista_pdf():
    listita = combis.listar()   
    combis.lista_a_pdf()
    return template('lista_combis.html', listado = listita)

@route('/lista')
def listado():
    listita = combis.listar()   
    # print(listita) 
    return template('lista_combis.html', listado = listita)

@route('/reserva')        
@route('/editar', method='get')       
def editar():
    if len(request.GET) > 0:
        rid = request.GET.get("id")
        datos = combis.listar(" id = {}".format(rid))
    else:
        rid = ""
        datos = []
        datos.append([""] * 10)
        
    return template('modificar.html', datorig = datos[0], lista_lugares=combis.dar_lugares())   
    
@route('/editar_post', method='post')
def editar_post():
    ide = request.POST.get("id")
    
    d = dict(request.POST)
    
    try:
        d["pagado"] = float(d["pagado"])
    except:
        d["pagado"] = 0
    
    try:
        ide = int(ide)
    except:
        ide = -1
    
    if ide == -1:
        combis.agregar(d)
    else:
        combis.modificar(d, ide)
    
    listita = combis.listar()    
   
    return template('lista_combis.html', listado = listita)        
    
@route('/borrar', method='get')
def borrar_reserva():
    rid = request.GET.get("id")
    combis.borrar(rid)        

    listita = combis.listar()    
   
    return template('lista_combis.html', listado = listita)    
  
@route('/buscar_resultado', method='get')
def consulta_combis():
    abuscar = request.GET.get("telbuscar")
    #listita = combis.listar(" telefono like %s" % (abuscar))
    listita = combis.listar(" telefono like '{}%'".format(abuscar))    
    return template('lista_combis.html', listado = listita)

if __name__ == '__main__':    
    run(host='0.0.0.0', port=8080, debug=True, reloader=True)
