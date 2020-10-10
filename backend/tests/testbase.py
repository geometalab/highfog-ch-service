'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Setup for unit tests
'''
from flask_testing import TestCase
from webservice import app, db
from webservice.models import Height, Peak, PublicTransport
from io import BytesIO


class BaseTestCase(TestCase):
    '''
    Creates app for basic testing
    '''

    def create_app(self):
        '''
        Creates app with test config
        '''
        app.config.from_object('config.flask_config.TestConfig')
        return app


class DatabaseTestCase(BaseTestCase):
    '''
    Creates app with DB connection
    '''

    def setUp(self):
        '''
        Setup Database with all tables from model
        '''
        db.metadata.create_all(db.engine, tables=[
            Height.__table__,
            Peak.__table__,
            PublicTransport.__table__
        ])

    @staticmethod
    def get_test_file():
        '''
        Returns a BytesIO object of a sample CSV file with pressure data
        '''
        a = open("forecast_201503160900.csv", 'rb')
        testfile = BytesIO()
        testfile.write(a.read())
        a.close()
        return testfile

    def tearDown(self):
        '''
        Deletes the database
        '''
        db.session.remove()
        db.metadata.drop_all(db.engine, tables=[
            Height.__table__,
            Peak.__table__
        ])
