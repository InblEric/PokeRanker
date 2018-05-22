from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

# TODO this data will eventually be stored in a database
pokemon = [
    {
        "pokemon_id": 1,
        "name": "Bulbasaur",
        "gen": 1,
        "rank": 1,
        "genRank": 1,
        "elo": 1200
    },
    {
        "pokemon_id": 2,
        "name": "Ivysaur",
        "gen": 1,
        "rank": 2,
        "genRank": 2,
        "elo": 1200
    },
    {
        "pokemon_id": 152,
        "name": "Chikorita",
        "gen": 2,
        "rank": 3,
        "genRank": 1,
        "elo": 1200
    }]

votes = []

# GET /pokemon
@app.route('/pokeranker/api/v1.0/pokemon', methods=['GET'])
def get_pokemon_list():
    return jsonify(pokemon)

# GET /pokemon/gen/{gen}
@app.route('/pokeranker/api/v1.0/pokemon/gen/<int:gen>', methods=['GET'])
def get_pokemon_list_gen(gen):
    # TODO write helper to validate the gen
    if type(gen) is not int or gen < 1 or gen > 7:
        abort(404)
    gen_pokemon = [poke for poke in pokemon if poke["gen"] == gen]
    return jsonify(gen_pokemon)

# GET /pokemon/{pokemon_id} (int)
@app.route('/pokeranker/api/v1.0/pokemon/<int:pokemon_id>', methods=['GET'])
def get_pokemon(pokemon_id):
    # TODO write helper to validate the ids
    if type(pokemon_id) is not int or pokemon_id < 1 or pokemon_id > 807:
        abort(404)
    found = False
    for poke in pokemon:
        if poke["pokemon_id"] == pokemon_id:
            return jsonify(poke)
    if not found:
        abort(404)

# GET /votes
@app.route('/pokeranker/api/v1.0/votes', methods=['GET'])
def get_votes():
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
    if len(votes) == 0:
        vote = {
            'vote_id': 1,
            "status": "new",
            "winner_id": winner_id,
            "loser_id": loser_id
        }
    else:
        vote = {
            'vote_id': votes[-1]['vote_id'] + 1,
            "status": "new",
            "winner_id": request.json['winner_id'],
            "loser_id": request.json['loser_id']
        }
    votes.append(vote)

    # TODO: apply ELO changes, update ranks, then set status of new vote to "done"
    # or you can do this somewhere else using workers or something

    return jsonify(vote), 201


# GET /votes/{vote_id} (int)
@app.route('/pokeranker/api/v1.0/votes/<int:vote_id>', methods=['GET'])
def get_vote_status(vote_id):
    # TODO write helper to validate the ids
    if type(vote_id) is not int or vote_id < 0 or vote_id > len(votes):
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
    # TODO write helper to validate the gen
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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

if __name__ == '__main__':
    app.run(debug=False)
