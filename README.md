# ws-blog
~WS flask project to write blogs

## Environment variables
    display all env variables:
    gci env:* | sort-object name

## Lauching the application

- The flask app is in a directory core/
- The flask app is in a python file named application.py
- The instance of the application is app
    
    $ python -m flask --app application run --port 3456 --host 0.0.0.0
    
    $ flask --app core.application run --port 3456 --host 0.0.0.0

## Postgres database connection string
    postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>

## Define the environnment variables of the system:
    $env:APP_SETTINGS_MODULE = 'config.local'

## commands database migrations with flask-migrate:
    flask --app application db init
    flask --app application db migrate -m "my message here"
    flask --app application db upgrade 




