Pokeranker
======

## Setup

Install docker and redis.

Clone the repository.

```
$ pip install -r requirements.txt
$ docker run -p 6379:6379 redis &
$ TODO run mongo
$ celery -A tasks worker --loglevel=info &
$ export FLASK_APP=app.py
$ export FLASK_DEBUG=1
$ flask run
```

In another terminal:

```
$ curl -i http://127.0.0.1:5000/pokeranker/api/v1.0/pokemon
```

To stop, go back to the terminal flask is running in:

```
$ ctrl c
$ celery -A tasks control shutdown
$ TODO shutdown mongo
$ docker ps
$ docker kill <redis id>
```
