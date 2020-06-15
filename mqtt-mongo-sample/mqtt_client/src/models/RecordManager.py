from mongoengine import *
from models.record import Record
from models.record import Record
import os
from dotenv import load_dotenv

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__),)
PATH = os.path.join(BASEDIR, '..','.env')
# Connect the path with your '.env' file name
load_dotenv(PATH)

class RecordManager:
    def __init__(self, server):
        if server is 'rpi':
            rpimongo_db = 'recordsData'
            rpimongo_port = 27017
            rpimongo_host = 'mongo'
            connect(rpimongo_db,
                    host='mongodb://' + rpimongo_host,
                    port=rpimongo_port,
                    alias='rpi')
        elif server is 'advantech':
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
        # load credentials
        # atmongo_username = os.getenv('atmongo_username')
        # atmongo_password = os.getenv('atmongo_password')
        # atmongo_host = os.getenv('atmongo_host')
        # atmongo_port = int(os.getenv('atmongo_port'))
        # atmongo_db = os.getenv('atmongo_db')
        #
        # connect(atmongo_db,
        #         host='mongodb://' + atmongo_host,
        #         port=atmongo_port,
        #         username = atmongo_username,
        #         password = atmongo_password)
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