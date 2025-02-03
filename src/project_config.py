import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "")
    port = os.environ.get("DB_PORT", 0)
    password = os.environ.get("DB_PASSWORD", "")
    user, db_name = "postgres", ""
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
