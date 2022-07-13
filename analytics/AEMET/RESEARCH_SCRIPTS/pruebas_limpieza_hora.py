
import pandas as pd 
import re

historico = pd.read_csv('database/historico_humedad_22_03_2022.csv')

print('\n Vemos el resultado de la importacion: \n')

historico = historico.drop('Unnamed: 0', axis = 1)

print(historico.head())

print('Probanos con:  ')

print( historico.iloc[0,3])

patron = '\d*\:\d*\:\d*'



for hora in range(0, historico.shape[0]):

    

    hora_off = re.search(r'\d*\:\d*\:\d*', historico.iloc[hora,3])

    historico.iloc[hora,3] = hora_off.group()

print(historico.head())