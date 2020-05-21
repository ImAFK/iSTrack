from mongoengine import *
#connect('test', host='mongodb://id4c.myqnapcloud.com/', port=37011, username = 'admin', password = 'password')
from record import Record

class RecordManager:
    def __init__(self):
        connect('admin', host='mongodb://id4c.myqnapcloud.com/', port=37011, username = 'admin', password = 'password')
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