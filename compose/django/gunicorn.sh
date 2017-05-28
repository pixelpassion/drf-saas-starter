#!/bin/sh
python /app/manage.py collectstatic --noinput
daphne -b 0.0.0.0 -p 5000 multichat.asgi:channel_layer