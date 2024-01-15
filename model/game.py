from datetime import datetime

from marshmallow import Schema,fields


class RoomData:
    def __init__(
        self,
        currentTurn=None,
        boardState="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        dataCreation=datetime.now(),
        isFree=True,
        gameState="Pending",
        lastMove=None,
        lastOnlinePlayerOne=datetime.now(),
        lastOnlinePlayerTwo=None,
        playerOneId=None,
        playerTwoId=None,
        rankPlayerOne=None,
        rankPlayerTwo=None,
        roomId=None,
        termination="",
        winner=""
    ):
        self.roomId = roomId
        self.playerOneId = playerOneId
        self.playerTwoId = playerTwoId
        self.isFree = isFree
        self.gameState = gameState
        self.lastOnlinePlayerOne = lastOnlinePlayerOne
        self.lastOnlinePlayerTwo = lastOnlinePlayerTwo
        self.rankPlayerOne = rankPlayerOne
        self.rankPlayerTwo = rankPlayerTwo
        self.dataCreation = dataCreation
        self.currentTurn = currentTurn
        self.boardState = boardState
        self.lastMove = lastMove
        self.winner = winner
        self.termination = termination

    @staticmethod
    def from_dict(source):
        room = RoomData(source["playerOneId"],
                        source["rankPlayerOne"], source["dataCreation"])

        return room

    def to_dict(self):
        return {
            "roomId": self.roomId,
            "playerOneId": self.playerOneId,
            "playerTwoId": self.playerTwoId,
            "isFree": self.isFree,
            "gameState": self.gameState,
            "lastOnlinePlayerOne": self.lastOnlinePlayerOne,
            "lastOnlinePlayerTwo": self.lastOnlinePlayerTwo,
            "rankPlayerOne": self.rankPlayerOne,
            "rankPlayerTwo": self.rankPlayerTwo,
            "dataCreation": self.dataCreation,
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
            f"isFree={self.isFree}, "
            f"gameState={self.gameState}, "
            f"lastOnlinePlayerOne={self.lastOnlinePlayerOne}, "
            f"lastOnlinePlayerTwo={self.lastOnlinePlayerTwo}, "
            f"rankPlayerOne={self.rankPlayerOne}, "
            f"rankPlayerTwo={self.rankPlayerTwo}, "
            f"dataCreation={self.dataCreation}), "
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
    isFree = fields.Boolean()
    gameState = fields.String()
    lastOnlinePlayerOne = fields.DateTime(allow_none=True)
    lastOnlinePlayerTwo = fields.DateTime(allow_none=True)
    rankPlayerOne = fields.Float(allow_none=True)
    rankPlayerTwo = fields.Float(allow_none=True)
    dataCreation = fields.DateTime(allow_none=True)
    currentTurn = fields.String()
    boardState = fields.String()
    lastMove = fields.String()
    winner = fields.String()
    termination = fields.String()