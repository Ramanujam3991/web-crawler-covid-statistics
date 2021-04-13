import pymongo

DB_URL = "mongodb+srv://dev:dev@cluster0.73vby.mongodb.net/sampleDB?retryWrites=true&w=majority"
DB_NAME = "sampleDB"
COLLECTION_NAME = "web_crawler"

databaseServers = pymongo.MongoClient(DB_URL)
database = databaseServers[DB_NAME]
collection = database[COLLECTION_NAME]

def clear_data():
    print('Clearing data....')
    collection.delete_many({})
    print('Cleared data....')

def insertIntoDb(dictarr):
    collection.insert_many(dictarr)
