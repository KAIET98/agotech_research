from metereology.metereology import * 




#ALBACETE:
#coordenadas = (38.968348, -1.884831)

coordenadas = (40.5206, 0.351246)

#TOLEDO : 

#coordenadas = (39.55678333333333, -3.1920416666666664) #https://www.vercalendario.info/es/como/convertir-latitud-longitud-grados-decimales.html#:~:text=Latitud%2038%C2%B054%E2%80%B2%2017%E2%80%B3N%20equivale%20a%2038.90472222222222%C2%B0,77.01638888888888%C2%B0%20(Grados%20decimales).

API_AEMET = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'
API_GOOGLE = 'AIzaSyD7zvwwj8-4JS2XZq0n8bLb9t2cSqStx84'
fecha_ini = '2009-01-01'
fecha_fin = '2009-02-01'


#fecha_ini =  '2021-01-01', fecha_fin = '2022-03-01'

mi_metereologia_clase = mi_metereologia( google_maps_key = API_GOOGLE,\
    coodenadas = coordenadas,\
    api_aemet =  API_AEMET,\
    fecha_ini = fecha_ini,\
    fecha_fin = fecha_fin)


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


estaciones_ordenadas = mi_metereologia_clase.ordenar_distancias()

estacion_mas_cercana_codigo = mi_metereologia_clase.mis_estaciones_mas_cercanas()


#print(estacion_mas_cercana_codigo)

#hacer la llamada a la api de aemet


#mis_datos = mi_metereologia_clase.meterelogia_estacion_mas_cercana()


#print(mis_datos.head())

df = mi_metereologia_clase.meterelogia_estacion_mas_cercana()

df = df.fillna(999)


print(df.head())





