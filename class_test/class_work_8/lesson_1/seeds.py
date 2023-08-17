from models import Notes, Record, Tag
import connect

# сначала - создать объект Tag
tag = Tag(name="Purchases")
# потом - создание объектов Record
record1 = Record(description="Buying sausage")
record2 = Record(description="Buying milk")
record3 = Record(description="Buying oil")
#  Последнее, создаем объект Note и сохраняем его
Notes(
    name="Shopping",
    records=[record1, record2, record3],
    tags=[
        tag,
    ],
).save()

Notes(
    name="Going to the movies",
    records=[
        Record(description="Went to see the Avengers"),
    ],
    tags=[
        Tag(name="Fun"),
    ],
).save()
