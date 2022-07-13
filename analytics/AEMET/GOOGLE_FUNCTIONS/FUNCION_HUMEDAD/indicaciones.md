

Este readme tiene indicaciones de la logica de construcción de las funciones. 

En si en si como se ha querido construir una teoria acerca de esto de como hacer la cosas por medio de los tutoriales encontrados en internet, se ha creado un docx en drive en el siguiente enlace donde se explica mejor como se ha implementado las funciones: 

https://docs.google.com/document/d/1ATBy6fDxBGrs16UCxKxf8-XFo6SflVhSDi1-J50-t8I/edit?usp=sharing


# GET_HUMIDITY_googlefunct.py

Al final el que hemos usado para poner en GCP ha sido el 'GET_HUMIDITY_googlefunct.py', donde la parte de la conexción a sql al final la hemos fomralizado tal y 
como la haciamos en funcionalidad_insert_into en SQL/. Y ha funcionado perfectamente. 

Como el registro de la humedad se hace una vez al día, en este caso a las 22.00 de la noche, 
realiza la call a la API y la mete en la MySQL.  El desencadenador es por medio de 
'0 22 * * *'; tal y como indica ander jauregui en su tutorial y lo hemos puesto en el drive.


