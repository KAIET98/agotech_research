

from pickle import NONE
import pandas as pd

import requests
import json
from geopy.distance import geodesic
from folium import FeatureGroup 
import folium
import googlemaps
from datetime import datetime
import matplotlib.pyplot as plt





api_key_bluetab = 'AIzaSyD7zvwwj8-4JS2XZq0n8bLb9t2cSqStx84'

api_aemet = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'

codigo = '8416Y'

def metereologia(fecha_ini, fecha_fin, codigo):
    url = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos"
                "/fechaini/{}T00:00:00UTC/fechafin/{}T00:00:00UTC/estacion/{}".format(fecha_ini, fecha_fin, codigo))

    API_KEY = api_aemet
    querystring = {"api_key": API_KEY}
        
    r = requests.get(url, params=querystring, verify=False)

    # print(r.json())


    def parse_data(raw_data):
        data = []
        
        for d in raw_data:
            d = dict(d)  # Exto copia el parámetro
            for param in ['prec', 'presMax', 'presMin', 'racha', 'sol', 'tmax', 'tmed', 'tmin', 'velmedia', 'altitud', 'dir']:
                try:
                    d[param] = float(d[param].replace(',', '.'))
                except:
                    d[param] = None

            data.append(d)
        return data

    try:

        #print(' El codigo en cuestion ', r.status_code)

        print(r.json())

        

       

        

        if r.json()['estado'] == 200:

            # print(r.json())

            data_url = r.json()['datos']

            return r.json()['estado']

        elif r.json()['estado'] == 404:

            return r.json()['estado']

            #print('ERROR 404')

            


        else: 

            return r.json()['estado']




    except: 

        print('checkea las credenciales')

resultado = {}
for ano in range(1999, 2000):
    for mes in range(1,12):

        print('Estamos en ', ano, ' en ', mes)

        tiempo = '{}-{}'.format(ano, mes)

        resultadofin  = metereologia('{}-{}-01'.format(ano, mes), '{}-{}-31'.format(ano, mes), codigo)

        if resultadofin != 200:

            continue
            print('malll')

        else:


            resultado[tiempo] = resultadofin

        



resultado = pd.DataFrame.from_dict(resultado, orient='index')
print(resultado)


url = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos"
                "/fechaini/{}T00:00:00UTC/fechafin/{}T00:00:00UTC/estacion/{}".format('1998-01-01', '1998-21-31', codigo))

API_KEY = api_aemet
querystring = {"api_key": API_KEY}
r = requests.get(url, params=querystring, verify=False)
    
print(requests.get(r.json()['datos'], params=querystring, verify=False).json())




#resultado.to_csv('resultado.csv')