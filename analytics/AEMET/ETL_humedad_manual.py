
from SQL_FUNCTIONS.funcionabilidad_insert_into import *
from HUMEDAD.humedad import humedad_ciudad
from datetime import date
from datetime import timedelta
import os


'''

¡¡¡ AVISO !!!

Hoy, 31-05-2022, tenemos en funcionamiento una Google function que nos alimenta los datos de 
Humedad de GET automáticamente por lo que establecemos el parametro insertar = False, para que no
inserte los datos manualmente en la base de datos cuando se ejecute este script. 

Funcionar funciona, pero no queremos que inserte porque ya los inserta Google.

'''

insertar = False

#----- LLAMADA A LA API DE AEMET------


#Especificamos la API_KEY


API_KEY ='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'


df_humedad = humedad_ciudad(API_KEY = API_KEY, codigo_ciud = 2003)

#vemos el resultado de la API
print(df_humedad)



if insertar != False: 


    #finalmente lanzaremos un select * para poder verificar si se cumple el insert into de manera correcta.

    host = '35.241.159.127' #este el el host nuevo
    user = 'admin'
    password = '12345678'
    database = 'GET_DATABASE'




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

    connection = pymysql.connect(host=host,
                                user=user,
                                password=password,
                                db=database)

    cursor = connection.cursor()

    #----- INSERTAMOS LOS DATOS MANUALMENTE -------------------------


    

    #from SQL_FUNCTIONS import *

        
    insert_into(df_humedad, 'HUMEDAD')

    #----- FINALMENTE HACEMOS EL SELECT * FROM; ----------------------
    def run_query(q):
        with pymysql.connect(host=host,
                                user=user,
                                db=database) as conn:
            return pd.read_sql(q, conn)

    q = 'select * from HUMEDAD;'


    print(run_query(q))


    