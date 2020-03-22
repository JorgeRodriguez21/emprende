Para correr la aplicación únicamente debes correr este comando:

 docker-compose up --build -d
 
 Eso creará dos contenedores, uno de base de datos y otro de la aplicación.
 
 Al correr: 
 
 docker-compose down
 
 Los contenedores serán eliminados.

Para correr la aplicación localmente (sin docker) se debe correr el script 
(debes cambiar el string de conexion de la base de datos, ya que por defecto se unirá al contenedor)
sh create_database
export FLASK_ENV=development
export FLASK_APP=run.py
run flask
