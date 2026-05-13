import os

DB_HOST     = os.environ.get("DB_HOST", "localhost")
DB_USER     = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "Admin1234!")
DB_NAME     = os.environ.get("DB_NAME", "appdb")
