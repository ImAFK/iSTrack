from mongoengine import *
from user import User

class UserManager:
    def __init__(self):
        connect('admin', host='mongodb://id4c.myqnapcloud.com/', port=37011, username = 'admin', password = 'password')
        pass
    
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