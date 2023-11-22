from marshmallow import Schema, fields

class User(object):
    def __init__(self, id, email, emailVerified, profilePictureUrl, provider, username):
        self.id = id
        self.email = email
        self.emailVerified = emailVerified
        self.profilePictureUrl = profilePictureUrl
        self.provider = provider
        self.username = username

class UserSchema(Schema):
    id = fields.String()
    email = fields.String()
    emailVerified = fields.Boolean()
    profilePictureUrl = fields.String()
    provider = fields.String()
    username = fields.String()

    
