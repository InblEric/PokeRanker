Pokeranker
======

## Setup

Clone the repository.

### With Docker and Docker Compose

Install Docker and Docker Compose

```
$ docker-compose build
$ docker-compose up
```

Seed the database. In another terminal:

```
$ python

import os
from pymongo import MongoClient

client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
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

### Without Docker

Install docker and redis and mongo.

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

### After Setup

In another terminal:

```
$ curl -i http://127.0.0.1:5000/pokeranker/api/v1.0/pokemon
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 506
Server: Werkzeug/0.14.1 Python/3.6.0
Date: Thu, 24 May 2018 23:39:06 GMT

[
  {
    "elo": 1200.0,
    "gen": 1,
    "genRank": 1,
    "name": "Bulbasaur",
    "pokemon_id": 1,
    "rank": 1
  }
]
```

## Teardown

### Docker Teardown

```
$ ctrl c
```

Remove any docker images or containers you want to afterwards

Warning: if you remove the mongo or redis containers you will lose data/queued votes

### Without Docker Teardown

Warning: if you kill the mongo docker container you will lose all vote/elo data

To stop, go back to the terminal flask is running in:

```
$ ctrl c
$ celery -A tasks control shutdown
$ docker ps
$ docker kill <redis id>
$ docker kill <mongo_id>
```
