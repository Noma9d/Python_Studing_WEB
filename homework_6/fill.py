import sqlite3
from datetime import datetime, timedelta, date
from faker import Faker
from random import randint, choice


DISCIPLINES = ["math", "english", "Ukraine history", "programming", "drawing"]
GROUPS = ["TS-1301", "TP-1303", "TE-1302", "TA-1304"]
NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50

fake = Faker()
conn = sqlite3.connect("hw_6.db")
cur = conn.cursor()


def seed_teacher():
    teachers = [fake.name() for _ in range(NUMBER_TEACHERS)]
    sql = "INSERT INTO teachers(name) VALUES(?);"
    cur.executemany(
        sql,
        zip(
            teachers,
        ),
    )


def seed_disciplines():
    sql = "INSERT INTO items(name, id_teacher) VALUES(?, ?);"
    cur.executemany(
        sql,
        zip(
            DISCIPLINES,
            iter(randint(1, NUMBER_TEACHERS) for _ in range(len(DISCIPLINES))),
        ),
    )


def seed_groups():
    sql = "INSERT INTO groups(name) VALUES(?);"
    cur.executemany(
        sql,
        zip(
            GROUPS,
        ),
    )


def seed_students():
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    sql = "INSERT INTO students(name, id_group) VALUES(?, ?);"
    cur.executemany(
        sql, zip(students, iter(randint(1, len(GROUPS)) for _ in range(len(students))))
    )


def seed_grades():
    sql = "INSERT INTO grades(id_students, id_items, grade, created_at) VALUES(?, ?, ?, ?);"

    start_date = datetime.strptime("2013-09-01", "%Y-%m-%d")
    end_date = datetime.strptime("2014-06-15", "%Y-%m-%d")

    def list_date(start: date, end: date):
        res = []
        cur_date = start

        while cur_date <= end:
            if cur_date.isoweekday() < 6:
                res.append(cur_date)
            cur_date += timedelta(1)

        return res

    date_list = list_date(start_date, end_date)
    grades = []

    for day in date_list:
        random_item = randint(1, len(DISCIPLINES))
        random_student = [randint(1, NUMBER_STUDENTS) for _ in range(4)]
        for studet in random_student:
            grades.append((studet, random_item, randint(1, 12), day.date()))

    cur.executemany(sql, grades)


def main():
    try:
        seed_teacher()
        seed_disciplines()
        seed_groups()
        seed_students()
        seed_grades()
        conn.commit()
    except sqlite3.Error as error:
        print(error)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
