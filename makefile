SHELL := /bin/bash

FIXTURES := integrated_users

appsetup:
	dockerbuild setupdb

dockerbuild:
	docker system prune -f
	docker-compose build --no-cache

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

loadfixtures:
	python manage.py loaddata $(FIXTURES)

setupdb:
	migrate loadfixtures