# combis_bottle

Sencillo ejemplo utilizando:
 
 * bottlepy + pyfpdf + sqlite

- Permite agregar, eliminar o modificar reservas para una (única!) combi / bus. 
- Genera un listado en pantalla y en PDF (utilizando PyFPDF)
- Permite buscar reservas por el número de teléfono 

Utiliza solo dos tablas:

- Reservas:

 id, nombre, teléfono, subeEn (origen), bajaEn (destino), nroAsiento, pago

y 

- Lugares:

 id, nombre, codpost


Instalar PyFPDF con

- sudo pip3 install fpdf

bottle.py puede estar en la carpeta de combis_gui.py
(descargar y copiar; en linux:  wget http://bottlepy.org/bottle.py )


* bottle: https://bottlepy.org
* PyFPDF: https://pyfpdf.readthedocs.io
