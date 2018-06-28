import os
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS
from random import randint
from tasks import update_elos
from pymongo import MongoClient, DESCENDING, ASCENDING

client = MongoClient(
    os.environ['DB_PORT_27017_TCP_ADDR'],
    27017)
db = client.pokedatabase
pokemon_collection = db.pokemon_collection
vote_collection = db.vote_collection

app = Flask(__name__)

CORS(app)

# GET /pokemon
@app.route('/pokeranker/api/v1.0/pokemon', methods=['GET'])
def get_pokemon_list():
    pokemon_cursor = pokemon_collection.find({}, {'_id': False}).sort("elo", DESCENDING)
    pokemon = [poke for poke in pokemon_cursor]
    return jsonify(pokemon)

# GET /pokemon/gen/{gen}
@app.route('/pokeranker/api/v1.0/pokemon/gen/<int:gen>', methods=['GET'])
def get_pokemon_list_gen(gen):
    # TODO write helper to validate the gen
    if type(gen) is not int or gen < 1 or gen > 7:
        abort(404)
    pokemon_cursor = pokemon_collection.find({'gen':gen}, {'_id': False}).sort("elo", DESCENDING)
    gen_pokemon = [poke for poke in pokemon_cursor]
    return jsonify(gen_pokemon)

# GET /pokemon/{pokemon_id} (int)
@app.route('/pokeranker/api/v1.0/pokemon/<int:pokemon_id>', methods=['GET'])
def get_pokemon(pokemon_id):
    # TODO write helper to validate the ids
    if type(pokemon_id) is not int or pokemon_id < 1 or pokemon_id > 807:
        abort(404)
    pokemon = pokemon_collection.find_one({'pokemon_id':pokemon_id}, {'_id': False})
    if pokemon is None:
        abort(404)
    return jsonify(pokemon)

# GET /votes
@app.route('/pokeranker/api/v1.0/votes', methods=['GET'])
def get_votes():
    votes_cursor = vote_collection.find({}, {'_id': False})
    votes = [poke for poke in votes_cursor]
    return jsonify(votes)

# POST /votes
@app.route('/pokeranker/api/v1.0/votes', methods=['POST'])
def submit_vote():
    # TODO write helper to validate the request json
    if not request.json or not 'winner_id' in request.json \
        or not 'loser_id' in request.json or len(request.json.keys()) is not 2:
        abort(400)
    # TODO write helper to validate the ids
    winner_id = request.json['winner_id']
    loser_id = request.json['loser_id']
    if type(winner_id) is not int or winner_id < 1 or winner_id > 807:
        abort(404)
    if type(loser_id) is not int or loser_id < 1 or loser_id > 807:
        abort(404)

    vote_id = vote_collection.count() + 1
    vote = {
        'vote_id': vote_id,
        "status": "pending",
        "winner_id": winner_id,
        "loser_id": loser_id
    }
    vote_collection.insert_one(vote)
    result = update_elos.delay(winner_id, loser_id, vote_id)
    vote = vote_collection.find_one({'vote_id':vote_id}, {'_id': False})
    return jsonify(vote), 201


# GET /votes/{vote_id} (int)
@app.route('/pokeranker/api/v1.0/votes/<int:vote_id>', methods=['GET'])
def get_vote_status(vote_id):
    # TODO write helper to validate the ids
    if type(vote_id) is not int or vote_id <= 0 or vote_id > vote_collection.count():
        abort(404)
    vote = vote_collection.find_one({'vote_id':vote_id}, {'_id': False})
    return jsonify(vote)
    if not found:
        abort(404)

# GET /match
@app.route('/pokeranker/api/v1.0/match', methods=['GET'])
def get_match():
    # TODO get len from db
    index_one = randint(0, pokemon_collection.count()-1)
    index_two = randint(0, pokemon_collection.count()-1)
    while index_one == index_two:
        index_two = randint(0, pokemon_collection.count()-1)

    pokemon_one = pokemon_collection.find({}, {'_id': False})[index_one]
    pokemon_two = pokemon_collection.find({}, {'_id': False})[index_two]
    match = {
        "one": pokemon_one["name"],
        "two": pokemon_two["name"],
        "oneid": pokemon_one["pokemon_id"],
        "twoid": pokemon_two["pokemon_id"]
    }
    return jsonify(match)

# GET /match/gen/{gen}
@app.route('/pokeranker/api/v1.0/match/gen/<int:gen>', methods=['GET'])
def get_match_gen(gen):
    # TODO write helper to validate the gen
    if type(gen) is not int or gen < 1 or gen > 7:
        abort(404)
    pokemon_cursor = pokemon_collection.find({'gen':gen}, {'_id': False})
    gen_pokemon = [poke for poke in pokemon_cursor]

    index_one = randint(0,len(gen_pokemon)-1)
    index_two = randint(0,len(gen_pokemon)-1)
    while index_one == index_two:
        index_two = randint(0,len(gen_pokemon)-1)

    pokemon_one = gen_pokemon[index_one]
    pokemon_two = gen_pokemon[index_two]
    match = {
        "one": pokemon_one["name"],
        "two": pokemon_two["name"],
        "oneid": pokemon_one["pokemon_id"],
        "twoid": pokemon_two["pokemon_id"]
    }
    return jsonify(match)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
