from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_secret_key: str
    api_algorithm: str = "HS256"
    auth0_client_id: str
    auth0_client_secret: str
    auth0_domain: str
    api_access_token_expire_minutos: float = 10.0
    authorized_email: str

    model_config = SettingsConfigDict(validate_default=False, env_file=".env")


@lru_cache
def get_settings():
    return Settings()  # type: ignore


settings = get_settings()
print(settings.model_dump())
