

select fecha as DIA, humedad_relativa as HUMEDAD_RELATIVA 
from `GET_DATABASE`.`TBA_AGROSENSORS_HISTORIC_TRAINING`

where fecha > (
    
    #para hacer el filtrado, sacamos la fecha mínima
    #de los datos de get sobre la humedad, pero como eso 
    #mismo lo tenemos en dos tablas, primero lanzamos
    #una subconsulta interna para crear el dataset de la humedad

    #sobre eso calculamos cual es la fecha minima, y filtramos
    #los dtos de TBA sensorica con eso
    select min(DIA) as DIA from 


        (

            select * from `HUMEDAD`
            UNION
            sel
            ect * from `HUMEDAD_prueba`



        ) as HUMEDAD_GET
    
    )
