import os
import django
from pymongo import MongoClient


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes_to_scrape.settings")
django.setup()


from quotes.models import Quote, Tag, Author  # noqa


url = "mongodb+srv://woody0740:test_mongo@nomadd.z5x2h3l.mongodb.net/FirstMongoDB?retryWrites=true&w=majority"
client = MongoClient(url)
db = client.Homework_9

authors = db.author.find()
quotes = db.quotes.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author["fullname"],
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"],
    )


for quote in quotes:
    tags = []
    for tag in quote["tags"]:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quote.objects.filter(quote=quote["quote"])))

    if not exist_quote:
        author = db.author.find_one({"fullname": quote["author"]})
        a = Author.objects.get(fullname=author["fullname"])
        q = Quote.objects.create(quote=quote["quote"], author=a)
        for tag in tags:
            q.tags.add(tag)