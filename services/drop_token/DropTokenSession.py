import uuid
from boto3.dynamodb.conditions import Key, Attr
from utilities.GameState import GameState


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
                'status': GameState.ACTIVE.val(),
                'players': self.event['body']['players']
            }
        )
        return game_id

    def get_active_games(self) -> []:
        """
        Retrieves all active games, denoted by a status of 1.
        Does a table scan (can be slow, but works fine given the requirements)
        In the future if these needed to scale a lot, would need a continuation token / while loop
        :return: Array of game IDs
        """
        # Retrieve results
        response = self.db.scan(
            FilterExpression=Attr('status').eq(GameState.ACTIVE.val())
        )
        # Parse for just game ids
        game_ids = []
        for game in response['Items']:
            game_ids.append(game['gameId'])

        return game_ids

    def get_game(self):
        response = self.db.query(
            KeyConditionExpression=Key('gameId').eq(self.event['gameId'])
        )
        return response['Items'][0]
