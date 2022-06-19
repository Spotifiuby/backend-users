from pydantic import BaseSettings

class Settings(BaseSettings):
    BACKOFFICE_API_KEY: str = "1"
    NATIVE_APP_API_KEY: str = ""
    ENV: str = "Tests-"
    DB_USER: str = "uxbnywzimexjuw"
    DB_PWD: str = "360f3d5b31d27e8c9ce22ffbf7a42735808e42ef1805d9a2b77b6a32620af7bd"
    DB_HOST: str = "ec2-52-5-110-35.compute-1.amazonaws.com"
    DB_PORT: str = "5432"
    DB_NAME: str = "d28amjt0el1ome"
    PAYMENT_URL: str = "https://spotifiuby-payment-service.herokuapp.com"
