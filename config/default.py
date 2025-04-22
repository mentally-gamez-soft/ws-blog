"""Define the default configuration to load for the application."""

from os.path import abspath, dirname, join

# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

# Media dir
MEDIA_DIR = join(BASE_DIR, "media")
POSTS_IMAGES_DIR = join(MEDIA_DIR, "posts")

SECRET_KEY = "Th1S-Iz.My-5uP3r_seCRE7#k"  # nosec
SQLALCHEMY_TRACK_MODIFICATIONS = False

# App environments
APP_ENV_LOCAL = "local"
APP_ENV_TESTING = "testing"
APP_ENV_DEVELOPMENT = "development"
APP_ENV_STAGING = "staging"
APP_ENV_PRODUCTION = "production"
APP_ENV = ""

# Configuración del email
MAIL_SERVER = "tu servidor smtp"
MAIL_PORT = 587
MAIL_USERNAME = "tu correo"  # nosec
MAIL_PASSWORD = "tu contrasena"  # nosec
DONT_REPLY_FROM_EMAIL = "(admin,admin.app@myflaskapp.com)"  # nosec
ADMINS = ("admin.app@myflaskapp.com",)
MAIL_USE_TLS = True
MAIL_DEBUG = False
ITEMS_PER_PAGE = 12
