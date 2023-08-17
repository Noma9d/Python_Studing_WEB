from models import Author, Quotes
import json
from connect_db import conn


def main():
    with open("authors.json", "r") as author:
        author_data = json.load(author)

    with open("quotes.json", "r") as file:
        quotes_data = json.load(file)

    for el in author_data:
        Author(
            fullname=el["fullname"],
            born_date=el["born_date"],
            born_location=el["born_location"],
            description=el["description"],
        ).save()

    for el in quotes_data:
        Quotes(tags=el["tags"], author=el["author"], quote=el["quote"]).save()


if __name__ == "__main__":
    conn
    main()
