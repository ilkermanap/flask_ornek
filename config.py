import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '55cc5c007adc16f1c072294a0806e9a303e720fb6024b3a7423873aa8cc46d33'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_DATABASE_URI = 'postgresql://username:passwd@localhost:5432/dbname'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMINS=["ilkermanap@gmail.com"]
    LANGUAGES = {"en": "English", "tr":"Turkish"}
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PASSWORD='xxxxxxxxx'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False
    MAIL_USERNAME="ilkermanap@gmail.com"
