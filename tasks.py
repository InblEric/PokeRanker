from celery import Celery, task

from pymongo import MongoClient

import math

client = MongoClient()
db = client.pokedatabase
pokemon_collection = db.pokemon_collection
vote_collection = db.vote_collection

celery = Celery("tasks", broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

def k_factor(elo):
    # I'm not sure where this came from:
     # ans = 116 - (0.04076923076923 * (elo-100))
     # TODO change this calculation eventually
     # https://ratings.fide.com/calculator_rtd.phtml
     return 20

def get_new_elos(winner_elo, loser_elo):
    qa = math.pow(10, (winner_elo/400))
    qb = math.pow(10, (loser_elo/400))

    winner_expected_score = qa / (qa + qb)
    loser_expected_score = qb / (qa + qb)

    new_winner_elo = winner_elo + k_factor(winner_elo) * (1 - winner_expected_score)
    new_loser_elo = loser_elo + k_factor(loser_elo) * (0 - loser_expected_score)

    return new_winner_elo, new_loser_elo

@celery.task
def update_elos(winner_id, loser_id, vote_id):
    winner = pokemon_collection.find_one({'pokemon_id':winner_id})
    loser = pokemon_collection.find_one({'pokemon_id':loser_id})

    winner_elo = winner["elo"]
    loser_elo = loser["elo"]

    new_winner_elo, new_loser_elo = get_new_elos(winner_elo, loser_elo)
    pokemon_collection.update_one({'pokemon_id': winner_id}, {'$set': {'elo': new_winner_elo}})
    pokemon_collection.update_one({'pokemon_id': loser_id}, {'$set': {'elo': new_loser_elo}})

    vote = vote_collection.find_one({'vote_id': vote_id})
    vote_collection.update_one({'vote_id': vote_id}, {'$set': {'status': "complete"}})
    return winner_elo, loser_elo
