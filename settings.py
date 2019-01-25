import os


DEBUG = os.getenv("DEBUG", "")
ENV = os.getenv("APP_ENV", "development")

PROJECT_NAME = "startlette_demo"
if ENV == "testing":
    PROJECT_NAME += "_test"

DSN = ""
DB_URL = "postgres://postgres:letmein@localhost:5432/" + PROJECT_NAME
REDIS_URL = "redis://localhost"
CACHE_BACKEND = "memory"
CACHE_KWARGS = {}

STAGGER_TITLE = PROJECT_NAME
STAGGER_DESCRIPTION = "Api documents"
STAGGER_VERSION = "0.1"
STAGGER_OPENAPI_VERSION = "2.0"
STAGGER_UI_PATH = f"/{PROJECT_NAME}/apidocs/"
STAGGER_SCAHMA_PATH = f"/{PROJECT_NAME}/apidocs/schame/"
STAGGER_UI_INDEX_FILE = "./app/static/index.html"
