from pydantic import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = ""
    ENV: str = "Tests"
    DB_USER: str = "bauti"
    DB_PWD: str = "pass"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "usersdb"