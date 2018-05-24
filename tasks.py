from celery import Celery, task

celery = Celery("tasks", broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery.task
def update_elos(winner_id, loser_id, pokemon):
    # TODO get pokemon from db using the ids, compute new elos and update
    # db entries
    # then get the vote from db using the vote_id,
    # and set the vote status to 'done'
    return 0
