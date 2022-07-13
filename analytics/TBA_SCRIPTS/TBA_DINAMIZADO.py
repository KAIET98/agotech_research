

from ast import expr_context
from traceback import print_tb
import pymysql
import datetime
from datetime import date
from datetime import timedelta
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import logging
import re
import os
import parameters
from parameters.parameters import *



# 1. Nos conectamos a la base de datos de GET
'''
host = '35.241.159.127' #este el el host nuevo
user = 'admin'
password = '12345678'
database = 'GET_DATABASE'
'''

try: 

  host = host
  user = user
  password = password
  database = database

except: 

  print('... please install environment variables package located in "environment_parameters" ...')

connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=database)

cursor = connection.cursor()


#2. Cargamos un par de funciones

def run_query(q):
    with pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=database) as conn:
        return pd.read_sql(q, conn)

    

# 3. Lanzamos la query para traernos toda la información de nuestra base de datos

q = 'select * from TBA_AGROSENSORS_HISTORIC_TRAINING;'



historico_tba = run_query(q)

#4. Vemos cual es la ultima fecha

last_day_timestamp = historico_tba.loc[historico_tba.shape[0]-1,'FECHA'].strftime('%Y-%m-%d')



#sacamos el dia de hoy 
today = date.today()


#6. Indicamos cual va a ser el rango de fechas que vamos a subir 

#print('El último dia: ', last_day_timestamp, ' y hoy es ', str(today))


#7. Nos conectamos a TBA

host = 'www.tbagrosensor.com'
database = 'tecfrut_ccl'
user = 'tecfrut_eae'
password = '.jvcUtJ?;='

def run_query(q):
    with pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=database) as conn:
        return pd.read_sql(q, conn)


'''
Nos conectamos a la base de datos
'''
logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=host, user=user, passwd=password, db=database, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    #sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


# 8. Vemos que tablas tienen 


'''
le tenemos que pasar :

1 = "-"
2 = "_"

'''

def tba_dia_formato(tipo):
    
    if tipo == 1:


        import re

        stmt = "SHOW TABLES"


        tablas = run_query(stmt)

        #renombramos la tabla de tablas
        tablas = tablas.rename(columns = {"Tables_in_tecfrut_ccl" : "TABLAS"})

        #filtramos


        regex = '^hist'

        tablas = tablas[tablas.TABLAS.str.match(regex)]



        tablas['fechas'] = tablas.TABLAS.str.extract('(\d+\_\d+\_\d+)')

        fechas_formato = []

        for fecha in range(tablas.shape[0]):

            fecha_a_modificar = tablas.iloc[fecha,1]

            fechas_formato.append(re.sub('_', '-', fecha_a_modificar))


        tablas['fechas_off'] = fechas_formato


        #nos quedamos con las columnas que nos interesan

        tablas = tablas[['fechas_off']]

        #los renombramos
        tablas = tablas.rename(columns = {'fechas_off':'fechas'})


        #transformamos a lista para obtener una funcionalidad mayor
        tablas['fechas']

        return tablas
    
    elif tipo == 2:
    
        
        import re

        stmt = "SHOW TABLES"


        tablas = run_query(stmt)

        #renombramos la tabla de tablas
        tablas = tablas.rename(columns = {"Tables_in_tecfrut_ccl" : "TABLAS"})

        #filtramos


        regex = '^hist'

        tablas = tablas[tablas.TABLAS.str.match(regex)]



        tablas['fechas'] = tablas.TABLAS.str.extract('(\d+\_\d+\_\d+)')


        #transformamos a lista para obtener una funcionalidad mayor

        tablas = tablas['fechas']

        return tablas
    
    
    else: 

        print('''
    
    Por favor, indica con un 1 si quieres modificar el string de fecha de "_" a "-"
    o con un 2, si lo quires dejar en "_"
    
    ''')

def insert_into(data, arrival_df):
  
  #establecemos la conexión a la base de datos
  connection = pymysql.connect(host=host,
                            user=user,
                            password=pasw,
                            db=db)

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


#vemos el resultado 
tablas = tba_dia_formato(tipo = 1)




#9. Sacamos cual es el ultimo dia



ultimo = tablas.iloc[tablas.shape[0]-1,:]



#10. Vemos que dias no estan subidos

tablas = pd.to_datetime(tablas['fechas']).reset_index().drop('index', axis = 1)



print('El último dia: ', last_day_timestamp, ' y hoy es ', str(today))

#pasado_timestamp = pd.Timestamp(today.year, today.month, today.day)
      
#extraemos de las tablas, cuales son la fechas que no estan subidas

fechas_no_subidas = tablas[tablas['fechas'] > last_day_timestamp]

print(fechas_no_subidas)

fechas_formato = []

for fecha in range(fechas_no_subidas.shape[0]):

    fecha_a_modificar = fechas_no_subidas.iloc[fecha,0]

    print('La fecha es: ', fecha_a_modificar.strftime('%Y-%m-%d'))

    fecha_string = fecha_a_modificar.strftime('%Y-%m-%d')

    #fecha_string = fecha_a_modificar.strftime('%Y-%m-%d').str.extract('(\d+\-\d+\-\d+)')

    fechas_formato.append(re.sub('-', '_', fecha_string))


fechas_no_subidas['fechas_off'] = fechas_formato

#nos quedamos solo con las columnas que nos interesan 

fechas_no_subidas = fechas_no_subidas[['fechas_off']]

fechas_no_subidas = fechas_no_subidas.rename(columns = {'fechas_off':'fechas'})


print('Fechas arreglado : ',  list(fechas_no_subidas['fechas']))

def informacion_dia(dia, host, db, user, pasw):
    
    host = host
    db = db
    user = user
    pasw = pasw


      
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        conn = pymysql.connect(host=host, user=user, passwd=pasw, db=db, connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
    #sys.exit()

      
    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


  #construimos el string del dia

  
    dia = 'historico_graficas_{}'.format(dia)

    q = """

      select * from {}

      """.format(dia)


    fecha_X = run_query(q)

  # 1. EXTRACCION FECHA --------------------------

  # Tranformamos la fecha a un feature más manejable. esd ecir
  # al que tenemos en la tabla METEREOLOGIA, datos test.


    instante = pd.DataFrame(fecha_X['instante'])

    fecha_X['instante'] = instante.applymap(lambda x: str(x))



    fecha_X['DIA'] = fecha_X.instante.str.extract('(\d+\-\d+\-\d+)')


  # 2. Extracción HORA-------------------------------------------



    hora = pd.DataFrame(fecha_X['instante'])

    fecha_X['hora'] = hora.applymap(lambda x: str(x))


    fecha_X['hora'] = fecha_X['hora'].str.extract('(\d+\:\d+\:\d+)')






  #seleccionamos las columnas


    fecha_X = fecha_X[['id_nodo', 	'var1', 	'var2', 	'var3', 	'var4', 	'var5', 	'var6', 	'var7',  'var8',	'var9', 'var12', 'var13', 'var14', 'hora', 'DIA']]


  # renommbramos las columnas

       
        



    fecha_X = fecha_X.rename(columns = {

      'var1' : 'HUMEDAD_1', \
      'var2' : 'HUMEDAD_2', \
      'var3' : 'HUMEDAD_3', \
      'var4' : 'HUMEDAD_4', \
      'var5' : 'HUMEDAD_5', \
      'var6' : 'HUMEDAD_6', \
      'var7' : 'COLUMNA_7', \
      'var8' : 'TEMPERATURA', \
      'var9' : 'HUMEDAD_RELATIVA', \
      'var12' : 'VELOCIDAD_VIENTO', \
      'var13' : 'LLUVIA', \
      'var14' : 'DIRECCION_VIENTO', \
     # 'var15' : 'FECHA', \
      'DIA':'FECHA', \
      'hora': 'HORA'

                                      })


  #3. Adecuación de datos -----------------------------
      

    fecha_X['HUMEDAD_1'] = fecha_X['HUMEDAD_1'] / 100
    fecha_X['HUMEDAD_2'] = fecha_X['HUMEDAD_2'] / 100
    fecha_X['HUMEDAD_3'] = fecha_X['HUMEDAD_3'] / 100
    fecha_X['HUMEDAD_4'] = fecha_X['HUMEDAD_4'] / 100
    fecha_X['HUMEDAD_5'] = fecha_X['HUMEDAD_5'] / 100
    fecha_X['HUMEDAD_6'] = fecha_X['HUMEDAD_6'] / 100
    fecha_X['COLUMNA_7'] = fecha_X['COLUMNA_7'] / 100
    fecha_X['TEMPERATURA'] = fecha_X['TEMPERATURA'] / 100
    fecha_X['HUMEDAD_RELATIVA'] = fecha_X['HUMEDAD_RELATIVA'] / 100
    fecha_X['VELOCIDAD_VIENTO'] = fecha_X['VELOCIDAD_VIENTO'] / 100
    fecha_X['LLUVIA'] = fecha_X['LLUVIA'] / 100
    fecha_X['DIRECCION_VIENTO'] = fecha_X['DIRECCION_VIENTO'] / 100



    return fecha_X


if len(list(fechas_no_subidas)) >= 1:


    #print(fechas_no_subidas)



    #fechas_no_subidas['fechas_bien'] = fechas_no_subidas['fechas'].str.extract('(\d+\-\d+\-\d+)')


    
    #print(fechas_no_subidas)



      #tablas = list(fechas_no_subidas['fechas'].str.extract('(\d+\-\d+\_\d+)'))

    #tablas = tba_dia_formato(tipo = 2)

    #print(tablas)

    #por cada fecha

    for fecha in list(fechas_no_subidas['fechas']):

      #construimos el nombre de la tabla a filtrar

      print('\n Subiremos la tabla: ')

      print('historico_graficas_{}'.format(fecha), '\n')


      #nos quedamos con el nombre de la tabla

      tabla_nomobre = 'historico_graficas_{}'.format(fecha)


      #llamamos a la base de datos de TBA

      host = 'www.tbagrosensor.com'
      db = 'tecfrut_ccl'
      user = 'tecfrut_eae'
      pasw = '.jvcUtJ?;='

      historico_limpio = informacion_dia(fecha, host, db, user, pasw)

      print(historico_limpio.head(2))




      

      print('\n', 'Subimos el historico de la tabla {}'.format(tabla_nomobre), '\n')

      '''

      Antes de subir nada, nos conectamos a nuesta base se datos de GET

      '''
      host = host
      user = user
      password = password
      database = database


      '''
      Nos conectamos a la base de datos
      '''
      logger = logging.getLogger()
      logger.setLevel(logging.INFO)

      try:
          conn = pymysql.connect(host=host, user=user, passwd=pasw, db=db, connect_timeout=5)
      except pymysql.MySQLError as e:
          logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
          logger.error(e)
          #sys.exit()

      logger.info("SUCCESS: Connection to RDS MySQL instance succeeded", "\n")





      print('En si insertariamos!!!!!!')

      insert_into(historico_limpio, 'TBA_AGROSENSORS_HISTORIC_TRAINING')




      print('##############')

else: 

    print('\n', 'GET Training Sensorica está actualizado')

