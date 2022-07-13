

from METEREOLOGY_CLASS.metereologia_lalon_class import mi_metereologia

# 1. EJEMPLO USANDO COORDENADAS

#1. Cargamos la clase

api_key_bluetab = 'AIzaSyD7zvwwj8-4JS2XZq0n8bLb9t2cSqStx84'

api_aemet = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'



#api_key_kaiet = 'AIzaSyB8b6vSNPb7MzEBXXTNRzdkWqLGIKQotmU'
mi_metereologia_clase = mi_metereologia( google_maps_key = api_key_bluetab,\
    coodenadas = (40.5206, 0.351246), \
        api_aemet = api_aemet, \
         fecha_ini = '2022-01-01', \
         fecha_fin = '2022-05-01')


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

estacion_mas_cercana_codigo = mi_metereologia_clase.mis_estaciones_mas_cercanas(estaciones_provincia,\
     estaciones_ordenadas)


#print(estacion_mas_cercana_codigo)

#hacer la llamada a la api de aemet


#mis_datos = mi_metereologia_clase.meterelogia_estacion_mas_cercana()


#print(mis_datos.head())

df = mi_metereologia_clase.meterelogia_estacion_mas_cercana()

df = df.fillna(999)


print(df.head())

print('#######')

print(df.tail())
#y finalmente crear la funcionalidad de subir los datos si eso

# 2. EJEMPLO USANDO LA DIRECCION -----------------------------


#1. Cargamos la clase


mi_metereologia_clase = mi_metereologia( informacion_adress = "EUSKAL HERRIA 5 IBARRA",\
     google_maps_key = api_key_bluetab,\
         api_aemet = api_aemet)


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

estacion_mas_cercana_codigo = mi_metereologia_clase.mis_estaciones_mas_cercanas(estaciones_provincia, estaciones_ordenadas)


#print(estacion_mas_cercana_codigo)

#hacer la llamada a la api de aemet

df = mi_metereologia_clase.meterelogia_estacion_mas_cercana(fecha_ini =  '1998-01-01', fecha_fin = '1998-02-10')


df = df.fillna(999)

print(df.head())

print('#######')

print(df.tail())

