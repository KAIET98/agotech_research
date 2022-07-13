# TFM_AGROTECH
Este es un repositorio creado por Kaiet Iglesias Baraibar para utilizar algunos scripts de python para el proyecto de TFM. 

# Parametros de entorno 

Dentro de `environment_parameters` tenemos creado un paquete desde el cual especificamos los parametros básicos de entorno como el host de nuestra base de datos, password, user y tal. Es importante ejecutar el paquete e instalarlo en nuestro entorno virtual sino la mayoría de las operaciones no se podran hacer. 

Existe un README que explica como hacerlo. 

# Kanban Dashboard

https://kanban-chi.appspot.com/dashboard/5757438876844032/d-5757438876844032


# General Instructions

The general project structure MUST have:

```
./analyticsfolder: Version of the model or analysis delivered to the customer must be here.
./results folder: all the outputs that different scripts generate will be saved into this folder. Each script will generate the subsections needed of this folder. This folder MUST always be included in the .gitignore file

```

# Base de datos

La base de datos que estamos corriendo es una micro que esta alojada en GCP, andamos con la version gratuita del programa por lo que la licencia expira de tanto en tanto, dicho esto, los valores de nuestro host hay que cambiarlos de tanto en tanto.

```
host =  '34.175.164.167'
user = 'admin'
password = '12345678'
database = 'GET_DATABASE'
```


En el caso que nos quedemos sin instancia o sin base de datos, para poder replicar lo que tenemos en otro proveedor, primero de todo tras crear las instancias necesarias en el nuevo proveedor, la conexión (regla de entrada) debe ser indicada como 0.0.0.0/0 y el usuario y base de datos con la contraseña tenemos que modificar el archivo "REPLICA_BASEDATOS.ipynb".

# Entorno virtual 

La creación de entornos se ha hecho por medio de VirtualEnv. 

Dicho esto para crear un entorno virtual nos colocamos dentro de nuestro ordenador en un lugar comun y creamos un direcotrio donde hostearesmos los entornos virtuales:

```
mkdir test_venv/

```
Una vez que tenemos la carpeta creada, lanzamos este comando para crear un entorno virutal dentro 
de esa carpeta: 

```
python3 -m venv test_venv/prueba_1

```
Una vez creado el entorno virtual "prueba_1" para activarlo: 

```
source prueba1/bin/activate

```
Para desactivarlo: 

```
deactivate

```
Si queremos ver los paquetes que tiene  el entorno, una vez activado el entorno lanzamos el: 

```
pip freeze

```
También podemos guardar los paquetes en un fichero txt


```
pip freeze > requirements.txt
```

# Lógica de negocio gráfica

Los archivos que tienen al lado un "Ahora", o bien se están ejecutando en Google Functions o hay que ejecutarlos cada semana o cada día, lo que uno decida, para alimentar el proyecto. En este enlace se pueden encontrar los archivos que hoy por hoy participan en el apartado de Data Engineering del proyecto: https://www.canva.com/design/DAEdO0ztTx4/Tvc1pLk8mtFoByGR14CIUQ/view?utm_content=DAEdO0ztTx4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton


# Directorio explicado:

# analytics/

Es la carpeta de referencia por defecto. Aquí se aloja todo código que se va a ejecutar bien para:

1. hacer pruebas de concepto, en Google Collaborate, 
2. como construcción de archivos Python auxiliares, .py, 
3. como Módulos de englobación de funcionalidades, carpetas con archiovs "__init__.py", 
4. como archivos SQL, utilizados para conectarnos a nuestras bases de datos como para hacer pruebas en PowerBI. 

Por naturaleza de nuestro proyecto, tenemos que predecir la viabilidad de la plantación del almendro en la finca de GET. Esto requiere hacerse con fuentes de información que engloban la **metereologia**, **sensorica** y datos del **suelo**. 

En cuanto a la **metereologia**, tras habernos peleado con varias fuentes de información, conexiones API, nos decantamos por AEMET, pues tiene una bateria de APIs muy interesantes de cara al público y exponiendo la información que nos interesa. Sobre todo nos hemos focalizado en datos sobre: 

1. Temperatura
2. Humedad
3. Presion
4. Viento

Todos estos datos los ofrece AEMET, sin embargo, la frecuencia en la que las emite es diferente en cada caso. Es decir, la temperatura, presión y viento las emite 1 vez al día como valores medios. Por otro lado, los registros de la Humedad las proyecta cada 6 horas, por lo que hay 4 registros/día. 
El que tengamos esta diferencia de frecuencia de emisión de datos de esta fuente ha hecho que tengamos que subdividir la extracción de datos de esta fuente en dos puntos de enfoque: 

1. Grupo 1: Temperatura, Presion, Viento
2. Grupo 2: Humedad

## AEMET/Google Collab

La mayoria de los códigos que se han extraido en el proyecto de aquí en adelante han nacido desde el jupyter `DATOS_PLUVIOMETRIA_HUMEDAD.ipynb`. En cada uno de sus apartados se desarrollan muchas de las funcionalidades que vamos a ir viendo en este README.md.

## AEMET/Research Scripts

En esta carpeta se encuentran los primeros archivos de desarrollo de código de cómo sacar información sobre **GET**. 

### Humedad

- humedad_albacete.py: se referencia al primer código que pudimos desarrollar para obtener datos suficientes sobre una localidad dada en cuanto a la humedad se refiere. 

- humedad_ciudad.py: es aquí, donde se hace el primer intento de "pre-industrializar" el conocimiento obtenido en el script de "humedad_albacete.py". 

- aplicación_insert_into_humedad.py: finalmente, en este script damos otro paso más que es aunar el conocimiento de "humedad_ciudad.py", extrayendo la información de la humedad referenciable a una ubicación, y si así lo deseamos, insertar los datos en una base de datos. 
Hay que indicar que este archivo se alimenta de una función para insertar datos en una base de datos que se aloja en el script "funcionabilidad_insert_into.py". 

Sin embargo, hacemos referencia que no le damos mucho valor "funcional" a esta carpeta, sino que teórica. Pues, la verdadera aplicación práctica de este conocimiento lo tenemos plasmado, en el siguiente apartado: `AEMET GCP_SCRIPT/ `.

### Metereologia

- mi_metereologia.py: al igual que hemos hecho con la humedad, hemos querido parametrizar el conocimiento sobre la extracción de datos sobre la metereología mediante una función. 

Tampoco es un archivo 100% funcional, pues, vamos a ver su aplicación más práctica más adelante, pero como contenido teórico está bien. 



## AEMET GCP_SCRIPT/ 

Como acabamos de indicar nuestro foco va a estar en los dos grupos anteriores. 

### Humedad GET.


#### Humedad - OLD-VERSION


Cuando hablamos de extraer datos de la API de AEMET, hablamos de Extraer y a la vez tambien de Insertar, en una base de datos, la nuestra, es decir, Load.


**extracción**

En cuestiones de Extracción de datos, podemos tener en cuenta 3 puntos de vista: 

1. El de la lógica operacional: es decir, el archivo que se encuentra en la raíz de AEMET, **ETL_humedad_manual.py**. Es el archivo clave de la operación **manual**. 
Se nutre del módulo de la carpeta `AEMET/HUMEDAD`, donde se le indica cómo extraer los datos de la **Humedad de GET**; e insertarlos en la base de datos.
Eso, sería como se debería de hacer, manualmente.

2. El de la lógica de desarrollo: dentro de `AEMET/GCP_SCRIPTS/HUMIDITY_CODIGN`, tenemos 3 archivos: 

- humedad_ciudad.py: es el archivo **paralelo** al que acabamos de comentar en  `AEMET/HUMEDAD`, es un archivo de soporte, tiene el código. 

- mi_humedad.py: es un script que trae el código hosteado en "humedad_ciudad.py", y lo pone a prueba. 

- clase_extracción_humedad.py: tambiñen intenta hacer lo mismo que mi_humedad.py, pero es el ejemplo de qué pasa si no se dan las órdenes adecuadas a la función de soporte.


#### Humedad - New Version

3. la lógica industrial, la importante: hoy por hoy, la ETL de la humedad de **GET** se hace por medio de Google Functions. Este código se aloja dentro de `AEMET/GOOGLE_FUNCTIONS/FUNCION_HUMEDAD/GET_HUMIDITY_googlefunct.py`. Sus respectivas indicacioens se encuentran en `AEMET/GOOGLE_FUNCTIONS/FUNCION_HUMEDAD/indicaciones.md`.


### Control

Hay que tener en cuenta que llevamos el control de las cargas de los archivos mencionados que se han puesto en producción, bien manualmente como automáticamente, mediante Google Functions, por medio de `AEMET/CONTROLLING/CONTROL_matplot_cargas_humedad_get`.

## AEMET METEREOLOGY_CODING/ METEREOLOGIA

En este directorio tenemos la mayoria del conocimiento sobre la API de AEMET que hemos puesto en funcionamiento sobre el proyecto: 

- estacion_data: es un código en formato pre-industrializable que solamente imprime por pantalla la inforamción metereologica (Sin humedad) de la provincia de **Albacete**.

- mi_metereologia_modulo: consiste en un código, que puede ser industrializado. Pues es una función, pero devuelve la información metereologica de una estación dada, habiendole proporcionado una fecha de inicio, una fecha final, la API KEY de AEMET, y  la Provincia deseada. 

- metereologia_finca.py: es un primer archivo que pone en funcionamiento el script de **mi_metereologia_modulo** de una manera semi-industrializada. 

## AEMET GET_LOAD/ METEREOLOGIA (HISTORICA Y DIARIA)

Focalizando nuestra mente en **el grupo 1**, y en **la empresa GET**, tenemos 2 archivos: 

1. METEREOLOGIA_HISTORICO: que es un jupyter, que se *aconseja ejecutarlo en Google Collab*, pues **extrae** de golpe todo el historial metereologico de la estación más cercana al punto que le indiquemos, y lo **carga** en nuestra base de datos.

2. METEREOLOGIA_HISTOR_DIF: una vez que hayamos ejecutado el archivo anterior, y *tengamos un historico* sobre nuestra ubicación en terminos de Metereologia. Podemos ejecutar cuando queramos este script, pues analizara cual es el último día que tenemos en la base de datos, y **la diferencia hasta el día de hoy**, la extraera y *la cargara en la base de datos*. 


## AEMET TBA_HISTORIC_LOAD/ 

### METEREOLOGIA (HISTORICA Y DIARIA)

En cuanto a la necesidad de extraer datos de TRAINING con **la empresa TBA**, el funcionamiento que hemos querido seguir es el mismo que con **GET**, dentro de **TBA_HISTORIC_LOAD/TBA_AEMET_DATA/**:

- TBA_AEMET_HISTORI_ETL: se lanza un código que de la misma manera que con GET, se extraer toda la información metereologica sobre el punto donde se ubique el campo de la empresa TBA, y a continuación, se **carga** en su respectiva tabla en nuestra BBDD.

- TBA_AEMET_HIST_DIF_ETL: en este caso, como se hacia en *METEREOLOGIA_HISTOR_DIF*, es un archivo que se puede ejecutar cuando queramos una vez que hayamos ejecutado el *TBA_AEMET_HISTORI_ETL*; pues **la diferencia hasta el día de hoy** desde el último día que tiene registrado, la extrae con la API de AEMET, y *la carga en la base de datos*. 


### HUMEDAD HISTORICO: 

En este caso, dentro de **TBA_HISTORIC_LOAD/TBA_SENSOR_HISTORIC_DATA/** nos hacemos partners de los datos de TBA, pues, en sus BBDD, sí quere recogen datos sobre la **humedad relativa**. Entonces, nos montamos un jupyter donde nos conectamos a su base de datos y extraemos todos los registros que tienen, y los insertamos en nuestra base de datos en formato de **humedad historico**.

Luego, si queremos extraer datos sobre la humedad, pero en formato diario, es decir, como subir datos **cada día** como si lo hicieramos con Google Functions, nos vamos a otra carpeta; **analytics/TBA_SCRIPTS**. 

## TBA_SCRIPTS

En esta carpeta se ubican los scripts más propios dirigidos a **la empresa de TBA**, y dar una solución más aislada a ellos. Bien la propia carpeta cuenta con un README.md. 

Sin embargo, de la misma manera que en **AEMET/GET_LOAD/METEREOLOGIA_HISTOR_DIF** o en ***TBA_HISTORIC_LOAD/TBA_AEMET_DATA/TBA_AEMET_HIST_DIF_ETL**, nos conectabamos a la base de datos a la tabla correspondiente y calculabamos la diferencia en días y extraiamos la información correspondiente y la insertabamos. Aquí hacemos lo mismo pero con los registros sobre **la sensorica**, es decir, **más relacionados con los  datos de la humedada de TBA**. Dicho de otra manera, este archivo es el análogo al `AEMET/GOOGLE_FUNCTIONS/FUNCION_HUMEDAD/GET_HUMIDITY_googlefunct.py` de **GET**, pero hay que ejecutarlo a mano, se trata de **TBA_DINAMIZADO.py**. 


### TBA METEREOLOGIA DINAMICA (TBA_SCRIPTS/METEREOLOGIA - CLASE METEREOLOGIA)

Se ha construido un script para poder formalizar la extraccion de datos sobre la metereologia de TBA, o un lugar en concreto, funciona al parecido al `TBA_HISTORIC_LOAD/TBA_AEMET_DATA/TBA_AEMET_HISTORI_ETL`. Pero de forma formalizada. 


## Visualización 

Se ha eleido como herramienta de visualización PowerBI por lo que hemos conectado PowerBI a la MySQL para poder analizar los datos. 

Dicho esto, hemos construido una carpeta para albergar archios para meter en el editor de PowerBI. 

Por ejemplo en cuanto a la humedad, existe una carpeta dedicada a ella, para que podamos extraer datos sobre ella. La query se encuentra dentro de la carpeta.
