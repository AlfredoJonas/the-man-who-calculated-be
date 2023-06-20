SHELL := /bin/bash

FIXTURES := integrated_users

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

loadfixtures:
	python manage.py loaddata $(FIXTURES)
