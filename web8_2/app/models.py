from common import mongo


class Contact(mongo.Document):
    full_name = mongo.StringField(required=True)
    email = mongo.EmailField(required=True)
    sent = mongo.BooleanField(default=False)
