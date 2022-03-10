#!/bin/bash

set -e

USER=refugee-management
PROJECT=refugee_management

zipfile="${PROJECT}.zip"

if [ -f ${zipfile} ]
then
    rm ${zipfile}
fi

printf "Zipping the files."
zip -r ${zipfile} . -x \*.zip \*.git\* \*.idea\* \*.DS_Store\* \*.sass-cache\* \*node_modules\* \*__pycache__\* \*.sqlite3 \*.sql \*.asc local_manage.sh config.ini

printf "Transferring the zip folder to the server."
scp ${zipfile}  $1:/home/${USER}

ssh $1 << ENDSSH
set -e
sudo su

rm -rf /home/$USER/$PROJECT

if [ ! -d "/home/$USER/local_settings" ]
then
    printf "Created local_settings directory.\n\n"
    mkdir /home/$USER/local_settings
fi

printf "Unzipping the zipped folder.\n\n"
unzip -o /home/$USER/$zipfile -d /home/$USER/$PROJECT

cd /home/$USER/$PROJECT

printf "Initiating run.sh.\n\n"
./run.sh

printf "DONE"

ENDSSH
