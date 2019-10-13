import os

SECRET_KEY = os.getenv('SECRET_KEY', 'appu chesi pappu koodu')
DEBUG = os.getenv('DEBUG', 'true').lower() == "true"
