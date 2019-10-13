#!/usr/bin/env bash

# https://pythonspeed.com/articles/gunicorn-in-docker/
gunicorn --bind 0.0.0.0:9000 wsgi:app --chdir /s3browser \
    --workers=2 --threads=4 --worker-class=gthread \
    --worker-tmp-dir /dev/shm