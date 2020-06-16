from mongoengine import *
from models.user import User
import os
from dotenv import load_dotenv

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__),)
PATH = os.path.join(BASEDIR, '..','.env')
# Connect the path with your '.env' file name
load_dotenv(PATH)

class UserManager:
    def __init__(self, server):
        atmongo_username = os.getenv('atmongo_username')
        atmongo_password = os.getenv('atmongo_password')
        atmongo_host = os.getenv('atmongo_host')
        atmongo_port = int(os.getenv('atmongo_port'))
        atmongo_db = os.getenv('atmongo_db')

        connect(atmongo_db,
                host='mongodb://' + atmongo_host,
                port=atmongo_port,
                username=atmongo_username,
                password=atmongo_password)
    
    def save(self, user):
        if user is not None:
            user.save()
            disconnect(alias='default')
        else:
            raise Exception("Nothing to save, because user parameter is None")

    def readAll(self):
        users = User.objects
        return users
        
    def readById(self, id_number):
        user = User.objects(id_number= id_number)
        return user

    def deleteById(self, id_number):
       user = User.objects(id_number= id_number)
       if user is not None:
           user.delete()
           return True
       else:
            return False

    def disconnect(self, alias):
        disconnect(alias=alias)

