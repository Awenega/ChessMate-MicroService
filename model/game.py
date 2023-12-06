from marshmallow import Schema, fields


class Game(object):
    def __init__(self, id, playerOneId, playerTwoId, win, duration):
        self.playerOneId = playerOneId
        self.playerTwoId = playerTwoId
        self.win = win
        self.duration = duration


class UserSchema(Schema):
    playerOneId = fields.String()
    playerTwoId = fields.String()
    win = fields.Boolean()
    duration = fields.String()
