'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Configuration file containing app config and test config
'''


class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        'postgresql://hochnebelkarte:hochnebelkarte@localhost:5434/hochnebelkarte'
    )
    SQLALCHEMY_ECHO = False


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        'postgresql://hochnebelkarte:hochnebelkarte@localhost:5434/tester'
    )
    SQLALCHEMY_BINDS = {
        'internal': SQLALCHEMY_DATABASE_URI
    }