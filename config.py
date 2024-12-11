import sys
import os
from dotenv import load_dotenv
from pathlib import Path



sys.stdout.reconfigure(encoding='utf-8')


# مسیر فایل .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# بارگذاری متغیرها
BOT_TOKEN = os.getenv('BOT_TOKEN')
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
REGISTRATION_PASSWORD = os.getenv('REGISTRATION_PASSWORD')
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')

# بررسی وجود متغیرها (اختیاری)
required_vars = ['BOT_TOKEN', 'TRELLO_API_KEY', 'TRELLO_TOKEN', 'REGISTRATION_PASSWORD', 'MONGO_URI']
missing_vars = [var for var in required_vars if os.getenv(var) is None]

if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
