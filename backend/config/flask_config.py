'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Configuration file containing app config and test config
'''
from config.ext_config import DATABASE_URL, TEST_DATABASE_URL


class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        DATABASE_URL
    )
    SQLALCHEMY_ECHO = False

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        TEST_DATABASE_URL
    )
    SQLALCHEMY_BINDS = {
        'internal': SQLALCHEMY_DATABASE_URI
    }
