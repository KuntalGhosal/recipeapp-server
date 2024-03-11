#Install PostgresSQL sudo apt update sudo apt install postgresql postgresql-contrib

#Login to PSQL sudo -i -u postgres psql

#Check listed users \du

#Create User CREATE USER postgres WITH PASSWORD 'Welcome@123';

#Grant Permission on table GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres; GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres; GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to postgres; alter user postgres with superuser;

#Create Database CREATE DATABASE recipe_db;

#exit and logout \q logout

#Install python if not installed already sudo add-apt-repository ppa:deadsnakes/ppa sudo apt install python3.8

#Install virtualenv if not installed already sudo apt install python3-pip or sudo apt-get install python3-setuptools sudo python3 -m easy_install install pip python3 -m pip --version

#Install and Create virtualenv sudo apt install virtualenv virtualenv -p python3.8 venv

#use the virtualenv source venv/bin/activate

#Install Dependencies sudo apt install python3.8-dev libpq-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev

#install requirement.txt pip install -r requirements.txt

#Apply Migrations python manage.py makemigrations python manage.py migrate

# Active celery main thread==> celery -A config.settings.celery worker -l info

# start celery beat ==> celery -A config.settings beat -l INFO

# build docker image ==> sudo docker build -t myimage .

# run docker ===> sudo docker run -d -p 8000:8000 myimage

# run test case ===> python manage.py test users

