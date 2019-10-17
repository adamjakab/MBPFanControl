#!/bin/bash

_DIR_="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
cd "${_DIR_}" || exit 1
/usr/local/bin/pipenv run "${_DIR_}/app.py"
