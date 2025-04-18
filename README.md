# ws-blog
~WS flask project to write blogs

## Environment variables
    display all env variables:
    gci env:* | sort-object name

## Lauching the application

- The flask app is in a directory core/
- The flask app is in a python file named application.py
- The instance of the application is app
    
    $ python -m flask --app core.application run --port 3456 --host 0.0.0.0
    
    $ flask --app core.application run --port 3456 --host 0.0.0.0

## Postgres database connection string
    postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>






