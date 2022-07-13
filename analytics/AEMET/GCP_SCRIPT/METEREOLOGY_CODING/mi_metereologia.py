

from mi_metereologia_modulo import mi_metereologia


#hacemos la prueba de concepto

df = mi_metereologia(8175, '2021-01-01', '2021-03-15',\
     'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo',\
         provincia = 'ALBACETE'
         )

#√emos el resultado

print(" \n El head: \n", df.head())

print('\n ############################## \n El tail: \n')

print(df.tail())