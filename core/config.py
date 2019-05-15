import os


class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SECRET_KEY = os.getenv('SECRET_KEY')