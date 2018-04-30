# BANK OTUCH

[![CircleCI](https://circleci.com/gh/alexkiura/bank_otuch/tree/develop.svg?style=svg)](https://circleci.com/gh/alexkiura/bank_otuch/tree/develop)
[![Coverage Status](https://coveralls.io/repos/github/alexkiura/bank_otuch/badge.svg)](https://coveralls.io/github/alexkiura/bank_otuch)

A banking application

## What is it?

Bank Otuch is an application that allows a user to:
  * Register for an account
  * Create a bank account for managing finances
  * Deposit money to the bank account
  * Withdraw money from the bank account
  * View their transactions


## Project Plan
The project uses pivotal tracker for project management. You can check out the board [here](https://www.pivotaltracker.com/n/projects/2168022).

## Installation

### Instal prerequisites:
* Get Python 3.6 [here](https://www.python.org/downloads/)  
* Get pipenv [here](https://github.com/pypa/pipenv)  
* Get postgres [here](http://postgresguide.com/setup/install.html)  


Clone the repo
```
$ git clone https://github.com/alexkiura/bank_otuch.git
```

Navigate to the root folder
```
$ cd bank_otuch
```
Create a python 3.6 environment
```
$ pipenv --python 3.6
```
Install the necessary packages
```
$ pipenv install --dev
```

### Setup the database:
Create the database:
Ensure postgres is running.
```
$ psql
$ CREATE DATABASE bank_otuch;
```



Perform migrations by running:
* `python manage.py makemigrations`
* `python manage.py migrate`

Start the development server by running `python manage.py runserver`


## Testing
To run the tests for the app:
```
pipenv run coverage run manage.py test
```
pipenv run coverage run manage.py test

To get coverage:
```
coverage report -m
```

## Technologies used
[Django](https://www.djangoproject.com/) |
[Django REST](http://www.django-rest-framework.org/)
