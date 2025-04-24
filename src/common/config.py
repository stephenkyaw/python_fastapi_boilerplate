import os
from dotenv import load_dotenv

load_dotenv()

class AppSettings:
    APP_NAME = os.getenv("APP_NAME", "MyApp")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

