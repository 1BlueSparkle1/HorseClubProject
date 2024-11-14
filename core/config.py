from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent


# DB_PATH = BASE_DIR / "db.sqlite3"
#
#
# class DbSettings(BaseModel):
#
#
#     url: str = f""
#     echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_days: int = 30
    access_token_expire_minutes: int = 30


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url_asyncpg(self):
        # return f"postgresql+asyncpg://testUser:1234@localhost:5432/postgres"
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    # db: DbSettings = DbSettings()
    db_echo: bool = False

    auth_jwt: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
