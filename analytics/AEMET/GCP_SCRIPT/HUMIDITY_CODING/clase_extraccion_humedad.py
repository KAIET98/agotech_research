from mimetypes import init
import requests
import pandas as pd
import numpy as np
from datetime import date 
import time

from sympy import Q



class metereologia_ciudad_humedad:


    def __init__(self, key_personal, codigo_ciudad):

        self.key_personal = key_personal
        self.codigo_ciudad = codigo_ciudad


        try: 

            #codigo oficial de albacete 02003
        #Tener en cuenta que el codigo de albacete empieza por medio de un 0
        #como no se puede leer ese 0 al meter la sentencia, le hemos puesto un 0
        #antes de las llaves!!!!!
        
            url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/0{}".format(self.codigo_ciudad)

            API_KEY = self.key_personal
        
        #API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'
        #url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"

            querystring = {"api_key":API_KEY}

            headers = {
            'cache-control': "no-cache"
                }

            response = requests.request("GET", url, headers=headers, params=querystring)

            print('El response es: ', response.status_code)

            if response.status_code == requests.codes.OK:
  
  #print(r.json())

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
            print(diccionario_dia_data.head())
            return diccionario_dia_data

            print('Dataframe devuelto')
            
        
        except: 

            print('No se puede hacer la llamada a la API')


    def metereologia_ciudad(self):
        
        
        try: 

            
    #Datos sobre la precipitacion 

    #Probabilidad precipitacion: 
            
            probPrecipitacion = pd.DataFrame(diccionario_dia_data[0]['probPrecipitacion'])
            probPrecipitacion = probPrecipitacion.rename(columns= {'value':'Probabilidad_precipitacion', 'periodo':'Rango_horas'})


    # cotaNieveProv

            cotaNieveProv = pd.DataFrame(diccionario_dia_data[0]['cotaNieveProv'])
            cotaNieveProv = cotaNieveProv.rename(columns= {'value':'Probabilidad_nieve', 'periodo':'Rango_horas'})
    

    # estadoCielo

            estadoCielo = pd.DataFrame(diccionario_dia_data[0]['estadoCielo'])
            estadoCielo = estadoCielo.rename(columns= { 'periodo':'Rango_horas', 'descripcion':'Tipo_Cielo'})

    # Viento 

            viento = pd.DataFrame(diccionario_dia_data[0]['viento'])
            viento = viento.rename(columns= { 'direccion':'Direccion_viento', 'velocidad':'Velocidad_viento', 'periodo':'Rango_horas'})


    ## rachaMax

            rachaMax = pd.DataFrame(diccionario_dia_data[0]['rachaMax'])
            rachaMax = rachaMax.rename(columns= {'value':'Racha_max', 'periodo':'Rango_horas'})


    ## # temperatura

            temperatura = pd.DataFrame(diccionario_dia_data[0]['temperatura'])
#rachaMax = rachaMax.rename(columns= {'value':'Racha_max', 'periodo':'Rango_horas'})
            value_temperatura = []
            value_hora = []

            for i in range(temperatura['dato'].shape[0]):
        #print(temperatura['dato'][i]['value'])

  #ñadimos el valor de la 'temperatura a la lista

                value_temperatura.append(temperatura['dato'][i]['value'])
  

        #añadimos la hora a dicha lista

                value_hora.append(temperatura['dato'][i]['hora'])



            temperatura['value_temperatura'] = value_temperatura
            temperatura['value_hora'] = value_hora


            temperatura = temperatura.drop('dato', axis = 1)


            temperatura = temperatura.rename(columns = {'maxima':'Temperatura_maxima',\
                                            'minima':'Temperatura_minima',\
                                            'value_temperatura':'Temperatura_tipo_2',\
                                            'value_hora':'Hora'})

    # sensTermica


            sensTermica = pd.DataFrame(diccionario_dia_data[0]['sensTermica'])
    #rachaMax = rachaMax.rename(columns= {'value':'Racha_max', 'periodo':'Rango_horas'})



            sensTermica_temperatura = []
            sensTermica_hora = []

            for i in range(sensTermica['dato'].shape[0]):
            
                sensTermica_temperatura.append(sensTermica['dato'][i]['value'])
  

  #añadimos la hora a dicha lista

                sensTermica_hora.append(sensTermica['dato'][i]['hora'])

            sensTermica['value_sensTermica'] = sensTermica_temperatura

            sensTermica['hora_sensTermica'] = sensTermica_hora


            sensTermica = sensTermica.drop('dato', axis = 1)


            sensTermica = sensTermica.rename(columns = {'maxima':'Temperatura_termi_maxima',\
                                            'minima':'Temperatura_termi_minima',\
                                            'value_sensTermica':'Sensacion_termica_grados',\
                                            'hora_sensTermica':'Hora_sens'})




            def humedad_ciudad(self):
                
                
                humedadRelativa = pd.DataFrame(diccionario_dia_data[0]['humedadRelativa'])
#rachaMax = rachaMax.rename(columns= {'value':'Racha_max', 'periodo':'Rango_horas'})



                humedadRelativa_humedad = []
                humedadRelativa_hora = []

                for i in range(humedadRelativa['dato'].shape[0]):

        #print(temperatura['dato'][i]['value'])

  #ñadimos el valor de la 'temperatura a la lista

                    humedadRelativa_humedad.append(humedadRelativa['dato'][i]['value'])

                

        #añadimos la hora a dicha lista

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

                humedadRelativa = humedadRelativa.drop(['HumedadRelativa_maxima', 'HumedadRelativa_minima'], axis = 1)

                if humedadRelativa.columns[0] == 'Sensacion_termica_grados':
                    humedadRelativa = humedadRelativa.rename(columns = {'Sensacion_termica_grados':'Humedad_Relativa'})



                
                print(humedadRelativa)
                #return humedadRelativa






        except:

            print('Revisa el código algo está fallando')


