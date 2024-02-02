from marshmallow import Schema,fields

class RoomData:
    def __init__(
        self,
        currentTurn=None,
        boardState="",
        fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        gameState="CREATED",
        lastMove=None,
        playerOneId=None,
        playerTwoId=None,
        pictureUrlOne=None,
        pictureUrlTwo=None,
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
        self.pictureUrlOne = pictureUrlOne
        self.pictureUrlTwo = pictureUrlTwo
        self.gameState = gameState
        self.rankPlayerOne = rankPlayerOne
        self.rankPlayerTwo = rankPlayerTwo
        self.currentTurn = currentTurn
        self.boardState = boardState
        self.fen = fen
        self.lastMove = lastMove
        self.winner = winner
        self.termination = termination

    @staticmethod
    def from_dict(source):
        room = RoomData(playerOneId=source["playerOneId"],
                        rankPlayerOne=source["rankPlayerOne"],
                        playerOneUsername=source["playerOneUsername"],
                        pictureUrlOne=source["pictureUrlOne"]
                        )

        return room

    def to_dict(self):
        return {
            "roomId": self.roomId,
            "playerOneId": self.playerOneId,
            "playerTwoId": self.playerTwoId,
            "playerOneUsername": self.playerOneUsername,
            "playerTwoUsername": self.playerTwoUsername,
            "pictureUrlOne": self.pictureUrlOne,
            "pictureUrlTwo": self.pictureUrlTwo,
            "gameState": self.gameState,
            "rankPlayerOne": self.rankPlayerOne,
            "rankPlayerTwo": self.rankPlayerTwo,
            "currentTurn": self.currentTurn,
            "boardState": self.boardState,
            "fen": self.fen,
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
            f"pictureUrlOne={self.pictureUrlOne}, "
            f"pictureUrlTwo={self.pictureUrlTwo}, "
            f"gameState={self.gameState}, "
            f"rankPlayerOne={self.rankPlayerOne}, "
            f"rankPlayerTwo={self.rankPlayerTwo}, "
            f"currentTurn={self.currentTurn}, "
            f"boardState={self.boardState}, "
            f"fen={self.fen}, "
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
    pictureUrlOne = fields.String()
    pictureUrlTwo = fields.String()
    gameState = fields.String()
    rankPlayerOne = fields.Float(allow_none=True)
    rankPlayerTwo = fields.Float(allow_none=True)
    currentTurn = fields.String()
    boardState = fields.String()
    fen = fields.String()
    lastMove = fields.String()
    winner = fields.String()
    termination = fields.String()