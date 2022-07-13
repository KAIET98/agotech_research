

import logging
import requests
from metereologia_lalon_class import mi_metereologia

host = '34.79.75.171'
user = 'admin'
password = '12345678'
database = 'GET_DATABASE'

#El objetivo de esta función es la construcción de una función que sirva para insertar 
#lineas en una tabla de sql.

import pandas as pd
import numpy as np
import pymysql
#import cryptography
import pandas as pd

'''
------------------- AWS OLD CONNECTION --------------
host = 'database-1.cq2dp4jmizro.eu-west-1.rds.amazonaws.com'
user = 'admin'
password = '12345678'
database = 'GET_DATABASE'

'''
#----------------------- GCP connection-----------------

host = '35.241.159.127' #este el el host nuevo
user = 'admin'
password = '12345678'
database = 'GET_DATABASE'

def insert_into(data, arrival_df):

    #establecemos la conexión a la base de datos
    connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=database)

    cursor = connection.cursor()


    #especificamos cual es el nombre de la tabla destino

    nombre_tabla = arrival_df

    
    # creating column list for insertion
    cols = "`,`".join([str(i) for i in data.columns.tolist()])
    cols = cols.strip()
    # Insert DataFrame recrds one by one.
    for i,row in data.iterrows():
        sql = "INSERT INTO `{}` (`".format(nombre_tabla) +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"

            
        cursor.execute(sql, tuple(row))

            # the connection is not autocommitted by default, so we must commit to save our changes
        connection.commit()



'''
def conectame(host, user, password, database):

    #conn = pymysql.connect(host=host, user=user, password=password, port=3306, db='GET_DATABASE',charset='utf8')

    connection = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                db=database)

    cursor = connection.cursor()

    return cursor
cursor = conectame(host, user, password, database)
'''

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=host, user=user, passwd=password, db=database, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
   # sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

#------------------ creamos la tabla ---------------

def run_query(q):
  with pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=database) as conn:
                             return pd.read_sql(q, conn)



def checkTableExists(conn, tablename):
    dbcur = conn.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

#------------ ESPECIFICAMOS CUAL VA A SER LA TABLA DE INTERÉS------

tabla_de_interes = 'DATOS_METEREOLOGIA_HISTORICO_TBA'



'''
Lanzamos las formulas propias de la clase para averigua qué estacion metereo
logica tenemos al rededor y engancharnos a sus datos

'''

# 1. EJEMPLO USANDO COORDENADAS

#1. Cargamos la clase

api_key_bluetab = 'AIzaSyD7zvwwj8-4JS2XZq0n8bLb9t2cSqStx84'

api_aemet = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'

#introduciomos ahora sí que si las coordenadas de nuestro campo de valencia
#api_key_kaiet = 'AIzaSyB8b6vSNPb7MzEBXXTNRzdkWqLGIKQotmU'
mi_metereologia_clase = mi_metereologia( google_maps_key = api_key_bluetab,\
    coodenadas = (40.5206, 0.351246),\
    api_aemet =  api_aemet)


#Sacamos que provincia me corresponde con la ubicacion que he pasado

provincia =  mi_metereologia_clase.address()



#Sacamos las esatciones de dicha provincia

estaciones_provincia = mi_metereologia_clase.estaciones()

print(estaciones_provincia)

#Extraigo mi latitud y longitud
mi_ubicacion = mi_metereologia_clase.mi_latlon()




#Sacamos la distancias que tengo a las estaciones de mi alrededor

mis_estaciones_distancias_brutas = mi_metereologia_clase.distancias()




#estaciones_provincia['distancia'] = mis_estaciones_distancias_brutas


#Falta sacar la estacion más cercana


estaciones_ordenadas = mi_metereologia_clase.ordenar_distancias(mis_estaciones_distancias_brutas)



print(estaciones_ordenadas)

estacion_mas_cercana_codigo = mi_metereologia_clase.mis_estaciones_mas_cercanas(estaciones_provincia, estaciones_ordenadas)



'''
Y finalmente empezamos subir los datos

'''

if checkTableExists(conn, tabla_de_interes):

  for ano in range(1998, 2022):
    
    print('\n ######################### \n')

    print('Subiendo los datos del año; ', ano)


      #-------- HACEMOS EL SCRAPPING ----------

    df = mi_metereologia_clase.meterelogia_estacion_mas_cercana(fecha_ini =  '{}-01-01'.format(ano), fecha_fin = '{}-12-31'.format(ano))


    df = df.fillna(999)

      #print(df.head())


      #-------- SUBIMOS LOS DATOS --------#

    insert_into(df, tabla_de_interes)
    



   
  
  
else:


  #Primero creamos la tabla
    
  q = '''CREATE TABLE {}(

    fecha   DATE NOT NULL, 
    Estacion VARCHAR(255) NOT NULL, 
    Provincia VARCHAR(255), 
    Temperatura_media INT,
    Precipitacion_l_m3 INT, 
        Temperatura_minima float, 
        Temperatura_maxima float,
        Direccion_viento VARCHAR(255), 
        Velocidad_media float, 
        Presion_maxima float,
          Presion_minima float, 
          Prom_temperatura_media_prov float, 
          Grados_debajo_siete float,
          Presion_externa float
          
          );'''.format(tabla_de_interes)


  print(run_query(q))


  #Y luego insertamos los datos


  for ano in range(1998, 2022):
    
    print('\n ######################### \n')

    print('Subiendo los datos del año; ', ano)


      #-------- HACEMOS EL SCRAPPING ----------

    df = mi_metereologia_clase.meterelogia_estacion_mas_cercana(fecha_ini =  '{}-01-01'.format(ano), fecha_fin = '{}-12-31'.format(ano))


    df = df.fillna(999)

      #print(df.head())


      #-------- SUBIMOS LOS DATOS --------#

    insert_into(df, tabla_de_interes)