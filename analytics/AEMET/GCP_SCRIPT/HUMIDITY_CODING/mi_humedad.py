

'''

El objetivo principal de este script es importar la función construida en "humedad_ciudad" 
de este directorio y lanzar la query desde este archivo

'''

from humedad_ciudad import humedad_ciudad


API_KEY ='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'
# Llamamos a la función
df = humedad_ciudad(API_KEY = API_KEY, codigo_ciud = 2003)


#Y hemos unas filas del dataframe
print(df.head())

#---------------- FUNCIONA :)-------------
