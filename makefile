SHELL := /bin/bash

FIXTURES := integrated_users integrated_operations

appsetup: dockerbuild setupdb serveApp

awssetup: dockerbuild migrate loadfixtures serveApp

makemigrations: python manage.py makemigrations

dockerbuild:
	docker system prune -f
	docker-compose build --no-cache

setupdb:
	docker-compose down -v
	docker-compose up -d db
	make migrate loadfixtures

migrate:
	docker-compose run web python manage.py migrate

loadfixtures:
	docker-compose run web python manage.py loaddata $(FIXTURES)

serveApp:
	docker-compose up -d web

