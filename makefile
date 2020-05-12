install:
	sudo pip -r install --sequential -U requirements.txt

run:
	python manage.py runserver

test:
	python manage.py test

db_create:
	python manage.py db_create

db_init:
	python manage.py db init

db_migrate:
	python manage.py db migrate

db_upgrade:
	python manage.py db upgrade

clean:
	find . -name \*.pyc -type f -delete
	find . -name __pycache__  -type d -delete
	rm -rf .pytest_cache/
