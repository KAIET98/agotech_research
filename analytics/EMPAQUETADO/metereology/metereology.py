
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

from funciones_auxiliares.lat_lon import latitud_decimal, longitud_decimal

from funciones_auxiliares.province_search import *

from funciones_auxiliares.province_extraction import search_province

class mi_metereologia: 

    def __init__(self, informacion_adress  = None, google_maps_key = None, coodenadas = None, api_aemet = None, fecha_ini = None, fecha_fin = None):

        self.adress =  informacion_adress

        self.google_maps = google_maps_key

        self.aemet = api_aemet

        self.coordenadas = coodenadas

        self.fecha_ini = fecha_ini

        self.fecha_fin = fecha_fin

        if self.coordenadas != None:

            print('Busqueda por coordenadas')
    
    

    





    '''
    Obtenemos la provincia donde vive el usuario
    
    '''

    
    def address(self):

        
        if self.coordenadas != None:

            gmaps = googlemaps.Client(key=self.google_maps)

            coordenadas = self.coordenadas

            reverse_geocode_result = gmaps.reverse_geocode(coordenadas)

            for element in reverse_geocode_result[0]:

                print(element, end = "\n")

                if isinstance(element[0], dict):

                    for elekey in element[0].keys():

                        print(element, '  ', element[0][elekey], "\n") 
                else: 

                    print('{} es una lista'.format(element))



            
           



            if 'long_name' in reverse_geocode_result[0]['address_components'][3]: 

                print('la provincia es: ', reverse_geocode_result[0]['address_components'][3]['long_name'])


                self.resultado  = reverse_geocode_result[0]['address_components'][3]['long_name']


                if 'geometry' in reverse_geocode_result[0].keys(): 

                    if 'location' in reverse_geocode_result[0]['geometry']:


                        self.latitude = reverse_geocode_result[0]['geometry']['location']['lat']

                        self.longitude = reverse_geocode_result[0]['geometry']['location']['lng']



                        print('Tenemos info geolocalizada :)', '\n', self.latitude , ", ", self.longitude)
                    
                    try: 

                        self.provincia = search_province(reverse_geocode_result[0]).upper()

                        #self.provincia = reverse_geocode_result[0]['address_components'][3]['long_name'].upper()

                        print('Provincia optenida :)', '\n', self.provincia )


                    #Ejecutamos la función de visualización del mapa

                    # mapa = ver_mapa(provincia)


                    
                    

                    except: 


                        print('No se puede sacar la provincia')

        
        else:


            gmaps = googlemaps.Client(key=self.google_maps)
            
            geocode_result = gmaps.geocode(str(self.adress))

            if 'geometry' in geocode_result[0].keys(): 

                if 'location' in geocode_result[0]['geometry']:


                    latitude = geocode_result[0]['geometry']['location']['lat']

                    longitude = geocode_result[0]['geometry']['location']['lng']



                    print('Tenemos info geolocalizada :)', '\n')

                try: 

                    self.provincia = geocode_result[0]['address_components'][3]['long_name'].upper()

                    print('Provincia optenida :)', '\n', self.provincia )


                #Ejecutamos la función de visualización del mapa

                # mapa = ver_mapa(provincia)


                
                

                except: 


                    print('No se puede sacar la provincia')




        
        #return mapa

        return self.provincia



    def estaciones(self): 

        #1. Primero sacamos cuale son las estaciones de españa


        url = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"

        #api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'
        querystring = {"api_key":self.aemet}

        headers = {
            'cache-control': "no-cache"
            }

        response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)

        if response['estado'] == requests.codes.OK:

            #nos hacemos con el enlace
            enlace  = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)['datos']

            estaciones = pd.DataFrame(requests.get(enlace, params=querystring, verify=False).json())

        
        if self.provincia == 'VALENCIAN COMMUNITY':
          
          self.provincia = 'VALENCIA'

        if self.provincia == 'CASTILE-LA MANCHA':
          
          self.provincia = 'CASTILLA-LA MANCHA'

        if self.provincia == 'VALENCIAN COMMUNITY':
          
          self.provincia = 'VALENCIA'

        if self.provincia == 'CASTELLÓN':
          
          self.provincia = 'CASTELLON'

        print(estaciones['provincia'].unique())
        

        estaciones_provincia = estaciones[estaciones['provincia'] == self.provincia][['indicativo', 'latitud', 'nombre', 'longitud']]



        #2. Filtramos las estaciones por la provincia que me corresponde como usuario


        #modiifico laas columnas de latitud y longitud


        estaciones_provincia['latitud_num_or']= estaciones_provincia.latitud.str.extract('(\d+)')
        estaciones_provincia['longitud_num_or']= estaciones_provincia.longitud.str.extract('(\d+)')


        estaciones_provincia = estaciones_provincia[["indicativo", "nombre", "latitud_num_or",  "longitud_num_or"]]


        # cambiamos los nombres de las columnas

        estaciones_provincia = estaciones_provincia.rename(columns={'nombre': 'Estacion', 'latitud_num_or': 'Latitud', 'longitud_num_or': 'Longitud'})[['Estacion', 	'Latitud', 	'Longitud', 'indicativo']].reset_index().drop('index', axis = 1)

        #definimos la lista donde guardaremos los resultados



        '''
        Importamos las funciones de modificacion de datos de longitud latitud
        
        

        def latitud_decimal(latitud_ini, lista):
            
            grados_lat = latitud_ini[:2]
            min_lat = int(latitud_ini[2:4])/60
            seg_lat = int(latitud_ini[4:6])/3600
            latitud_decim = int(grados_lat)+min_lat+seg_lat
            
            #guardamos el resultado en una lista

            lista.append(latitud_decim)



        def longitud_decimal(longitud_ini, lista_lon):

            grados_lon = longitud_ini[:2]
            min_lon = int(longitud_ini[2:4])/60
            seg_lon = int(longitud_ini[4:6])/3600
            longitud_decim = -1*(int(grados_lon)+min_lon+seg_lon)

            lista_lon.append(longitud_decim)

        '''



        #0. Definimos las listas donde gaurdaremos los resultados de las localizacion
        #es de las estaciones
        latitudes = []
        lista_longitudes = []

        #print('El tamaño de esatciones_provincia es: ', len(estaciones_provincia))

        #print(estaciones_provincia)

        #Transformaeremos cada laittud y longitud qu eencontremos en el dataset 
        for linea in range(len(estaciones_provincia)):

        #1. Luego definimos las funcioens para obtener los resutlados

            latitud_decimal(estaciones_provincia.iloc[linea,1], latitudes)
            longitud_decimal(estaciones_provincia.iloc[linea,2], lista_longitudes)


        estaciones_provincia['latitud_of'] = latitudes

        estaciones_provincia['longitud_of'] = lista_longitudes

        estaciones_provincia = estaciones_provincia[['Estacion', 'latitud_of', 'longitud_of', 'indicativo']]

        self.estaciones_provincia = estaciones_provincia.rename(columns = {'latitud': 'latitud_of', 'longitud':'longitud_of'})

        return self.estaciones_provincia
        


    #vemos cuales son mis estaciones mas cercanas


    def mi_latlon(self):

        self.addressgmaps = googlemaps.Client(key=self.google_maps)


        if self.coordenadas != None:

            

            coordenadas = self.coordenadas
            
            reverse_geocode_result = self.addressgmaps.reverse_geocode(coordenadas)
             

           # print(reverse_geocode_result[0].keys())


            if 'geometry' in reverse_geocode_result[0].keys(): 

                #print(reverse_geocode_result[0]['geometry'])

                    if 'location' in reverse_geocode_result[0]['geometry']:


                        self.latitude = reverse_geocode_result[0]['geometry']['location']['lat']

                        self.longitude = reverse_geocode_result[0]['geometry']['location']['lng']

        else: 

            gmaps = googlemaps.Client(key=self.google_maps)

            calle = self.adress


            geocode_result = gmaps.geocode(str(calle))

            if 'geometry' in geocode_result[0].keys(): 

                if 'location' in geocode_result[0]['geometry']:


                    self.latitude = geocode_result[0]['geometry']['location']['lat']

                    self.longitude = geocode_result[0]['geometry']['location']['lng']


        



                    #print('Tenemos info geolocalizada :)', '\n')

    # calculo de distancias a la estacion mas cercana

    def distancias(self):
  
  
        nuestro_terreno = [self.latitude, self.longitude]

        distancia_a_campo = []


        for ubicacion in range(self.estaciones_provincia.shape[0]):

            latitud_ubicacion = self.estaciones_provincia.iloc[ubicacion, 1]
            longitud_ubicacion = self.estaciones_provincia.iloc[ubicacion, 2]


            ubicacion_estacion = [latitud_ubicacion, longitud_ubicacion]
        #Creamos una lista que va a albergar los kms

            

            #Hacemos el calculo de las distancias, y lo añadimos al dataset
            distancia_a_campo.append(geodesic(nuestro_terreno, ubicacion_estacion).km)
        

        self.estaciones_provincia['distancia'] = distancia_a_campo
            

        return self.estaciones_provincia


    def ordenar_distancias(self):


        
        #Ordenamos por distancia más cercana

        estaciones_provincia = self.estaciones_provincia.sort_values('distancia')

        #Renombaramos los campos y nos quedamos con las columnas que queremos

        estaciones_provincia = estaciones_provincia.rename(columns={'latitud_of': 'Latitud', 'longitud_of': 'Longitud', 'distancia':'Distancia (KM)'})

        estaciones_provincia['Distancia (KM)'] = estaciones_provincia['Distancia (KM)'].round(2)
        estaciones_provincia[['Estacion','Latitud','Longitud','Distancia (KM)']]

        #nos quedamos con la esatacion mas cercana

        self.estacion = estaciones_provincia.iloc[0,0]


        return self.estacion
       
       
       # return self.estaciones

    
    #vamos a ver cuales son mis estaciones mas cercanas

    def mis_estaciones_mas_cercanas(self):
        
    #def mis_estaciones_mas_cercanas(self, estaciones_provincia, estacion):


        #print(estaciones_provincia)


        codigo_estacion_mas_cercana = self.estaciones_provincia[self.estaciones_provincia['Estacion'] == self.estacion][['indicativo']]

        #codigo_estacion_mas_cercana = estaciones_provincia[estaciones_provincia['Estacion'] == self.estacion][['indicativo']]

       # print(codigo_estacion_mas_cercana)

        self.codigo_estacion_cercano = list(codigo_estacion_mas_cercana['indicativo'])[0]

        #codigo_estacion_cercano = list(codigo_estacion_mas_cercana['indicativo'])[0]


        return self.codigo_estacion_cercano

        #return codigo_estacion_cercano


    #obtenemos los datos de esa estacion: 


    def funciona_o_no(fecha_ini, fecha_fin, codigo, aemet):
      
      url = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos"
                "/fechaini/{}T00:00:00UTC/fechafin/{}T00:00:00UTC/estacion/{}".format(fecha_ini, fecha_fin, codigo))

      API_KEY = aemet
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


    def meterelogia_estacion_mas_cercana(self):
      
        url = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos"
            "/fechaini/{}T00:00:00UTC/fechafin/{}T00:00:00UTC/estacion/{}".format(self.fecha_ini, self.fecha_fin, self.codigo_estacion_cercano))

        API_KEY = self.aemet
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

            print(' El codigo en cuestion ', r.status_code)

            if r.status_code == 200:

               # print(r.json())

                data_url = r.json()['datos']

                print('\n La url que vamos a gestionar es: ', data_url, '\n')

                r_data = requests.get(data_url, params=querystring, verify=False)
                #print(r_data)
                #print('Y los datos son: ', r_data)
                raw_data = r_data.json()
                
                raw_data = parse_data(raw_data)

                #guardamos con los datos en el dataframe

                información_base_cercana = pd.DataFrame(raw_data)

                #print(información_base_cercana.head())


                #return información_base_cercana

        except: 

            print('La extracción de información falla, checkea las credenciales')




        #---------------- EXTRAEMOS LA INFORMACIÓN DE LAS DEMÁS ESTACIONES DE LA PROVINCIA
        # 
        def busqueda_metricas_temperatura_media(nombre_estacion, codigo_estacion_cercano, fecha_ini, fecha_fin, diccionario, aemet_key):
            

        #0. Extraemos la información de una estación filtrando por el nombre de la estacion
        #le añadimos el drop index, porque luego, más adelante reseeteamos el index para que el código funcione
        #bien. Por loq ue, al genera un indice natural de python, el indice antiguo nos pasa como nueva columna y eso
        #no nos intereesa. 

            #estacion_actual = estaciones_albacete[estaciones_albacete['Estacion'] == nombre_estacion].drop('index', axis = 1)

            #codigo_estacion_mas_cercana = estaciones_provincia[estaciones_provincia['Estacion'] == estacion][['indicativo']]
            #1. Nos qudamos con el código identificativo de la estacion de interes
            
            codigo_estacion_actual = codigo_estacion_cercano

            # print(codigo_estacion_actual)

            #2. Utilizamos el codigo de la estación para extraer la infomración metereológica

            url = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos"
                "/fechaini/{}T00:00:00UTC/fechafin/{}T00:00:00UTC/estacion/{}".format(fecha_ini, fecha_fin,\
                                                                                        codigo_estacion_actual))

            #API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'

            querystring = {"api_key": aemet_key}
                
            r = requests.get(url, params=querystring, verify=False)


            if r.status_code == requests.codes.OK:
                
                #3. Nos qudamos con el apartado de 'datos' una vez transformada a json, que es una URL
                #print(r.json())

                data_url = r.json()['datos']

                #4. Hacemos la petición a la API.

                r_data = requests.get(data_url, params=querystring, verify=False)

                #5. Hacemos la transfomración a JSON.

                raw_data = r_data.json()

                #6. Cambiamos los decimales de coma a punto

                raw_data = parse_data(raw_data)
                

                #7. Guardamos el output en un dataframe

                información_base_cercana_temp = pd.DataFrame(raw_data)

                #8.Y nos quedamos con la ifnormación de la fecha y con la temperatura media de dicha estacion

                información_temp_media = información_base_cercana_temp.loc[:,['fecha','tmed']]

                #print('Los datos de esta estacion son: ', información_temp_media['tmed'].values.tolist()[:5])

                #Finalmente, esta ifnormación la transladamos a lita para poder guardarlo junto al código de la estación de interés

                diccionario[nombre_estacion] = información_temp_media['tmed'].values.tolist()

            

        '''
        Dicho esto, creamos un diccionario para guardar la información de la formula que acabamos e crear, 
        y le pasamos la información de las estaciones de la provinica de interés. Pero para ello necesitamos saber cuales son 
        las estaciones de albacete

        '''

        url_estaciones = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"
        querystring = {"api_key":self.aemet}

        headers = {
            'cache-control': "no-cache"
            }

        #Como lo hemos hecho en veces anteriores, nos quedamos ocn el apartado de 'DATOS' que no deja de ser una URL. 

        #print(requests.request("GET", url_estaciones, headers=headers, params=querystring))

        #print(json.loads(requests.request("GET", url_estaciones, headers=headers, params=querystring).text))

        datos_url_plu = json.loads(requests.request("GET", url_estaciones, headers=headers, params=querystring).text)['datos']

        #Hacemos la request, y los resultados los guardamos en un dataframe. 

        todas_estaciones = pd.DataFrame(requests.get(datos_url_plu, params=querystring, verify=False).json())

        #Una vez que hemos logrado las estaciones filtramos por la provincia que nos interesa.

        estaciones_albacete = todas_estaciones[todas_estaciones['provincia'] == 'ALBACETE'][['indicativo', 'latitud', 'nombre', 'longitud']]

        #Una vez que tenemos las estaciones de la provincia accionamos la formula creada para obtener las temepraturas medias.


        #restablecemos el índice para que cuente desde el 0 sino no va a funcionar el script

        estaciones_albacete = estaciones_albacete.rename(columns={'nombre': 'Estacion'}).reset_index()
        #print(estaciones_albacete)


        #print(estaciones_albacete.loc[0,'Estacion'])



        #estacioness = {}
        estaciones = {}

        for estac in range(0,estaciones_albacete.shape[0]):

            #por cada estacion en la tabla de estaciones de esa provincia
            #nos quedamos con el codigo de esa provincia: 

            nombre_estacion = estaciones_albacete.loc[estac,'Estacion']
            #print(nombre_estacion)
            busqueda_metricas_temperatura_media(nombre_estacion = nombre_estacion,\
             codigo_estacion_cercano = self.codigo_estacion_cercano,\
              fecha_ini = self.fecha_ini,\
               fecha_fin = self.fecha_fin ,\
                diccionario = estaciones,\
                aemet_key = self.aemet)

            

        #Transfomramos el output en un dataframe operativo

        temperatura_media_estaciones = pd.DataFrame.from_dict(estaciones, orient='index').T

        #si hay NAs los reemplazamos por 0


        temperatura_media_estaciones = temperatura_media_estaciones.fillna(0)

        #Creamos la columna de la media de las estaciones diarias

        temperatura_media_estaciones['mean_tmed'] = temperatura_media_estaciones.mean(axis=1)


        #Adjuntamos la fecha a la que se referencia cada media diaria

        temperatura_media_estaciones['fecha'] = información_base_cercana['fecha']


        #y nos quedamos solamente con los dos datos, la media diaria y la fecha

        temperatura_media_estaciones = temperatura_media_estaciones[['fecha', 'mean_tmed']]

        #---------------- JUNTAMOS LA INFORMACIÓN DE LAS DEMAS ESTACIONES OCN LA DE LA BASE AEREA

        información_base_cercana['prov_tmed'] = temperatura_media_estaciones['mean_tmed']

        #√emos el resultado del matching

        #print(información_base_cercana.head())

        #---------------- CREAMOS LAS NUEVAS METRICAS DE DATOS 

        '''
        Si la temperatura exterior cae bajo los 7 grados, se sabe que el almendro puede empezar a caer en periodo de hibernación
        Por lo que vamos a tener que investigar si este caso ocurre . 
        '''

        import numpy as np

        #primero nos interesa si ha estado dorido o no ha estado dormido

        información_base_cercana['almendro_sueño'] = información_base_cercana['tmed'] < 7

        #luego nos interesa saber a cuantos grados ha etado dormido si es true

        información_base_cercana['dor_grados'] = 7 - información_base_cercana['tmed']

        #solo queremos reperesentar los valores que ha estado realmente por debajo de 7 grados, por lo que
        #todas aquellas veces que ha estado por encima, lo reemplazamos por 0. 

        información_base_cercana['dor_grados'] = np.where(información_base_cercana['dor_grados'] > 0,\
        información_base_cercana['dor_grados'], 0)


        '''
        En cuanto a la presión se refiere, también nos es de mucha interes porque es un medio que usan las 
        plantas para absorver la humedad de la tierra. 
        La presión interna tiene que ser superior a la externa. Nosotros de esta fuente solo tenemos la presión 
        externa, por lo que vamos a llamalo como tal. 

        '''

        información_base_cercana['Presion_externa'] = (información_base_cercana['presMax'] + información_base_cercana['presMin'])/2

        #--------------- CAMBIAMOS LOS NOMBRES DE LAS COLUMNAS 


        información_base_cercana = información_base_cercana[['fecha', 'nombre', 	'provincia','tmed','prec','tmin','tmax','dir','velmedia','presMax','presMin','prov_tmed','dor_grados', 'Presion_externa']]

        #cambiamos los nombres de las columnas a otros más comprensibles

        información_base_cercana = información_base_cercana.rename(columns={'nombre': 'Estacion', 'provincia': 'Provincia', 'tmed': 'Temperatura_media', 'prec':'Precipitacion_l_m3', 'tmin':'Temperatura_minima','tmax':'Temperatura_maxima','dir':'Direccion_viento','velmedia':'Velocidad_media','velmedia':'Velocidad_media','presMax':'Presion_maxima', 'presMin':'Presion_minima', 'prov_tmed':'Prom_temperatura_media_prov', 'dor_grados':'Grados_debajo_siete'})


        return información_base_cercana
