import os
import logging
import typing


DEBUG = os.getenv("DEBUG", "")
ENV = os.getenv("APP_ENV", "development")

PROJECT_NAME = "{{cookiecutter.app_name}}"
if ENV == "testing":
    PROJECT_NAME += "_test"
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)

APIMAN = {"title": "{{cookiecutter.name}} API manual"}
DSN = ""
DB_URL = "postgres://postgres:letmein@localhost:5432/" + PROJECT_NAME
REDIS_URL = "redis://localhost"
CACHE_BACKEND = "memory"
CACHE_KWARGS: typing.Dict[str, typing.Any] = {}
AMQP_URL = "amqp://rabbit:letmein@localhost:5672"
AMQP_EXCHANGE = PROJECT_NAME + "_default"
AMQP_ROUTING_KEY = PROJECT_NAME + "_default"
AMQP_QUEUE = PROJECT_NAME + "_default"
