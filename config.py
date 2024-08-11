import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
MAX_FILE_SIZE_MB = 4096  # 4 GB in MB
LOG_FILE = 'logs/user_logs.txt'
