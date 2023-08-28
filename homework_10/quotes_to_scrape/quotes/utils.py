from pymongo import MongoClient


def get_mongo():
    url = "mongodb+srv://woody0740:test_mongo@nomadd.z5x2h3l.mongodb.net/FirstMongoDB?retryWrites=true&w=majority"
    client = MongoClient(url)
    db = client.Homework_9

    return db
