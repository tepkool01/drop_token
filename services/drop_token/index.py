import os
import boto3

# Custom libraries
from utilities.errors import MalformedRequest, NotFound, Conflict, GameFinished
from DropTokenSession import DropTokenSession
from utilities.Validation import Validation

# Caching area
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DATABASE_NAME'])


def lambda_handler(event, _):
    # Give the drop token session handler access to the database and any event details from the request
    dt_session = DropTokenSession(table, event)

    try:
        # GENERAL Validations, these will raise specific errors that will be rendered with the correct status code
        # VALIDATE: that game exists if accessing a resource that requires a game ID
        validate = Validation(event)
        if 'gameId' in event:
            game_info = dt_session.get_game()
            validate.set_game_info(game_info)  # Giving the validation class access to the game data

        # VALIDATE: Player is part of the game
        validate.player_in_game()

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
                # Validate if we received the OPTIONAL query string parameters. Both must be present
                if 'start' in event and 'until' in event:
                    validate.unsigned_integer_values(event['start'], event['until'])
                    validate.valid_query_range(event['start'], event['until'])

                    moves = dt_session.retrieve_moves(int(event['start']), int(event['until']))
                # Otherwise, show them all the moves for the game
                else:
                    moves = dt_session.retrieve_moves()

                return {
                    "moves": moves
                }

        elif event['resource'] == '/drop_token/{gameId}/moves/{move_number}':
            if event['method'] == 'GET':
                return 'Specific move'

        elif event['resource'] == '/drop_token/{gameId}/{playerId}':
            # VALIDATE: Game is not in 'DONE' state
            validate.game_is_active()

            # Player is a sore loser or forgot to feed the cat, they are leaving the game, an entry in moves is recorded
            if event['method'] == 'DELETE':
                dt_session.quit_game()
                return ''

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
    except Conflict as e:
        raise Exception({
            "reason": "CONFLICT",
            "message": str(e)
        })
    except GameFinished as e:
        raise Exception({
            "reason": "GONE",
            "message": str(e)
        })
    # General exception case for anything I can't catch, so we don't release important information
    except Exception as e:
        print(str(e))  # Normally would do a log level here
        raise Exception({
            "reason": "Unhandled Exception",
            "message": "See logs for details."
        })
