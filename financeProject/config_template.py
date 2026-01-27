"""
Configuration template.
Copy this file to config.py and fill in real values.
"""

DB_CONFIG = {
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": 3306,
    "database": "your_database",
    "charset": "utf8mb4",
}

MYSQL_HOST = DB_CONFIG["host"]
MYSQL_PORT = DB_CONFIG["port"]
MYSQL_USER = DB_CONFIG["user"]
MYSQL_PASSWORD = DB_CONFIG["password"]
MYSQL_DATABASE = DB_CONFIG["database"]

SECRET_KEY = "please_change_me_to_random_string"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_DAYS = 7
