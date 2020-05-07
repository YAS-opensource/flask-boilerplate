# Flask Boilerplate #

## Description ##

This is a boilerplate made for quick start of flask projects.

## Installation ##

- Install and run dependencies on virtualenv:

  ```bash
  pipenv install
  pipenv run
  ```

- Migrate the database:

  ```bash
  make create_db
  make db_init
  make db_migrate
  ```

- Upgrade the database:

  ```bash
  make db_upgrade
  ```

## Usage ##

- To run the project:

  ```bash
  make run
  ```

  Your server will run at <http://127.0.0.1:5000/>

- If you want to run the project on a different port(for example: 8000):
  
  ```bash
  python manage.py runserver 8000
  ```

- To run tests:

  ```bash
  make test
  ```
