


select fecha as DIA, Temperatura_media AS TEMPERATURA_MEDIA_DIARIA
from `GET_DATABASE`.`METEREOLOGIA`
where fecha > (
    select min(fecha) as DIA from DATOS_METEREOLOGIA_HISTORICO_TBA
    )

