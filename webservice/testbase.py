'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Setup for unit tests
'''
from flask_testing import TestCase
from . import app, db
from models import Heights


class BaseTestCase(TestCase):
    '''
    Creates app for basic testing
    '''

    def create_app(self):
        '''
        Creates app with test config
        '''
        app.config.from_object('config.TestConfig')
        return app

class DatabaseTestCase(TestCase):
    '''
    Creates app with DB connection
    '''
    def create_app(self):
        '''
        Creates app with test config
        '''
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        '''
        Setup Database with all tables from model
        '''
        db.metadata.create_all(db.engine, tables=[
            Heights.__table__
        ])

    def tearDown(self):
        '''
        Deletes the database
        '''
        db.session.remove()
        db.metadata.drop_all(db.engine, tables=[
            Heights.__table__
        ])