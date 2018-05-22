from flask import Flask, jsonify, abort

app = Flask(__name__)

pokemon = [{"pokemon_id": 1,
    "name": "Bulbasaur",
    "gen": 1,
    "rank": 1,
    "genRank": 1},{"pokemon_id": 2,
    "name": "Ivysaur",
    "gen": 1,
    "rank": 2,
    "genRank": 2}]

@app.route('/pokeranker/api/v1.0/pokemon', methods=['GET'])
def get_pokemon_list():
    return jsonify(pokemon)

@app.route('/pokeranker/api/v1.0/pokemon/gen/<int:gen>', methods=['GET'])
def get_pokemon_list_gen(gen):
    if type(gen) is not int or gen < 1 or gen > 7:
        abort(404)
    gen_pokemon = [poke for poke in pokemon if poke["gen"] == gen]
    return jsonify(gen_pokemon)

if __name__ == '__main__':
    app.run(debug=False)
