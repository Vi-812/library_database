import os
from dotenv import load_dotenv


load_dotenv()

django_secret_key = os.getenv('DJANGO_SECRET_KEY')
database_name = os.getenv('DATABASE_NAME')
database_username = os.getenv('DATABASE_USER')
database_password = os.getenv('DATABASE_PASSWORD')
database_host = os.getenv('DATABASE_HOST')
database_port = os.getenv('DATABASE_PORT')
