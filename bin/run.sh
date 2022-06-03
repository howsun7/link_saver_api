#!/usr/bin/env bash

if gunicorn
then
    gunicorn wsgi:app --bind 0.0.0.0:8080 --log-level=debug --workers=4
else 
    export FLASK_ENV=development
    flask run -p 3000
fi
