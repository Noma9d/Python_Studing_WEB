from sql_model import Students, Grades, Groups, Teachers, Items, session
from sqlalchemy import func, desc, select, and_
from pprint import pprint
import json


def select_1(limit_student: int):
    # Найти 5 студентов с наибольшим средним баллом по всем предметам.
    result = (
        session.query(
            Students.name, func.round(func.avg(Grades.grade), 2).label("avg_grade")
        )
        .select_from(Grades)
        .join(Students)
        .group_by(Students.name)
        .order_by(desc("avg_grade"))
        .limit(limit_student)
        .all()
    )

    return result


def select_2(items_id: int):
    # Найти студента с наивысшим средним баллом по определенному предмету.
    result = (
        session.query(
            Items.name,
            Students.name,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Grades)
        .join(Students)
        .join(Items)
        .filter(Items.id == items_id)
        .group_by(Students.id, Items.name)
        .order_by(desc("avg_grade"))
        .limit(1)
        .all()
    )

    return result


def select_3(items_id: int):
    # Найти средний балл в группах по определенному предмету.
    resylt = (
        session.query(
            Items.name,
            Groups.name,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Grades)
        .join(Students)
        .join(Items)
        .join(Groups)
        .filter(Items.id == items_id)
        .group_by(Groups.name, Items.name)
        .order_by(desc("avg_grade"))
        .all()
    )

    return resylt


def select_4():
    # Найти средний балл на потоке (по всей таблице оценок).
    res = (
        session.query(func.round(func.avg(Grades.grade), 2).label("avg_grade"))
        .select_from(Grades)
        .all()
    )

    return res


def select_5(teacher_name: str):
    # Найти какие курсы читает определенный преподаватель.
    res = (
        session.query(Teachers.name, Items.name)
        .select_from(Items)
        .join(Teachers)
        .filter(Teachers.name == teacher_name)
        .all()
    )

    return res


def select_6(groups_name: str):
    # Найти список студентов в определенной группе.
    res = (
        session.query(
            Groups.name.label("group_name"), Students.name.label("student_name")
        )
        .select_from(Groups)
        .join(Students)
        .filter(Groups.name == groups_name)
        .group_by(Groups.name, Students.name)
        .all()
    )

    return res


def select_7(groups_name: str, items_name: str):
    # Найти оценки студентов в отдельной группе по определенному предмету.
    res = (
        session.query(
            Groups.name.label("groups_name"),
            Students.name.label("student_name"),
            Grades.grade.label("grades_name"),
            Items.name.label("items_name"),
        )
        .select_from(Groups)
        .join(Students)
        .join(Grades)
        .join(Items)
        .filter(and_(Groups.name == groups_name, Items.name == items_name))
        .all()
    )

    return res


def select_8(teachers_name: str):
    # Найти средний балл, который ставит определенный преподаватель по своим предметам.
    res = (
        session.query(
            Teachers.name.label("teacher_name"),
            Items.name.label("items_name"),
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Teachers)
        .join(Items)
        .join(Grades)
        .filter(Teachers.name == teachers_name)
        .group_by(Teachers.name, Items.name)
        .all()
    )

    return res


def select_9(student_name: str):
    # Найти список курсов, которые посещает определенный студент.
    res = (
        session.query(
            Students.name.label("student_name"), Items.name.label("items_name")
        )
        .select_from(Students)
        .join(Grades, Grades.id_student == Students.id)
        .join(Items, Grades.id_item == Items.id)
        .filter(Students.name == student_name)
        .group_by(Students.name, Items.name)
        .all()
    )

    return res


def select_10(student_name: str, teacher_name: str):
    # Список курсов, которые определенному студенту читает определенный преподаватель
    res = (
        session.query(
            Students.name.label("student_name"),
            Teachers.name.label("teacher_name"),
            Items.name.label("items_name"),
        )
        .select_from(Items)
        .join(Grades, Grades.id_item == Items.id)
        .join(Students, Students.id == Grades.id_student)
        .join(Teachers, Items.id_teacher == Teachers.id)
        .filter(and_(Students.name == student_name, Teachers.name == teacher_name))
        .order_by(Items.name)
        .all()
    )

    return res


def select_11(student_name: str, teacher_name: str):
    # Средний балл, который определенный преподаватель ставит определенному студенту.
    res = (
        session.query(
            Students.name.label("student_name"),
            Teachers.name.label("teacher_name"),
            Items.name.label("items_name"),
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Items)
        .join(Teachers, Items.id_teacher == Teachers.id)
        .join(Grades, Grades.id_item == Items.id)
        .join(Students, Students.id == Grades.id_student)
        .filter(and_(Students.name == student_name, Teachers.name == teacher_name))
        .group_by(Students.name, Teachers.name, Items.name)
        .all()
    )

    return res


def select_12(groups_name: str, items_name: str, grades_create_at: str):
    # Оценки студентов в определенной группе по определенному предмету на последнем занятии.
    res = (
        session.query(
            Groups.name.label("groups_name"),
            Students.name.label("student_name"),
            Grades.grade.label("grades_name"),
            Items.name.label("items_name"),
            Grades.crated_at,
        )
        .select_from(Groups)
        .join(Students)
        .join(Grades)
        .join(Items)
        .filter(
            and_(
                Groups.name == groups_name,
                Items.name == items_name,
                Grades.crated_at == grades_create_at,
            )
        )
        .all()
    )

    return res


def main():
    res = []

    res.append(select_1(5))
    res.append(select_2(5))
    res.append(select_3(5))
    res.append(select_4())
    res.append(select_5("Colin Anderson"))
    res.append(select_6("TE-1302"))
    res.append(select_7("TA-1304", "math"))
    res.append(select_8("Colin Anderson"))
    res.append(select_9("Edward Wilkins"))
    res.append(select_10("Edward Wilkins", "Colin Anderson"))
    res.append(select_11("Edward Wilkins", "Colin Anderson"))
    res.append(select_12("TP-1303", "Ukraine history", "2014-06-13"))

    json_res = {}
    count_select = 12

    for item, count in zip(res, range(1, count_select + 1)):
        res_dict = {f"select_{count}": str(item)}
        json_res.update(res_dict)

    with open("result.json", "w") as file:
        json.dump(json_res, file)

    return res


if __name__ == "__main__":
    main()
