![Python3](https://img.shields.io/badge/python-3.x-blue.svg)
![Vue3](https://img.shields.io/badge/vue-3.x-brightgreen.svg)
![Vuetify3](https://img.shields.io/badge/vuetify-3.x-blueviolet.svg)
![Node.js](https://img.shields.io/badge/node.js-18.x-green.svg)
![Django4](https://img.shields.io/badge/django-4.x-darkgreen.svg)
![DRF](https://img.shields.io/badge/django--rest--framework-3.x-red.svg)


# Wordle App

Competitive Wordle app!

Check out the live demo of the app [here](https://wordle-app2.onrender.com)!
> If the app takes a long time to load, it is running on a free-tier server which hibernates it.  This can result in load times of up to 2 minutes.  Sorry, im too poor to pay for a better service :/

## Table of contents
- [Wordle App](#wordle-app)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
    - [Build](#build)
    - [Run](#run)
  - [Fake Data Population (Testing)](#fake-data-population-testing)
    - [Creates 100 fake users](#creates-100-fake-users)
    - [Creates 1000 Fake wordles and assigns them to random users](#creates-1000-fake-wordles-and-assigns-them-to-random-users)
  - [Local Development](#local-development)
    - [Frontend](#frontend)
    - [Backend](#backend)
  - [Environment Variables](#environment-variables)
  - [Contribute](#contribute)
  - [License](#license)


Competitive wordle app!

## Setup

### Build
```
pip install -r backend/requirements.txt && cd frontend && npm install . && npm run build && cd ../backend && python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate
```

### Run
```
cd backend && gunicorn backend.wsgi:application
```


## Fake Data Population (Testing)

### Creates 100 fake users
```
python manage.py demo_users --num_users 100
```

### Creates 1000 Fake wordles and assigns them to random users
```
python manage.py demo_wordles --count 1000
```

## Local Development

The easiest way to set up and do local development on the app is to run the frontend in development mode alongside the Django development server.

### Frontend

To run the frontend development server on localhost:3000 run the following commands
```
cd fontend
```

If the npm package has not been installed run the following command
```
npm install .
```

Run the development frontend build
```
npm run dev
```

### Backend

To run the backend development server on localhost:8000 run the following commands
```
cd backend
```

Install the required python packages
```
python -m venv env
source env/bin/active # Windows its .\env\Scripts\Activate.bat
pip install -r requirements.txt
```

Run the python development backend
```
python manage.py runserver
```


## Environment Variables

Environment variables are found in [./.env.prod](./.env.prod)

If no environment variables are set then the app defaults to running the backend on http://localhost:8000 and the frontend on http://localhost:3000

If a hcaptcha secret / site key are not set then the backend will not require a valid token to work

If no database url is set the app will default to using a SQLlite3 database for the backend

## Contribute

Anyone is welcome to contribution to the project!

Thank you for your support!

## License

Software is licensed under the MIT License found [here](./LICENSE)
