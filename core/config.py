from pydantic_settings import BaseSettings
import os 
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    DB_URL: str  = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")
    MEXC_API_KEY: str = os.getenv("MEXC_API_KEY")
    MEXC_SECRET_KEY: str = os.getenv("MEXC_SECRET_KEY")
    COINMARKETCAP_API_KEY: str = os.getenv("COINMARKETCAP_API_KEY")
    BINGX_API_KEY: str = os.getenv("BINGX_API_KEY")
    BINGX_SECRET_KEY: str = os.getenv("BINGX_SECRET_KEY")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")


    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_URL}:{self.DB_PORT}/{self.DB_NAME}"

    
    class Config:
        env_file = ".env"

settings = Settings()
