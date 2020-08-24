import json

import os
import boto3

# Custom libraries
from utilities.errors import MalformedRequest, NotFound
from DropTokenSession import DropTokenSession

# Caching area
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DATABASE_NAME'])


def lambda_handler(event, _):
    # Give the drop token session handler access to the database and any event details from the request
    dt_session = DropTokenSession(table, event)

    try:
        # ROUTES and RESPONSES
        if event['resource'] == '/drop_token':
            # Creating a game
            if event['method'] == 'POST':
                game_id = dt_session.create_game()
                return {
                    'gameId': game_id
                }

            # Showing all games
            elif event['method'] == 'GET':
                games = dt_session.get_active_games()
                return {
                    'games': games
                }

        elif event['resource'] == '/drop_token/{gameId}':
            # Retrieve one single game and all the related information
            if event['method'] == 'GET':
                game = dt_session.get_game()
                return game

        elif event['resource'] == '/drop_token/{gameId}/moves':
            if event['method'] == 'GET':
                # Optional 'start' and 'until' query string parameters TODO:
                print(event)
                return 'All moves'

        elif event['resource'] == '/drop_token/{gameId}/moves/{move_number}':
            if event['method'] == 'GET':
                return 'Specific move'

        elif event['resource'] == '/drop_token/{gameId}/{playerId}':
            if event['method'] == 'DELETE':
                return 'Player terminated session'

            # Player is making a move! This is where the fun happens!
            elif event['method'] == 'POST':
                move = dt_session.create_move()
                return move

    # Begin the handling of errors sent from the game session or game
    except MalformedRequest as e:
        raise Exception({
            "reason": "BAD_REQUEST",
            "message": str(e)
        })
    except NotFound as e:
        raise Exception({
            "reason": "NOT_FOUND",
            "message": str(e)
        })

    return "Test"




# b = [
#     [1, None, 0, None],
#     [0, None, None, 1],
#     [1, 1, 1, 0],
#     [1, 1, 0, 1]
# ]
# # drop_token = DropToken(b)
# #
# # res = drop_token.validate_move(0)
# # print(res)
#
# d = DropToken(b)
# d.set_move(1)
# print(d.get_win_state())
