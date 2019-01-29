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

STARCHART_TITLE = PROJECT_NAME
STARCHART_DESCRIPTION = "Api documents"
STARCHART_VERSION = "0.1"
STARCHART_OPENAPI_VERSION = "2.0"
STARCHART_UI_PATH = f"/{PROJECT_NAME}/apidocs/"
STARCHART_SCAHMA_PATH = f"/{PROJECT_NAME}/apidocs/schame/"
