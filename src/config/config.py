import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

API_CONFIG = {
    'key': os.getenv('API_KEY'),
    'url': os.getenv('API_URL'),
    'base_currency': os.getenv('API_BASE_CURRENCY'),
}

APP_CONFIG = {
    'schedule_time': '06:00',
    'log_format': '%(asctime)s - %(levelname)s - %(message)s',
    'log_level': 'INFO'
} 

