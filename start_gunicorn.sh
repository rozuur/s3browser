#!/usr/bin/env bash
# https://pythonspeed.com/articles/gunicorn-in-docker/

# https://stackoverflow.com/questions/59895/get-the-source-directory-of-a-bash-script-from-within-the-script-itself
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

gunicorn -c "${SCRIPT_DIR}/configs/gunicorn_config.py" wsgi:app

