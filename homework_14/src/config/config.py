from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "sqlite:///./test.db"
    secret_key: str = "my_secret_key"
    algorithm: str = "HS256"
    mail_username: str = "example@gmail.com"
    mail_password: str = "123456789"
    mail_from: str = "example@meta.ua"
    mail_port: int = "587"
    mail_server: str = "smtp.yourmailserver.com"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: int = "123456789"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
