import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("APP_CONFIG_KEY", "dev-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///movies_base.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = os.path.join(os.getcwd(), ".flask_session")
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True


    TMDB_BEARER = os.getenv("TMDB_BEARER", "")
    NEWS_URL = "https://screenrant.com/movie-news/"


    MY_EMAIL = os.getenv("MY_EMAIL", "")
    PASSWORD = os.getenv("PASSWORD", "")


    HTTP_HEADER = {
        "Accept-Language": "en-GB",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    }
