from mongoengine import *
from record import Record
import os

class RecordManager:
    def __init__(self):
        if not os.path.exists('/usr/src/app/src/credentials.conf'):
            print('Config not found')
        else:
            # load credentials
            creds_config = configparser.ConfigParser()
            creds_config.read('/usr/src/app/src/credentials.conf')
            atmongo_username = creds_config['ATMongo']['atmongo_username']
            atmongo_password = creds_config['ATMongo']['atmongo_password']
            atmongo_host = creds_config['ATMongo']['atmongo_host']
            atmongo_port = creds_config['ATMongo']['atmongo_port']
            atmongo_db = creds_config['ATMongo']['atmongo_db']
        connect(atmongo_db,
                host='mongodb://' + atmongo_host,
                port=atmongo_port,
                username = atmongo_username,
                password = atmongo_password)
        pass
    
    def save(self, record):
        if record is not None:
            record.save()
            disconnect(alias='default')
        else:
            raise Exception("Nothing to save, because record parameter is None")

    def readAll(self):
        records = Record.objects
        return records
        
    def readById(self, record_id):
        record = Record.objects(id_number= record_id)
        return record

    # Depends on what we are updating
    """def updateById(self, record_id):
        record = Record.objects(id_number= record_id)
        record.update()"""

    def deleteById(self, record_id):
       record = Record.objects(id_number= record_id)
       if record is not None:
           record.delete()
           return True
       else:
            return False