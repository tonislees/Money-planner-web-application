import os


class Config:
    SECRET_KEY = 'xXK2A@7!Rq&PUjZ&$*k4G9'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "site.db")}'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "rahaleht@gmail.com"
    MAIL_PASSWORD = "knvicrdgwtjqhdup"