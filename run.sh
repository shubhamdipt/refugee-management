#!/bin/bash

USER=refugee-management
PROJECT=refugee_management


printf "Killing old processes for python3 and uwsgi.\n\n"
pkill -9 "uwsgi"
pkill -9 "python"

printf "Copying local settings file.\n\n"
cp /home/${USER}/local_settings/manage.sh /home/${USER}/${PROJECT}/manage.sh
cd /home/${USER}/${PROJECT}

printf "Activating virtual environment for Python3.\n\n"
source /home/${USER}/.venv/bin/activate

printf "Installing the python3 requirements.\n\n"
pip install -r requirements.txt

printf "Running migrations.\n\n"
./manage.sh migrate

printf "Initiating server.\n\n"
./manage.sh runserver

printf "DONE"
