# Flask Boilerplate

A boilerplate made for kick-starting your next flask project, with ready to go authentication(using JWT) module and a base REST api module. Godspeed!

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
