class RoomData:
    def __init__(
        self,
        roomId=None,
        playerOneId=None,
        playerTwoId=None,
        isFree=True,
        gameState="Pending",
        isOnlinePlayerOne=True,
        isOnlinePlayerTwo=False,
        rankPlayerOne=None,
        rankPlayerTwo=None,
        dataCreation=None
    ):
        self.roomId = roomId
        self.playerOneId = playerOneId
        self.playerTwoId = playerTwoId
        self.isFree = isFree
        self.gameState = gameState
        self.isOnlinePlayerOne = isOnlinePlayerOne
        self.isOnlinePlayerTwo = isOnlinePlayerTwo
        self.rankPlayerOne = rankPlayerOne
        self.rankPlayerTwo = rankPlayerTwo
        self.dataCreation = dataCreation

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
            "isOnlinePlayerOne": self.isOnlinePlayerOne,
            "isOnlinePlayerTwo": self.isOnlinePlayerTwo,
            "rankPlayerOne": self.rankPlayerOne,
            "rankPlayerTwo": self.rankPlayerTwo,
            "dataCreation": self.dataCreation
        }

    def __repr__(self):
        return (
            f"RoomData("
            f"roomId={self.roomId}, "
            f"playerOneId={self.playerOneId}, "
            f"playerTwoId={self.playerTwoId}, "
            f"isFree={self.isFree}, "
            f"gameState={self.gameState}, "
            f"isOnlinePlayerOne={self.isOnlinePlayerOne}, "
            f"isOnlinePlayerTwo={self.isOnlinePlayerTwo}, "
            f"rankPlayerOne={self.rankPlayerOne}, "
            f"rankPlayerTwo={self.rankPlayerTwo}, "
            f"dataCreation={self.dataCreation})"
        )
