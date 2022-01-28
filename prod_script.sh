function start_app {
    cd /app/api/
    info "Starting app"
    gunicorn --bind :8000 --workers 3 --reload app.wsgi --log-level debug --access-logfile -
}

function make_migrations {
    info "Creating migrations"
    cd /app/api/
    python manage.py makemigrations
}

function run_migrations {
    info "Running migrations"
    cd /app/api/
    python manage.py migrate
}

make_migrations
run_migrations
start_app