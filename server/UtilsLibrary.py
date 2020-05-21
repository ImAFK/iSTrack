from pymongo import MongoClient
from bson.objectid import ObjectId
from record import Record
import pprint

class CloudSender(object):
    """ implementation of CRUD operations on Records collection in MongoDB """

    def connect():
        client = MongoClient("mongodb://admin:password@id4c.myqnapcloud.com:37011/")
        db = client['test']



    def __init__(self):
        # initializing the MongoClient, this helps to 
        # access the MongoDB databases and collections 
        #self.client = MongoClient(host='mongodb://id4c.myqnapcloud.com/', port=37011/)
        #self.cli
        #self.database = self.client['records']


    def create(self, record):
        if record is not None:
            self.database.record.insert(record.get_as_json())            
        else:
            raise Exception("Nothing to save, because record parameter is None")


    def read(self, record_id=None):
        if record_id is None:
            return self.database.records.find({})
        else:
            return self.database.records.find({"_id":records_id})


    def update(self, record):
        if record is not None:
            # the save() method updates the document if this has an _id property 
            # which appears in the collection, otherwise it saves the data
            # as a new document in the collection
            self.database.records.save(record.get_as_json())            
        else:
            raise Exception("Nothing to update, because record parameter is None")


    def delete(self, record):
        if record is not None:
            self.database.records.remove(record.get_as_json())            
        else:
            raise Exception("Nothing to delete, because record parameter is None")