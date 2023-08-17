import sqlite3


def create_db():
    with open("salary.sql", "r") as file:
        sql = file.read()

    with sqlite3.connect("salary.db") as con:
        cur = con.cursor()
        cur = con.executescript(sql)


if __name__ == "__main__":
    create_db()
