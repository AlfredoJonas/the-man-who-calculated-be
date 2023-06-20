SHELL := /bin/bash

FIXTURES := integrated_users

appsetup: dockerbuild setupdb

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

loadfixtures:
	python manage.py loaddata $(FIXTURES)

dockerbuild:
	docker system prune -f
	docker-compose build --no-cache

setupdb:
	docker-compose down -v
	docker-compose up -d db
	docker-compose run web make migrate loadfixtures