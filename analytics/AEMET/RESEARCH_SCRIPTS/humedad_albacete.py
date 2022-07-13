
import pandas as pd
import requests
import numpy as np 
from datetime import date 

url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/0{}".format(2003)
key_personal = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'
API_KEY = key_personal
        
        #API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'
        #url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"

querystring = {"api_key":API_KEY}

headers = {
            'cache-control': "no-cache"
                }

response = requests.request("GET", url, headers=headers, params=querystring)

print('El response es: ', response.status_code)

if response.status_code == requests.codes.OK:
    print(response.json())
  
    data_url = response.json()['datos']
  
        #print('La URL que vamos a scrappear es: ', data_url)

        #print('\n La url que vamos a gestionar es: ', data_url, '\n')

    r_data = requests.get(data_url, params=querystring, verify=False)

  
        #print('Y los datos son: ', r_data)

        #Una vez que sabemos que podemos extraer los dtos, los transformamos a un formato json.

    raw_data = r_data.json()
    

    #Extraemos los datos que nos interesan del JSON

    diccionario_base = raw_data[0]['prediccion']
    diccionario_dia_data = diccionario_base['dia']


            


    print('Llamada a la API realizada :) \n')

    print(pd.DataFrame(diccionario_dia_data))


    humedadRelativa = pd.DataFrame(diccionario_dia_data[0]['humedadRelativa'])
#rachaMax = rachaMax.rename(columns= {'value':'Racha_max', 'periodo':'Rango_horas'})



    humedadRelativa_humedad = []
    humedadRelativa_hora = []

    for i in range(humedadRelativa['dato'].shape[0]):
        humedadRelativa_humedad.append(humedadRelativa['dato'][i]['value'])
        humedadRelativa_hora.append(humedadRelativa['dato'][i]['hora'])


    humedadRelativa['humedadRelativa_humedad'] = humedadRelativa_humedad

    humedadRelativa['humedadRelativa_hora'] = humedadRelativa_hora


    humedadRelativa = humedadRelativa.drop('dato', axis = 1)


    humedadRelativa = humedadRelativa.rename(columns = {'maxima':'HumedadRelativa_maxima',\
                                            'minima':'HumedadRelativa_minima',\
                                            'humedadRelativa_humedad':'Sensacion_termica_grados',\
                                            'humedadRelativa_hora':'Hora_humedad'})


#-------------------- CAMBIAMOS EL CAMPO DE HORA DEL DATAFRAME


                #parada dde concepto:

    print(humedadRelativa.head())

    def transformar_hora_humedad(hora):
        import time
        today = date.today()
        time = time.strftime("{}:00:00".format(hora))
        dia_completo = "{} {}".format(today, time)
        return dia_completo
  #print("Today's date:", today, time)

# Lo guardamos todo en una lista


    horas_generales = []

    for hora in humedadRelativa['Hora_humedad']:
        horas_generales.append(
        transformar_hora_humedad(hora)
                    )


# Seleccionamos solo las columnas que nos interesan

    humedadRelativa['Hora_generica'] = horas_generales

    humedadRelativa = humedadRelativa.drop('Hora_humedad', axis = 1)

    humedadRelativa = humedadRelativa.drop('HumedadRelativa_maxima', axis = 1)

    humedadRelativa = humedadRelativa.drop('HumedadRelativa_minima', axis = 1)

    df_humedad = pd.DataFrame(humedadRelativa)  

    print('####################### \n')      

    print(df_humedad.head())   
    
    #return df_humedad


    #print(diccionario_dia_data.head())




    
    