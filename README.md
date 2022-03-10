Refugee management
=================

A tool to manage refugee related services

Requirements
------------

* Python3 (>=3.8)
* PostgreSQL (>= 12)

## Set up for local development
* Install npm, ruby and sass and python (>= 3.8)

* Install the dependencies for frontend development
````
npm install grunt-cli -g  # (or using sudo if required)
npm install --save-dev
````

* Clone the git repository and go to the project directory.
* Create a python virtual environment
````
python3 -m venv .venv
````
* Activate the python virtual environment
````
source .venv/bin/activate
````
* Install the python dependencies
````
pip install -r requirements.txt
````

## Configuration

* Create a new file called local_manage.sh by copying the contents from manage.sh.
* Make the file executable.
* Enter the credentials for database and other stuffs in this file only.

## Usage

* For running the server locally
````
./local_manage.sh runserver
````
* To compile the static files (sass, pug, js)
````
grunt assets
grunt watch:assets  # To run watcher
````
* For production
    * Set the PRODUCTION variable in manage.sh to True
    * Execute the deploy.sh script
````
./deploy.sh <user>@<server>
````
