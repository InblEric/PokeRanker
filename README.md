Pokeranker
======

## Setup

Install docker and redis.

Clone the repository.

```
$ pip install -r requirements.txt
$ docker run -p 27017:27017 mongo &
$ docker run -p 6379:6379 redis &
$ celery -A tasks worker --loglevel=info &
$ export FLASK_APP=app.py
$ export FLASK_DEBUG=1
$ flask run
```

Seed the database. In another terminal:

```
$ python

from pymongo import MongoClient
client = MongoClient()
db = client.pokedatabase
pokemon_collection = db.pokemon_collection
```

Using a list of dictionaires with this format, insert them into the database:

```
pokemon = [
    {
        "pokemon_id": 1,
        "name": "Bulbasaur",
        "gen": 1,
        "rank": 1,
        "genRank": 1,
        "elo": 1200.0
    }
]

for poke in pokemon:
  pokemon_collection.insert_one(poke)
```

In another terminal:

```
$ curl -i http://127.0.0.1:5000/pokeranker/api/v1.0/pokemon
```

## Teardown

Warning: if you kill the mongo docker container you will lose all vote/elo data

To stop, go back to the terminal flask is running in:

```
$ ctrl c
$ celery -A tasks control shutdown
$ docker ps
$ docker kill <redis id>
$ docker kill <mongo_id>
```
