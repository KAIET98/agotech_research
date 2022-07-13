

select  DIA, ROUND(avg(Humedad_relativa),2) as humedad_media from (
    select * from `HUMEDAD`

    UNION

    select * from `HUMEDAD_prueba`
    
) as HUMEDAD
GROUP BY DIA;









