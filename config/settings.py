import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-123')
    OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
    SITE_URL = os.environ.get('SITE_URL', '')
    SITE_NAME = os.environ.get('SITE_NAME', '')
    
    # Define and create data directory for Pandas storage
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(DATA_DIR, exist_ok=True)
