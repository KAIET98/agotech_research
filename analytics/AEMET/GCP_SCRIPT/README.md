

En la carpeta hay varios files de dos tipos: 

1. Estaciones_provincia: 

Da como rsultado las estaciones metereologicas de la provincia que estamos investigando 
con sus codigos de latitud y longitud ocmo el codigo identificativo de la estacion. 


2. Datos de metereología (humedad):


Hay un primer archivo que se llama 'clase_extraccion_humedad' donde se extraen 
los valore smetereologicos de un pubeblo dado. 

Tenemos diseñado un script para extraer los datos de la ciudad de Albacete llamado humedad_albacete.py. 

Por toro lado tenemos un nuevo fichero que engloba el código que está en humedad_albacete y lo 
inyecta a un dataframe dado, "humedad_ciudad.py". Su principal funcion es extraer la información
metereologica general de AEMET de una estación dada. Seguidamente compara esta estación con las 
estaciones que tiene al rededor y devuelve un dataframe. 

Vamos a generalizar ese mismo script metiendo todo en una función, esto se va a guardar y 
alojar en el script/módulo "mi_metereologia.py". 


Finalmente, para poder lanzar la query en GCP, hemos creado un archiov llamado "mi_humedad.py" donde
intentaremos llamar al modulo "humedad_ciudad.py" y lanzar la query. 

3. Datos Generales de la metereología

Actualmetne tenemos un script llamado  "estacion_data.py"; vamos a replicar el funcionamiento 
de este script en un módulo entero en "mi_metereologia_modulo.py". Tras ello, lo vamos a llamar 
desde mi_metereologia.py.


Se sabe que la API de aemete en cuanto a los datos generales nos deja como máximo recopilar los datos historicos de 'antes de ayer' es decir: 

hasta = hoy - 2

Dicho esto, podemos definir una frequencia de que suba los datos a GCP cada 2 dias es decir: 

hasta = hoy - 2

desde = hasta - 2

Esta funcionalidad se implementa en el archivo de 'metereologia-finca.py'. El resultado en cambio, va a ser la información del día "desde", es decir de la fecha de hace 4 dias.



## Historicos de metereologia

El archiov de METEREOLOGIA_HISTORICO.ipynb contiene elscript de google collab, NO EJECUTAR, que subio 22 años de historico a Mysql. 

Luego está el script de 'subida_metereologia_max_historic...' que se encarga de subir los datos desde 01-01-2022 hasta 25-03-2022, previo a la implementacion de la funcion de metereologia en GCP.

