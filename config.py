import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ['WTF_CSRF_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'flask_crops_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['el', 'en']  # Support Greek and English language