# combis_bottle

Sencillo ejemplo utilizando:
 
 * bottlepy, 
 * pyfpdf, 
 * sqlite

- Permite agregar, eliminar o modificar reservas para una (única!) combi / bus. 
- Genera un listado en pantalla y en PDF (utilizando PyFPDF)
- Permite buscar reservas por el número de teléfono 

Utiliza solo dos tablas:

- Combis:

 id, nombre, teléfono, subeEn (origen), bajaEn (destino), nroAsiento, pago

y 

- Lugares:

 id, nombre, codpost

