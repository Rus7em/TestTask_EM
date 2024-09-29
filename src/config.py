import os 

DB_USERNAME = os.getenv("DB_USERNAME","project")
DB_PASSWORD = os.getenv("DB_PASSWORD", "project")
DB_NAME = os.getenv("DB_NAME", "project")
DB_HOST = os.getenv("DB_HOST", "0.0.0.0:5432")
