#!/bin/bash

set -euox pipefail
IFS=$'\n\t'

declare -r SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
declare -r APP=s3browse

function static_analyse {
    black "${SCRIPT_DIR}/app" "${SCRIPT_DIR}"/*.py
}

function venv_activate {
    set +x
    source "${SCRIPT_DIR}/.${APP}_venv/"bin/activate
    echo "Using $(which python)"
    echo "Using $(which pip)"
    set -x
}

function build {
    make -s -f "${SCRIPT_DIR}"/setup_osx_venv.mk
    venv_activate
    pip install -q \
        -r "${SCRIPT_DIR}"/requirements/requirements.txt \
        -r "${SCRIPT_DIR}"/requirements/dev-requirements.txt
}

function run {
    local port="$1"
    trap static_analyse EXIT
    FLASK_ENV=development FLASK_APP=wsgi.py flask run --host=0.0.0.0 --port="${port}"
}

function main {
    local port=${1?Port is required}
    unset PYTHONPATH
    export PYTHONPATH="."
    build
    run "${port}"
}

main "$@"

