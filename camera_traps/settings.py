from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global Settings"""

    # Postgres.
    DB_USER: str
    """user"""
    DB_PASSWORD: str
    """passw"""
    DB_HOST: str
    """database host"""
    DB_PORT: str
    """database port"""
    DB_NAME: str
    """database name"""

    # Storage.
    S3_ENDPOINT_URL: str
    """endpoint url"""


S = Settings()  # type: ignore
