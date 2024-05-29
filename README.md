## Challenge

Para iniciar el proyecto ejecute los siguientes comandos

* `make start-container` para levantar la base de datos y rabbitmq
* Crea tu entorno viartual y activalo <https://www.freecodecamp.org/espanol/news/entornos-virtuales-de-python-explicados-con-ejemplos/>
* `make requirements` para instalar los requerimientos
* `make start-reservation` para levantar el servicio de reservaciones
* En otra tab ejecutar `make start-passenger` para levantar el servicio de pasajeros

Una vez levantado el servicio de rabbitmq se podrá acceder a la interfaz grafica del mismo en la dirección <http://localhost:15672/> usando el usuario de `root` y las password `123`

En la carpeta `postman` vienen las peticiones guardas y estas se pueden exportar a `postman`

## Android app

* Abre la carpeta de `Passenger_app` en la aplicacion de `android studio`
* Sincroniza las dependencias
* Ejecuta el emulador
