# Flask Boilerplate

[![Actions Status](https://github.com/YAS-opensource/flask-boilerplate/workflows/flask-boilerplate/badge.svg)](https://github.com/YAS-opensource/flask-boilerplate/actions)
[![codecov](https://codecov.io/gh/YAS-opensource/flask-boilerplate/branch/master/graph/badge.svg)](https://codecov.io/gh/YAS-opensource/flask-boilerplate)
[![Maintainability](https://api.codeclimate.com/v1/badges/0461212239959a3242a9/maintainability)](https://codeclimate.com/github/YAS-opensource/flask-boilerplate/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/945173f5a1d24513b0f1e709216c6baf)](https://app.codacy.com/gh/YAS-opensource/flask-boilerplate?utm_source=github.com&utm_medium=referral&utm_content=YAS-opensource/flask-boilerplate&utm_campaign=Badge_Grade_Settings)

A boilerplate made for kick-starting your next flask project, with ready to go authentication(using JWT) module and a base REST api module. Godspeed!

- Out of the box Authentication with JWT
- And extendable base module to create new API endpoints with ease. Supported methods are: GET, POST
- Out of the box Authentication checker decorator that you can add to any endpoint!

## Installing dependencies

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

- Add a `.env` file. One is given here as an `example.env`, you must not use this file as is, always edit the secret key to a new secure key, when you develop your application. Modify other variables as per your necessary configuration for your own project.

## Usage

- To run the project:

  ```bash
  make run
  ```

  Your server will run at <http://127.0.0.1:5000/>

> If you want to run the project on a different port, for example 8000, do this:
>  
>  ```bash
>  python manage.py runserver 8000
>  ```

- To run tests:

  ```bash
  make test
  ```

## Documentations

- Using `Base.py` to create custom views: [see wiki](https://github.com/YAS-opensource/flask-boilerplate/wiki/Base.py-superclass)
- API endpoints: [see wiki](https://github.com/YAS-opensource/flask-boilerplate/wiki/API-endpoints)
