from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from fastapi.security import OAuth2PasswordBearer


class Settings(BaseSettings):
    # --- declare the fields you expect from .env ---
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    env: str = "dev"
    cors_origins: list[str] = []

    # read from .env in the project root
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # allow CORS_ORIGINS to be given as a comma-separated string in .env
    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_cors(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        if v is None:
            return []
        return list(v)

# create a global Settings instance to import elsewhere
settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
