import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///home_ease.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'personal_protected_key'
    SERVICER_FILE = os.path.join(os.getcwd(), 'static','servicer_file')