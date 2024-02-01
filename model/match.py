from marshmallow import Schema, fields


class Match(object):
    def __init__(self, roomid, matchType, userIdOne, userIdTwo, results, usernameUserTwo = None, profilePictureUrlUserTwo = None):
        self.roomId = roomid
        self.matchType = matchType
        self.userIdOne = userIdOne
        self.userIdTwo = userIdTwo
        self.results = results
        self.usernameUserTwo = usernameUserTwo
        self.profilePictureUrlUserTwo = profilePictureUrlUserTwo
    
    def __repr__(self):
        return (
            f"Match("
            f"roomId={self.roomId}, "
            f"matchType={self.matchType}, "
            f"userIdOne={self.userIdOne}, "
            f"userIdTwo={self.userIdTwo}, "
            f"results={self.results}, "
            f"usernameUserTwo={self.usernameUserTwo}, "
            f"profilePictureUrlUserTwo={self.profilePictureUrlUserTwo}"
        )

class MatchSchema(Schema):
    roomId = fields.String()
    matchType = fields.String()
    userIdOne = fields.String()
    userIdTwo = fields.String()
    results = fields.Integer()
    usernameUserTwo = fields.String()
    profilePictureUrlUserTwo = fields.String()

