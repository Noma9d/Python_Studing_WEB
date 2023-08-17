import configparser
from mongoengine import connect


config = configparser.ConfigParser()
config.read("config.ini")
user = config.get("DB", "USER")
password = config.get("DB", "password")
domain = config.get("DB", "domain")
db_name = config.get("DB", "db_name")

url = f"mongodb+srv://{user}:{password}@{domain}/{db_name}?retryWrites=true&w=majority"

conn = connect(host=url, ssl=True)
