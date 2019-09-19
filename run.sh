#!/bin/bash
echo Local IP Address detected as:
ip address show scope global eth0 | grep inet
export FLASK_ENV=development
export FLASK_APP=__init__.py
flask run --host=$1
