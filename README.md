# iREPORTER
 [![Build Status](https://travis-ci.org/ObedZac/iREPORTER.svg?branch=develop)](https://travis-ci.org/ObedZac/iREPORTER).
 [![Coverage Status](https://coveralls.io/repos/github/ObedZac/iREPORTER/badge.svg?branch=develop)](https://coveralls.io/github/ObedZac/iREPORTER?branch=develop)
 
This is a project aimed at making a web application than can enable anyone whistle blow on corruption. It is a simple website application made as part of [*Andela fellowship bootcamp challenge*](https://andela.com/fellowship/), possibly the best software development challenge in the world. [This is the link to the project code](https://obedzac.github.io/iREPORTER).

## what it does

It provides the API endpoints for [iREPORTER](https://ireporerobed.herokuapp.com/)
> an app that allows users to report on corruption or an intervention from anywhere in Kenya.

## Usage

* As a User, you can:
                    * Create an account
                    * Log in into the account
                    * Create a red flag or intervention post
                    * View all your posts
                    * View a specific post
                    * View the status of a post
                    * Modify a post
                    * delete a post

* As an admin, you can:
                    * Create an account
                    * Log in into the account
                    * View all posts
                    * View a specific post
                    * Change the status of a post


## Prerequisites

* Python 3.6 or later
* Git
* Virtualenv

## Installation

### Download option

* Go to [iReporter](https://github.com/ObedZac/iREPORTER) on github
* Download the zip file and extract it
* Right click on the folder and open with terminal on linux or bash

** Cloning option **

* On your favorite terminal
* cd to where you want the repo to go
* Run the following command:

`git clone https://https://github.com/ObedZac/iREPORTER.git`

* Then:

`cd iREPORTER`

## Virtual environment

> Now create a vitual environment, run:

`virtualenv env`

> or :

`python3 -m venv env`

> or any other that you know of.
> > Create a .env file and configure it with:

```
source env/bin/activate

export FLASK_APP="run.py"

export APP_SETTINGS="development"

```

>To activate virtualenv, run:

`source .env`

> or:

`source env/bin/activate`

**Install Dependencies**
> run:

`pip install -r requirements.txt`

> or:

### Test Endpoints
> To test endpoints follow this [link](https://ireporerobed.herokuapp.com/) to the heroku app

> Then use the endpoints below to test them on post man

## API-Endpoints

For user:

Test | API-endpoint |HTTP-Verb | Inputs
---------------------| ---------------- | ------ | ----------------
Users can create new post | api/v1/redflags | POST | {"redflag_id":1,"title":"title","body":"body"}
users can view all their posts | api/v1/redflags | GET | None
users can view a post | api/v1/redflags/<int:redflag_id> | GET |None
users can modify their post | api/v1/redflags/<int:redflag_id> | PUT |{"title":"title", "body":"body"}
users can delete a post | api/v1/questions/<int:redflag_id> | DELETE |None


*Testing*
> you could test each endpoint on postman
> you could also run
`nosetests`
or
`pytest`

*this readme will be updated periodically*
### Author

*Obed Zakayo*

### Acknowledgement

*Andela Kenya*

*Bootcamp-cohort35-comrades*


### Support or Contact

[Github Pages](https://github.com/ObedZac/iREPORTER)

[Heroku App](https://ireporerobed.herokuapp.com/)


