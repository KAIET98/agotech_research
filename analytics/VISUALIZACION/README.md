En esta carpeta están las queries que se lanzan a PowerBI para obtener datos.

# Humedad

1. En un principio en **datos_humedad_get.sql**, se lanza una query para ver como obtenemos los datos relativos a la humedad. 

2. Luego en la consulta de **humedad_media.sql** ya modificamos la consulta anterior para obtener una media de humedad por cada dia, que esto nos dara una visión más global sobre la humedad en el dia. 

3. En la consulta de **humedad_media_horaria** se establece la misma logica que en la segunda consulta pero en este caso obtenienod una media por hora.

4. También sería intersante ver cómo evoluciona la humedad con los datos de TBA. Para ello atacaremos los datos de la sensórica. **humedad_diaria_tba**.

5. Luego, sería interesante comparar en un mismo gráfico de líneas como fluctua la humedad en los terrenos de TBA por medio de la sensorica y por otro lado en los terrenos de GET. **tba_humedad_get_date**, este fichero se crea para extraer datos de la sensorica de TBA, que concuerden en fechas con los datos de GET. 


Entonces tendría dos partes analíticas: 

- VIEW_humedad_tba_and_get: donde se crea la vista con los datos de la humedad de tba, que parte desde la fecha mínima de GET. 

- humedad_tba_conjunt_get: donde se comparan las dos tablas, y nos quedamos con las fechas de get, pero con la humedad de TBA.


# Temperatura

CARPETA (/TEMPERATURA)

## Temperatura GET (TEST)

1. **Temperatura_med_get.sql**, recoge los datos de la temperatura media de cada dia de Albacete.



## Temperatura TRA (TRAIN)

1. **Temperatura_med_tba.sql**, estos recogen los datos de la temperatura media diaria de Valencia, es decir los datos de Training.