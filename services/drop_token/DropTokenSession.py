import uuid
from boto3.dynamodb.conditions import Key, Attr

from utilities.GameState import GameState
from utilities.errors import NotFound
from DropTokenGame import DropTokenGame


class DropTokenSession(object):
    """
    Class that handles interactions and transformations from the database
    """
    def __init__(self, db, event):
        self.db = db
        self.event = event

    def create_game(self) -> str:
        """
        Creates a game session with a unique identifier, and the payload that the user submitted. Additional validation
        Could be performed here
        :return: string of game ID
        """
        game_id = str(uuid.uuid4())  # Generate random unique identifier
        self.db.put_item(
            Item={
                'gameId': game_id,
                'state': GameState.ACTIVE.val(),
                'players': self.event['body']['players'],
                'rows': self.event['body']['rows'],
                'columns': self.event['body']['columns'],
                'moves': []
            }
        )
        return game_id

    def get_active_games(self) -> []:
        """
        Retrieves all active games
        Does a table scan (can be slow, but works fine given the requirements)
        In the future if these needed to scale a lot, would need a continuation token / while loop
        :return: Array of game IDs
        """
        # Retrieve results
        response = self.db.scan(
            FilterExpression=Attr('state').eq(GameState.ACTIVE.val())
        )
        # Parse for just game ids
        game_ids = []
        for game in response['Items']:
            game_ids.append(game['gameId'])

        return game_ids

    def get_game(self) -> dict:
        try:
            response = self.db.query(
                KeyConditionExpression=Key('gameId').eq(self.event['gameId'])
            )
            return response['Items'][0]
        except Exception as e:
            raise NotFound("Game not found.")

    def create_move(self):
        # Retrieve current game session
        game_data = self.get_game()

        # Get board array, and set to None so game machine can create it
        board_state = game_data['board_state'] if 'board_state' in game_data else None

        if self.event['playerId'] not in game_data['players']:
            raise NotFound('Player is not part of this game.')

        # todo: check for if it is not their turn
        current_player_token = 0 if game_data['players'][0] == self.event['playerId'] else 1

        drop_token = DropTokenGame(board_state, int(game_data['columns']), int(game_data['rows']))
        drop_token.set_player(current_player_token)
        drop_token.set_move(self.event['body']['column'])

        # todo: Check only after >= 8 moves made
        win_state = drop_token.get_win_state()
        winner = ''
        state = GameState.ACTIVE.val()

        if win_state is True:
            winner = self.event['playerId']
            state = GameState.COMPLETE.val()

        game_data['moves'].append({
            "type": "MOVE",
            "player": self.event['playerId'],
            "column": self.event['body']['column']
        })
        _, num = self.get_latest_move(game_data)

        self.db.update_item(
            Key={'gameId': self.event['gameId']},
            UpdateExpression="set moves=:m, #st=:s, winner=:w, board_state=:b",
            ExpressionAttributeValues={
                ':m': game_data['moves'],
                ':s': state,
                ':w': winner,
                ':b': drop_token.board_state
            },
            ExpressionAttributeNames={
                "#st": "state"
            },
            ReturnValues="UPDATED_NEW"
        )
        return {
            'move': f"{self.event['gameId']}/moves/{num}"
        }

    @staticmethod
    def get_latest_move(game_data):
        count = len(game_data['moves'])
        # Check if this is the first move being made
        if count > 0:
            last_player = game_data['moves'][count-1]['player']
        else:
            last_player = ''

        return last_player, count

    def quit_game(self):
        pass
