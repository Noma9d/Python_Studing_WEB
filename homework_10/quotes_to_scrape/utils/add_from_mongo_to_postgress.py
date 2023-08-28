from models import Author, Quotes, session
from pymongo import MongoClient

url = "mongodb+srv://woody0740:test_mongo@nomadd.z5x2h3l.mongodb.net/FirstMongoDB?retryWrites=true&w=majority"
client = MongoClient(url)
db = client.Homework_9

authors = db.author.find()
quotes = db.quotes.find()

for el in authors:
    author = Author(fullname = el['fullname'], date_born = el['born_date'], location_born = el['born_location'], bio = el['description'])
    session.add(author)

for el in quotes:
    keywords = ' '.join(el['tags'])
    quote = Quotes(keywords = keywords, author = el['author'], quote = el['quote'])
    session.add(quote)