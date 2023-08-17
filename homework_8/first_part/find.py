from connect_db import url
from pymongo import MongoClient
from pprint import pprint
from redis_lru import RedisLRU
import redis


client = redis.StrictRedis(host="localhost", port="6379", password=None)
cache = RedisLRU(client)

client = MongoClient(url)
db = client.FirstMongoDB


@cache
def find_by_name(name: str) -> None:
    data = db.quotes.find({"author": name})
    result = []

    for el in data:
        result.append(el["quote"])

    return result


@cache
def find_by_tag(tag: str) -> None:
    data = db.quotes.find({"tags": tag})
    result = []

    for el in data:
        result.append(el["quote"])

    return result


@cache
def find_by_tags(tags_str: str) -> None:
    tags = tags_str.split(",")
    data = db.quotes.find({"tags": {"$in": tags}})
    result = []

    for el in data:
        result.append(el["quote"])

    return result


def main():
    while True:
        input_command = input("Input your command >>")
        data = input_command.split(":")

        match data[0]:
            case "name":
                res = find_by_name(data[1])
            case "tag":
                res = find_by_tag(data[1])
            case "tags":
                res = find_by_tags(data[1])
            case "exit":
                break

        pprint(res)


if __name__ == "__main__":
    main()
