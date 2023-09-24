from django.db.models import (
    Model,
    CharField,
    TextField,
    DateTimeField,
    ForeignKey,
    CASCADE,
    ManyToManyField,
)

# Create your models here.


class Author(Model):
    fullname = CharField(max_length=50)
    born_date = CharField(max_length=50)
    born_location = CharField(max_length=150)
    description = TextField()
    created_at = DateTimeField(auto_now_add=True)


class Tag(Model):
    name = CharField(max_length=50, null=False, unique=True)


class Quote(Model):
    quote = TextField()
    tags = ManyToManyField(Tag)
    author = ForeignKey(Author, on_delete=CASCADE, default=None, null=True)
    created_at = DateTimeField(auto_now_add=True)
