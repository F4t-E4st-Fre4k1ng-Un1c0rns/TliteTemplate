from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", str_to_upper=True)

    hugging_face_access_token: str

settings = Settings()
