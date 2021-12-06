#! /bin/bash

# set colors for text
BOLD='\e[1m'
BLUE='\e[34m'
RED='\e[31m'
YELLOW='\e[33m'
GREEN='\e[92m'
NC='\e[0m'

# set colors for the logs
info() {
    printf "\n${BOLD}${BLUE}====> $(echo $@ ) ${NC}\n"
}

warning () {
    printf "\n${BOLD}${YELLOW}====> $(echo $@ )  ${NC}\n"
}

error() {
    printf "\n${BOLD}${RED}====> $(echo $@ )  ${NC}\n"
    bash -c "exit 1"
}

success () {
    printf "\n${BOLD}${GREEN}====> $(echo $@ ) ${NC}\n"
}

# TODO
# export $(cat .env | xargs)

# start the application
function start_app {
    cd /app/api/
    info "Starting app"
    gunicorn --bind :8000 --workers 3 --reload app.wsgi --log-level debug --access-logfile -
}

# install new package
function install_package {
    info "Installing $1"
    cd /app/
    pip install $1
    pip freeze > /app/requirements.txt
}

function reinstall {
    info "Installing requirements..."
    pip install -r /app/requirements.txt
}

function make_migrations {
    info "Creating migrations"
    cd /app/api/
    python manage.py makemigrations $1 $2
}

function run_migrations {
    info "Running migrations"
    cd /app/api/
    python manage.py migrate $1 $2
}

function django-app {
    info "Creating $1 app"
    cd /app/api/
    python manage.py startapp $1
}

function collectstatic {
    info "Running collect static"
    cd /app/api/
    python manage.py collectstatic --noinput
}

function deletestatic {
    info "Deleting static files"
    cd /app/api
    python manage.py collectstatic --noinput --clear --no-post-process
}

function django-shell {
    info "Creating django shell"
    cd /app/api/
    python manage.py shell -i ipython
}

function wait_for_database {
    until $(nc -vz database 5432); do
        info "Waiting for database"
        sleep 5
    done; echo "Database is ready..."
}

function run-tests {
    info "Running tests"
    cd /app/api
    wait_for_database
    python manage.py test
}

# run on demand functions
if [[ $1 == "start" ]];
then
    start_app
elif [[ $1 == "package" ]];
then
    install_package $2
elif [[ $1 == "make_migrations" ]];
then
    make_migrations $2 $3
elif [[ $1 == "run_migrations" ]];
then
    run_migrations $2 $3
elif [[ $1 == "django-app" ]];
then   
    django-app $2
elif [[ $1 == "reinstall" ]];
then
    reinstall
elif [[ $1 == 'collectstatic' ]];
then
    collectstatic
elif [[ $1 == 'shell' ]];
then
    django-shell
elif [[ $1 == 'test' ]];
then
    run-tests
else
    error "Unknow parameter \`$1\`"
fi
