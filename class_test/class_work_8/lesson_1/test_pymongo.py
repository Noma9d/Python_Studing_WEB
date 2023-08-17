from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient("")

db = client.book

# res = db.cats.insert_one(
#     {
#         "name": "Murzik",
#         "age": 10,
#         "gender": "male",
#     }
# )

# print(res.inserted_id)

# res_many = db.cats.insert_many(
#     [
#         {"name": "Nata", "age": 5, "gender": "female"},
#         {"name": "Bars", "age": 9, "gender": "male"},
#     ]
# )

# print(res_many.inserted_ids)

# result = db.cats.find_one({"_id": ObjectId("64d25a41448e024189b9bc8c")})
# db.cats.update_one({'name':'Bars'}, {'$set':{'age':6}})
db.cats.delete_one({"name": "Murzik"})
result = db.cats.find({})

for el in result:
    print(el)
