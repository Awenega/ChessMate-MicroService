from marshmallow import Schema,fields

class RoomData:
    def __init__(
        self,
        currentTurn=None,
        boardState="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        gameState="CREATED",
        lastMove=None,
        playerOneId=None,
        playerTwoId=None,
        playerOneUsername=None,
        playerTwoUsername=None,
        rankPlayerOne=None,
        rankPlayerTwo=None,
        roomId=None,
        termination="",
        winner=""
    ):
        self.roomId = roomId
        self.playerOneId = playerOneId
        self.playerTwoId = playerTwoId
        self.playerOneUsername = playerOneUsername
        self.playerTwoUsername = playerTwoUsername
        self.gameState = gameState
        self.rankPlayerOne = rankPlayerOne
        self.rankPlayerTwo = rankPlayerTwo
        self.currentTurn = currentTurn
        self.boardState = boardState
        self.lastMove = lastMove
        self.winner = winner
        self.termination = termination

    @staticmethod
    def from_dict(source):
        room = RoomData(playerOneId=source["playerOneId"],
                        rankPlayerOne=source["rankPlayerOne"],
                        playerOneUsername=source["playerOneUsername"])

        return room

    def to_dict(self):
        return {
            "roomId": self.roomId,
            "playerOneId": self.playerOneId,
            "playerTwoId": self.playerTwoId,
            "playerOneUsername": self.playerOneUsername,
            "playerTwoUsername": self.playerTwoUsername,
            "gameState": self.gameState,
            "rankPlayerOne": self.rankPlayerOne,
            "rankPlayerTwo": self.rankPlayerTwo,
            "currentTurn": self.currentTurn,
            "boardState": self.boardState,
            "lastMove": self.lastMove,
            "winner": self.winner,
            "termination": self.termination
        }

    def __repr__(self):
        return (
            f"RoomData("
            f"roomId={self.roomId}, "
            f"playerOneId={self.playerOneId}, "
            f"playerTwoId={self.playerTwoId}, "
            f"playerOneUsername={self.playerOneUsername}, "
            f"playerTwoUsername={self.playerTwoUsername}, "
            f"gameState={self.gameState}, "
            f"rankPlayerOne={self.rankPlayerOne}, "
            f"rankPlayerTwo={self.rankPlayerTwo}, "
            f"currentTurn={self.currentTurn}, "
            f"boardState={self.boardState}, "
            f"lastMove={self.lastMove}), "
            f"winner={self.winner}, "
            f"termination={self.termination}"
        )

class GameSchema(Schema):
    roomId = fields.String()
    playerOneId = fields.String()
    playerTwoId = fields.String()
    playerOneUsername = fields.String()
    playerTwoUsername = fields.String()
    gameState = fields.String()
    rankPlayerOne = fields.Float(allow_none=True)
    rankPlayerTwo = fields.Float(allow_none=True)
    currentTurn = fields.String()
    boardState = fields.String()
    lastMove = fields.String()
    winner = fields.String()
    termination = fields.String()