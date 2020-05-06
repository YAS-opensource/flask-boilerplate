# Flask JWT Auth

### Basics

1. Activate a virtualenv
2. Install the requirements

### Set Environment Variables without .env file

Update *project/server/config.py*, and then run:

```sh
export APP_SETTINGS="project.server.config.DevelopmentConfig"
```

or

```sh
export APP_SETTINGS="project.server.config.ProductionConfig"
```

Set a SECRET_KEY:

```sh
export SECRET_KEY="change_me"
```

### Create DB

Create the databases in `psql`:

```sh
$ psql
# create database flask_jwt_auth
# create database flask_jwt_auth_test
# \q
```

Create the tables and run the migrations:

```sh
python manage.py create_db
python manage.py db init
python manage.py db migrate
```

### Run the Application

```sh
python manage.py runserver
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

> Want to specify a different port?

> ```sh
> $ python manage.py runserver -h 0.0.0.0 -p 8080
> ```

### Testing

Without coverage:

```sh
python manage.py test
```

With coverage:

```sh
python manage.py cov
```

### Examples

#### Register

```sh
curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"email":"sihantawsik@gmail.com","password":"abcdef"}' \
    http://localhost:5000/auth/register
```

#### Login

```sh
curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"email":"sihantawsik@gmail.com","password":"abcdef"}' \
    http://localhost:5000/auth/login
```

#### Check status

```sh
curl --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY1Mzk5NjksImlhdCI6MTU4NjUzOTM2OSwic3ViIjoxfQ.wE8_sQvhgcIBjxpsyUi6KZWAJhajqWvsdEeWbtYnuq8" --header "Content-Type: text/plain" --request GET http://localhost:5000/auth/status
```
