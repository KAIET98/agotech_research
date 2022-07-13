

from humedad.humedad import * 


coordenadas = (38.976422, -1.888443)

#-zumarraga

#coordenadas = (43.090594, -2.320489)

#- tolosa

#coordenadas = (43.126969, -2.069878)

#- donosti

#coordenadas = (43.309835, -1.984475)
API_AEMET = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'
API_GOOGLE = 'AIzaSyD7zvwwj8-4JS2XZq0n8bLb9t2cSqStx84'

#direccion = "Calle de los mancebos"

humedad_mod = humedad( google_maps_key = API_GOOGLE,\
        #informacion_adress = direccion,\
        coodenadas = coordenadas,  
        api_aemet = API_AEMET
         )


codigo_ciudad = humedad_mod.address()


#codigo_ciudad = 2003
print(codigo_ciudad)


humedad_lugar = humedad_mod.humedad_ciudad()

print(humedad_lugar)