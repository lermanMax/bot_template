from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env

TGBOT_TOKEN = os.getenv('TGBOT_TOKEN')
TGBOT_USERNAME = os.getenv('TGBOT_USERNAME')
TG_SUPERADMINS_ID = [int(i) for i in os.getenv('TG_SUPERADMINS_ID').split(',') if i]

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')
