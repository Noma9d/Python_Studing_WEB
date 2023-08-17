from argparse import ArgumentParser
from CRUD import CRUD_OPERATIO


parser = ArgumentParser()
parser.add_argument(
    "-a", "--action", dest="action", help="Command: create, list, update, remove"
)
parser.add_argument("-m", "--model", dest="model")
parser.add_argument("--id", dest="id")
parser.add_argument("-n", "--name", dest="name")
parser.add_argument("-g", "--grade", dest="grade")

arg = parser.parse_args()


def main():
    match arg.action:
        case "remove":
            CRUD_OPERATIO["remove"](arg.model, arg.id)
        case "update" if arg.grade is None:
            CRUD_OPERATIO["update"](arg.module, arg.id, arg.name)
        case "update" if arg.grade:
            CRUD_OPERATIO["update"](arg.module, arg.id, arg.grade)
        case "action" if arg.model == "Teacher":
            CRUD_OPERATIO["create_teacher"](arg.name)
        case "action" if arg.model == "Student":
            CRUD_OPERATIO["create_student"](arg.name)
        case "action" if arg.model == "Grade":
            CRUD_OPERATIO["create_grade"](arg.name)
        case "action" if arg.model == "Item":
            CRUD_OPERATIO["create_item"](arg.name)
        case "action" if arg.model == "Group":
            CRUD_OPERATIO["create_group"](arg.name)


if __name__ == "__main__":
    main()
