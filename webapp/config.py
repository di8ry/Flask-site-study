import os
from datetime import timedelta


WEATHER_DEFAULT_CITY = 'China,Beijing'
WEATHER_APY_KEY = '50027f868a9842088fe150322221109'

basedir = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
SECRET_KEY = 'Woaini123!'
SQLALCHEMY_TRACK_MODIFICATIONS = False

REMEMBER_COOKIE_DURATION = timedelta(days=30)