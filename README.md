# test_quick

## MiniAPI

Este es un proyecto programado en django y ORM, hace uso de la base de datos postgres.

Se crea el proyecto django y se instalan las librerias psycopg2, pyjwt, djangorestframework

Se creo el archivo jwt_authentication que permite extraer el valor token jwt, acontinuacion creamos el archivo models.py con los modelos de la base de datos, es decir las tablas que vamos a usar. Luego utilizamos el serializer para convertir los datos de una lista a json o viceversa. En nuestro archivo views.py tenemos las vistas es decir las funciones donde se desarrolla la logica de lo que se va mostrar o recibir en el servidor y por ultimo editamos el archivo urls.py para agregar las rutas de las urls que vamos a usar.


## Requisitos

Python 3.12.0
Django
Django Rest Framework
psycopg2
pyjwt
hashlib
csv



## Instalación

git clone  https://github.com/3p1c0s3nd/test_quick.git
cd test_quick
pip install -r requirements.txt
python manage.py runserver


## Configura la Base de datos
python manage.py makemigration
python manage.py migrate


