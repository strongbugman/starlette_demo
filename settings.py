import os
import logging


DEBUG = os.getenv("DEBUG", "")
ENV = os.getenv("APP_ENV", "development")

PROJECT_NAME = "startlette_demo"
if ENV == "testing":
    PROJECT_NAME += "_test"
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)

DSN = ""
DB_URL = "postgres://postgres:letmein@localhost:5432/" + PROJECT_NAME
REDIS_URL = "redis://localhost"
CACHE_BACKEND = "memory"
CACHE_KWARGS = {}
AMQP_URL = "amqp://rabbit:letmein@localhost:5672"
AMQP_EXCHANGE = PROJECT_NAME + "_default"
AMQP_ROUTING_KEY = PROJECT_NAME + "_default"
AMQP_QUEUE = PROJECT_NAME + "_default"

STARCHART_TITLE = PROJECT_NAME
STARCHART_DESCRIPTION = "Api documents"
STARCHART_VERSION = "0.1"
STARCHART_OPENAPI_VERSION = "2.0"
STARCHART_UI_PATH = f"/{PROJECT_NAME}/apidocs/"
STARCHART_SCAHMA_PATH = f"/{PROJECT_NAME}/apidocs/schame/"
