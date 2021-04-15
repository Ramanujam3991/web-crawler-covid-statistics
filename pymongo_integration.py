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



def insertIntoDb(dictarr, table_name=''):
    global collection
    print('table_name>>>',table_name)
    if table_name=='':
        collection.insert_many(dictarr)
    else:
        print('table_name::',table_name)
        collection = database[COLLECTION_NAME+'_'+table_name]
        collection.insert_many(dictarr)
