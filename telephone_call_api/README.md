# Telephone Calls API

This HTTP REST API receives call detail records and calculates monthly bills for a given telephone number.

The API avoids consistency errors when receiving call records, eliminating the concerns of telecommunication platforms that consume the service.

This service expects Start/End call record pairs inputs. Then, counts bills based of pre-existent charge prices. On the final month period, a Bill is avaliable for query with all call records information of subscribers by monthly period.

## Instalation

### Deploying on Heroku:


#### Requirements
- Heroku CLI: 

    https://devcenter.heroku.com/articles/heroku-cli    


#### Instructions

1. Clone the project locally:

```sh
$ git clone git@github.com:douglasmoraisdev/work-at-olist.git
```


2. Upload the code for the Heroku App (e.g: telephone-call-api):

```sh
$ cd work-at-olist/
$ git subtree push --prefix telephone_call_api/ heroku master
```

3. Run database migrations:

```sh
$ heroku run python manage.py migrate
```

*Done.*


## Test instructions


1. cd project root path:

```sh
$ cd work-at-olist/telephone_call_api/
```

2. run tests

```sh
$ python manage.py test
```
or
```sh
$ python3 manage.py test
```
Depending of your python installation.

## API Documentation

- After the installation, all API documentation, with the Endpoints descriptions can be accessed on the url:

    http://telephone-call-api.herokuapp.com/docs/

## Dev Work environment
Computer/operating system, text editor/IDE, libraries, etc).

- Hardware: Lenovo Notebook, Intel i7 processor, 16GB Ram, NVIDIA 2GB
- SO: Linux Ubuntu 18.04 LTS
- Text Editor: VSCode 1.26
- Python version: 3.6
- Main libraries: django, djangorestframework, django-heroku (complete list on Pipfile)
- Virtual environment using *pipenv* (https://github.com/pypa/pipenv)

### Extras: 

- Deploy to a diferent Heroku App:

```sh
$ cd work-at-olist/
$ git remote remove heroku
$ heroku git:remote -a <your-heroku-app-name>
$ git subtree push --prefix telephone_call_api/ heroku master
```
