import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Secret key for session security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'

    # SQLite database stored in instance/library.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'instance', 'library.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False