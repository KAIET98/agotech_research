
'''
Este script reune bien los datos generados en mi_metereologia.py como en 
mi_humedad
'''
import numpy as np
from mi_metereologia_modulo import mi_metereologia
import pandas as pd
from datetime import date
from datetime import timedelta
import os


API_KEY ='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJraWdsZXNpYXNiYXJhaWJhckBzdHVkZW50LmVhZS5lcyIsImp0aSI6ImY4YWQ5OGRmLTkzMjQtNDEzMi05NjY3LTdjY2E2Nzc3Mzc0NiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjQyOTYzODc0LCJ1c2VySWQiOiJmOGFkOThkZi05MzI0LTQxMzItOTY2Ny03Y2NhNjc3NzM3NDYiLCJyb2xlIjoiIn0.en7xw4HHYaZ4oW8qooX6wGG3yn1Tv3OzFfnhrZac6vo'



#hacemos la prueba de concepto

#la diferencia que pilla es de 2 dias, por ejemplo: '2022-03-11', '2022-03-12'

#sacamos el dia de hoy 
today = date.today()

#sacamos la información desde hace 4 dias hasta hace 2 dias
hace_dos = today - timedelta(days = 2)
hace_cuatro  = hace_dos - timedelta(days = 2)


df_meter_general = mi_metereologia(8175, hace_cuatro, hace_dos, API_KEY, provincia = 'ALBACETE')

print(df_meter_general.head())
