from os import getenv

EMPTY_STRING = str()

DATABASE_URL = getenv("DATABASE_URL", EMPTY_STRING)
