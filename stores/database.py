from pymongo import MongoClient, errors
import json
from definition import *


class MongoDatabase:
    def __init__(self):
        pass

    '''
	* get mongo_uri depend on ENV 
	* @param ENV - prod/dev/test
	*
	* @return
	*   $mongo_uri
	'''

    def get_uri(self, ENV):

        data = json.loads(open(MONGO_URI).read())
        if ENV == 'local':
            mongo_uri = data['config'][ENV]['mongo_uri']
        elif ENV == 'prod':
            mongo_uri = data['config'][ENV]['mongo_uri']
        elif ENV == 'dev':
            mongo_uri = data['config'][ENV]['mongo_uri']
        return mongo_uri

    '''
	* connect to the database by given mongo_uri
	* @param uri - mongo_uri
	*
	* @return
	*   $mongodb client 
	'''

    def connect(self, uri):

        try:
            print("Attempting to connect...")
            client = MongoClient(uri)
            # print("server_info():", client.server_info())
        except errors.ServerSelectionTimeoutError as err:
            print("Connection timeout error: ", err)
            client = None
        except errors.ConnectionFailure as err:
            print("Connection failure: ", err)
            client = None

        return client
