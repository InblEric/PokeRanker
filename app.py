from flask import Flask, jsonify, abort

app = Flask(__name__)

# TODO this data will eventually be stored in a database
pokemon = [
    {
        "pokemon_id": 1,
        "name": "Bulbasaur",
        "gen": 1,
        "rank": 1,
        "genRank": 1
    },
    {
        "pokemon_id": 2,
        "name": "Ivysaur",
        "gen": 1,
        "rank": 2,
        "genRank": 2
    },
    {
        "pokemon_id": 152,
        "name": "Chikorita",
        "gen": 2,
        "rank": 3,
        "genRank": 1
    }]

votes = []

# GET /pokemon
@app.route('/pokeranker/api/v1.0/pokemon', methods=['GET'])
def get_pokemon_list():
    return jsonify(pokemon)

# GET /pokemon/gen/{gen}
@app.route('/pokeranker/api/v1.0/pokemon/gen/<int:gen>', methods=['GET'])
def get_pokemon_list_gen(gen):
    if type(gen) is not int or gen < 1 or gen > 7:
        abort(404)
    gen_pokemon = [poke for poke in pokemon if poke["gen"] == gen]
    return jsonify(gen_pokemon)

# GET /pokemon/{pokemon_id} (int)
@app.route('/pokeranker/api/v1.0/pokemon/<int:pokemon_id>', methods=['GET'])
def get_pokemon(pokemon_id):
    if type(pokemon_id) is not int or pokemon_id < 1 or pokemon_id > 807:
        abort(404)
    found = False
    for poke in pokemon:
        if poke["pokemon_id"] == pokemon_id:
            return jsonify(poke)
    if not found:
        abort(404)

# GET /votes
@app.route('/pokeranker/api/v1.0/votes')
def get_votes():
    return jsonify(votes)

# POST /votes
# TODO

# GET /votes/{vote_id} (string)
@app.route('/pokeranker/api/v1.0/votes/<str:vote_id>', methods=['GET'])
def get_vote_status(vote_id):
    if type(vote_id) is not str: # TODO: validate the vote id
        abort(404)
    found = False
    for vote in votes:
        if vote["vote_id"] == vote_id:
            return jsonify(vote)
    if not found:
        abort(404)

# GET /ranks/match
@app.route('/pokeranker/api/v1.0/ranks/match', methods=['GET'])
def get_match():
    # TODO get two pokemon from pokemon at random and build this dict
    match = {
        "one": "string",
        "two": "string",
        "oneid": 0,
        "twoid": 0
    }
    return jsonify(match)

# GET /ranks/match/gen/{gen}
@app.route('/pokeranker/api/v1.0/ranks/match/gen/<int:gen>', methods=['GET'])
def get_match_gen(gen):
    if type(gen) is not int or gen < 1 or gen > 7:
        abort(404)
    gen_pokemon = [poke for poke in pokemon if poke["gen"] == gen]
    # TODO get two pokemon from gen_pokemon at random and build this dict
    match = {
        "one": "string",
        "two": "string",
        "oneid": 0,
        "twoid": 0
    }
    return jsonify(match)

if __name__ == '__main__':
    app.run(debug=False)
