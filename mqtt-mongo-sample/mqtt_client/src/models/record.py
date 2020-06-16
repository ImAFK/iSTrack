from mongoengine import *
import datetime


class Record (Document):

    id_number = StringField(required=True, unique = False)
    location = StringField(required=True )
    body_temperature = FloatField(required=True )
    date = DateTimeField(default=datetime.datetime.now)


    # meta = {'alias': 'default', 'db': 'record'}

