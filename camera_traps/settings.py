from pydantic_settings import BaseSettings

SITES = {
    "0": {"name": "0", "lat": 44.6337, "lon": 9.7314},
    "1": {"name": "1", "lat": 44.6347, "lon": 9.7311},
}


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
