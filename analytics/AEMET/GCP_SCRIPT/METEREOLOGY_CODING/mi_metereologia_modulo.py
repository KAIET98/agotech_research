

'''
Este script tiene como objetvio automatizar la captación de todos los datos metereologicos
de una estación cualquiera de españa que se le proporcione
'''






#------------- EXTRACCION DATOS DESDE LA API DE AEMET -------------


'''
Establecemos la url de acceso a los datos junto a la key de KAIET
'''

'''
Vamos a crear una funcion para chequear si AEMET tiene historico de datos sobre la provincia que quiere 
checkear el usuario

'''






def mi_metereologia(codigo_estacion, desde, hasta, API_KEY, provincia):

    import pandas as pd
    import requests
    import json
    import numpy as np
    '''
    Esto nos devolvera  un booleano, es decir, si es que es true, lanzaremos las operaciones ordinarias tal y como hemos hecho hasta la fecha, 
    si no, le indicaremos con un mensaje que tenemos información sobre la estación que esta buscando.
    '''
    def info_mi_provincia(API_KEY):

        #'Extraemos cuales son las estaciuones que tiene miradas aemet.'

        url_estaciones = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"
        querystring = {"api_key":API_KEY}

        headers = {
            'cache-control': "no-cache"
            }

        #Como lo hemos hecho en veces anteriores, nos quedamos ocn el apartado de 'DATOS' que no deja de ser una URL. 

        datos_url_plu = json.loads(requests.request("GET", url_estaciones, headers=headers, params=querystring).text)['datos']

        #Hacemos la request, y los resultados los guardamos en un dataframe. 

        todas_estaciones = pd.DataFrame(requests.get(datos_url_plu, params=querystring, verify=False).json())


        return todas_estaciones['provincia'].unique()


    if provincia in list(info_mi_provincia(API_KEY)):

        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        import pandas as pd
        import requests
        import json
        import numpy as np

        mi_provincia = provincia.upper()


        #1. Parametrizamos la estación, la API KEY como lafechas desde y hasta


        codigo_estacion_cercano = codigo_estacion
        
        #codigo_estacion_cercano = 8175

        #desde_Fecha = '2021-01-01'

        desde_Fecha = desde

        #hasta_fecha = '2021-02-10'
        
        hasta_fecha = hasta

        #API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'
        API_KEY =  API_KEY 


        url = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos"
            "/fechaini/{}T00:00:00UTC/fechafin/{}T00:00:00UTC/estacion/{}".format(desde_Fecha,\
                hasta_fecha,\
                    codigo_estacion_cercano))

        
        querystring = {"api_key": API_KEY}
            
        r = requests.get(url, params=querystring, verify=False)

        #Creamos una función que transformarra los datos numericos reemplazando la coma por el punto

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


        #Finalmente lanamos la query y si es que todo  va bien extraemos la información

        try: 

            if r.status_code == requests.codes.OK:
                #print(r.json())

                data_url = r.json()['datos']
            

                #print('\n La url que vamos a gestionar es: ', data_url, '\n')

                r_data = requests.get(data_url, params=querystring, verify=False)

                #print('Y los datos son: ', r_data)

                #Una vez que sabemos que podemos extraer los dtos, los transformamos a un formato json.

                raw_data = r_data.json()
        
                #aplicamos la funcion recientemente creada par la transformacion decimal

                raw_data = parse_data(raw_data)

                #guardamos con los datos en el dataframe

                información_base_cercana = pd.DataFrame(raw_data)


                
                
                print('Se ha extraido la información de AEMET')

        except: 

            print('La extracción de información falla, checkea las credenciales')



        #---------------- EXTRAEMOS LA INFORMACIÓN DE LAS DEMÁS ESTACIONES DE LA PROVINCIA
        # 
        def busqueda_metricas_temperatura_media(nombre_estacion, diccionario):
        
        #0. Extraemos la información de una estación filtrando por el nombre de la estacion
        #le añadimos el drop index, porque luego, más adelante reseeteamos el index para que el código funcione
        #bien. Por loq ue, al genera un indice natural de python, el indice antiguo nos pasa como nueva columna y eso
        #no nos intereesa. 

            estacion_actual = estaciones_provincia[estaciones_provincia['Estacion'] == nombre_estacion].drop('index', axis = 1)

            #1. Nos qudamos con el código identificativo de la estacion de interes
            
            codigo_estacion_actual = estacion_actual.iloc[0,0]

            print('El codigo es: ', codigo_estacion_actual)
        # print(codigo_estacion_actual)

            #2. Utilizamos el codigo de la estación para extraer la infomración metereológica


            '''
            
            El que funcionaba hasta ahora: 

            url = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos"
                "/fechaini/{}T00:00:00UTC/fechafin/{}T00:00:00UTC/estacion/{}".format('2021-01-01', '2022-02-10',\
                                                                                        codigo_estacion_actual))

            '''

            url = ("https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos"
                "/fechaini/{}T00:00:00UTC/fechafin/{}T00:00:00UTC/estacion/{}".format(desde_Fecha, hasta_fecha,\
                                                                                        codigo_estacion_actual))

            API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'

            querystring = {"api_key": API_KEY}
                
            r = requests.get(url, params=querystring, verify=False)

            
            #Vemos si se hace la llamada correctamente

            if r.status_code == 200:
                
                #3. Nos qudamos con el apartado de 'datos' una vez transformada a json, que es una URL
                #print(r.json())

                print(r.json())

                #una vez que se hace la llamada, vamos a ver cúal es su contenido, 
                #si realmetne nos devuelve contenido por ejemplo.

                if r.json()['estado'] == 200:

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

                else: 

                    print('No hay información sobre esta estacion')
            #información_temp_media =

             

        '''
        Dicho esto, creamos un diccionario para guardar la información de la formula que acabamos e crear, 
        y le pasamos la información de las estaciones de la provinica de interés. Pero para ello necesitamos saber cuales son 
        las estaciones de albacete

        '''

        url_estaciones = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"
        querystring = {"api_key":API_KEY}

        headers = {
            'cache-control': "no-cache"
            }

        #Como lo hemos hecho en veces anteriores, nos quedamos ocn el apartado de 'DATOS' que no deja de ser una URL. 

        datos_url_plu = json.loads(requests.request("GET", url_estaciones, headers=headers, params=querystring).text)['datos']

        #Hacemos la request, y los resultados los guardamos en un dataframe. 

        todas_estaciones = pd.DataFrame(requests.get(datos_url_plu, params=querystring, verify=False).json())


        #print(todas_estaciones)

        #print(todas_estaciones[todas_estaciones['provincia'] == mi_provincia])


        #Una vez que hemos logrado las estaciones filtramos por la provincia que nos interesa.

        estaciones_provincia = todas_estaciones[todas_estaciones['provincia'] == mi_provincia][['indicativo', 'latitud', 'nombre', 'longitud']]


        #estaciones_albacete = todas_estaciones[todas_estaciones['provincia'] == 'ALBACETE'][['indicativo', 'latitud', 'nombre', 'longitud']]

        #Una vez que tenemos las estaciones de la provincia accionamos la formula creada para obtener las temepraturas medias.


        #restablecemos el índice para que cuente desde el 0 sino no va a funcionar el script

        estaciones_provincia = estaciones_provincia.rename(columns={'nombre': 'Estacion'}).reset_index()
        #print(estaciones_albacete)

        #print(estaciones_albacete)

        #print(estaciones_albacete.loc[0,'Estacion'])



        estaciones = {}

        for estac in range(0,estaciones_provincia.shape[0]):

            #por cada estacion en la tabla de estaciones de esa provincia
            #nos quedamos con el codigo de esa provincia: 

            nombre_estacion = estaciones_provincia.loc[estac,'Estacion']
            #print(nombre_estacion)
            busqueda_metricas_temperatura_media(nombre_estacion, estaciones)


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

    

    else:

        print('AEMET no tiene información acerca de la estación que estás intentando buscar')

    


    
    



