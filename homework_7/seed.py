from faker import Faker
from random import randint
from sql_model import Groups, Grades, Teachers, Students, Items, session
from datetime import date, datetime, timedelta


fake = Faker()

DISCIPLINES = ["math", "english", "Ukraine history", "programming", "drawing"]
GROUPS = ["TS-1301", "TP-1303", "TE-1302", "TA-1304"]
NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50
teachers = [fake.name() for _ in range(NUMBER_TEACHERS)]
students = [fake.name() for _ in range(NUMBER_STUDENTS)]


def list_grades(items, number_students):
    grades = []
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

    for day in date_list:
        random_item = randint(1, len(items))
        random_student = [randint(1, number_students) for _ in range(4)]
        for studet in random_student:
            grades.append((studet, random_item, randint(1, 12), day.date()))

    return grades


grades = list_grades(DISCIPLINES, NUMBER_STUDENTS)

if __name__ == "__main__":
    for group in GROUPS:
        gr = Groups(name=group)
        session.add(gr)

    for student, group_id in zip(
        students, iter(randint(1, len(GROUPS)) for _ in range(len(students)))
    ):
        st = Students(name=student, id_group=group_id)
        session.add(st)

    for teacher in teachers:
        te = Teachers(name=teacher)
        session.add(te)

    for item, teacher_id in zip(
        DISCIPLINES, iter(randint(1, NUMBER_TEACHERS) for _ in range(len(DISCIPLINES)))
    ):
        it = Items(name=item, id_teacher=teacher_id)
        session.add(it)

    for item in grades:
        id_student, id_item, grade, date_create = item
        grad = Grades(
            id_student=id_student, id_item=id_item, grade=grade, crated_at=date_create
        )
        session.add(grad)

    session.commit()
