#!/bin/bash

#Enable virtual environment
. ./venv/bin/activate

# Run the flask python script which runs the app server
python webapp/flaskr.py

# Disable virtual env
deactivate
