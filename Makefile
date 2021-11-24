DEV_COMPOSE_FILE := docker/docker-compose.yml

network:
	@docker network create exp

build:
	@echo "Building image..."
	@docker-compose -f $(DEV_COMPOSE_FILE) build

up:
	@echo "Running docker-compose up"
	@docker-compose -f $(DEV_COMPOSE_FILE) up -d

start: up
	@echo "Start app..."
	@docker-compose -f $(DEV_COMPOSE_FILE) start app

run-app:
	@echo "Running app..."
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /app/start_app.sh start

stop:
	@echo "Stopping app..."
	@docker-compose -f $(DEV_COMPOSE_FILE) stop app

# add package
pip-install:
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /app/start_app.sh package $(package)

pip-reinstall:
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /app/start_app.sh reinstall

down:
	@echo "Running docker-compose down"
	@docker-compose -f $(DEV_COMPOSE_FILE) down

migrate:
	@echo Running migrations
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /app/start_app.sh run_migrations $(application) $(migration)

migrations:
	@echo Creating migrations
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /app/start_app.sh make_migrations $(application) $(migration)

django-app:
	@echo adding django app
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /app/start_app.sh django-app $(app)

collectstatic:
	@echo Running collectstatic
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /app/start_app.sh collectstatic

django-shell:
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /app/start_app.sh shell

exp-shell:
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /bin/bash

tests:
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /app/start_app.sh test

jenkins-tests:
	@docker-compose -f $(DEV_COMPOSE_FILE) exec app /app/start_app.sh test
