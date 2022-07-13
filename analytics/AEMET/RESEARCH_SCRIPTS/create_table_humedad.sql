
#Creamos la tabla de la humedad, paraa
#recoger los datos diarios

USE GET_DATABASE;


CREATE TABLE HUMEDAD (
id_humedad  INT  PRIMARY KEY AUTO_INCREMENT, 
Humedad_relativa int, 
DIA DATE NOT NULL, 
HORA TIME
);