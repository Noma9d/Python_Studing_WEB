import configparser
import pathlib


file_config = pathlib.Path(__file__).parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get("DB", "user")
password = config.get("DB", "password")
domain = config.get("DB", "domain")
db_name = config.get("DB", "db_name")
port = config.get("DB", "port")
