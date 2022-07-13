

#El objetivo de esta función es la construcción de una función que sirva para insertar 
#lineas en una tabla de sql.

import pandas as pd
import numpy as np
import pymysql
import cryptography
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

    

