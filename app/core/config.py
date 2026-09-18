import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "wh_portal")

    secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")
    algorithm = "HS256"
    access_token_expire_minutes = 15
    refresh_token_expire_days = 7


settings = Settings()
