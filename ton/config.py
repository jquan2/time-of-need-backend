import os

DATABASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATABASE_FILE = "local.db"
DATABASE_PATH = os.path.join(DATABASE_DIR, DATABASE_FILE)
SQLALCHEMY_DATABASE_URI = 'sqlite:///{db_path}'.format(db_path=DATABASE_PATH)

SECRET_KEY = '384509348'

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "VT37z1fKuEpc06Nlmkj0E32B7PWo"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False
