from mongoengine import *
import datetime

class User (Document):

    id_number = StringField(required=True, unique = True )
    first_name = StringField(required=True )
    last_name = StringField(required=True )
    phone_number = StringField(required=True )
    email = StringField(required=False )