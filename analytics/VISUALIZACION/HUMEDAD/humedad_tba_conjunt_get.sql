
SELECT * FROM (
    
    select fecha as DIA, humedad_relativa as HUMEDAD_RELATIVA 
    from `GET_DATABASE`.`TBA_AGROSENSORS_HISTORIC_TRAINING`

    where fecha > (
        
    
        select min(DIA) as DIA 
        from (

                select * from `HUMEDAD`
                UNION
                select * from `HUMEDAD_prueba`



            ) as HUMEDAD_GET
        
    ) as get_humedad

) as HUMEDAD_TBA_GET_RELATIVE 

left join (
    
    select DIA
    from (
     
        select  DIA, ROUND(avg(Humedad_relativa),2) as humedad_media 
        from (
            select * from `HUMEDAD`

            UNION

            select * from `HUMEDAD_prueba`
        
        ) as HUMEDAD
        GROUP BY DIA 
    
    
    ) as humedad_diaria_get  

) as B

on HUMEDAD_TBA_GET_RELATIVE.DIA = B.DIA;

