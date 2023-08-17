from sql_model import session, Teachers, Students, Items, Groups, Grades
from seed import NUMBER_TEACHERS, GROUPS, students, DISCIPLINES
from random import randint


def model_name(model_name: str):
    models = {
        "Groups": Groups,
        "Grades": Grades,
        "Students": Students,
        "Teachers": Teachers,
        "Items": Items,
    }

    if model_name in models:
        return models[model_name]
    else:
        raise ValueError(f"You input incorect table_name: {model_name}")


def create_teacher(name: str):
    data = Teachers(name=name)
    session.add(data)
    session.commit()
    session.close()
    NUMBER_TEACHERS += 1

    return f"You create teacher with name: {name}"


def create_student(name: str):
    id_group = iter(randint(1, len(GROUPS)) for _ in range(len(students)))
    data = Students(name=name, id_group=id_group)
    session.add(data)
    session.commit()
    session.close()

    return f"You create student with name: {name} and id_group: {id_group}"


def create_group(name: str):
    data = Groups(name=name)
    session.add(data)
    session.commit()
    session.close()

    return f"You create group with name: {name}"


def create_item(name: str):
    DISCIPLINES.append(name)
    teacher_id = iter(randint(1, NUMBER_TEACHERS) for _ in range(len(DISCIPLINES)))
    data = Items(name=name, id_teacher=teacher_id)
    session.add(data)
    session.commit()
    session.close()

    return f"You create item: {name}, with teacher_id: {teacher_id}"


def create_grades():
    raise NotImplementedError


def list(table_name: str):
    model = model_name(table_name)

    res = session.query(model).select_from(model).all()

    return res


def update_table(table_name: str, id: int, field: str | int):
    model = model_name(table_name)
    data = session.query(model).get(id)

    if data and model == "Grades":
        data.grade = field
        session.commit()
        session.close()
    elif data:
        data.name = field
        session.commit()
        session.close()
    else:
        print(f"Field: {field} with id: {id} in table: {table_name} not found")

    return f"You update field: {field} with id: {id} in table: {table_name}"


def remove_data(table_name: str, id: int):
    model = model_name(table_name)
    data = session.query(model).filter(model.id == id).delete()
    session.commit()
    session.close()

    return f"Delete data: {data} in table: {table_name}"


CRUD_OPERATIO = {
    "create_student": create_student,
    "create_grade": create_grades,
    "create_group": create_group,
    "create_item": create_item,
    "create_teacher": create_teacher,
    "list": list,
    "update": update_table,
    "remove": remove_data,
}
