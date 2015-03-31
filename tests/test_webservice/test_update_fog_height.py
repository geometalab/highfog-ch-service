'''
Created: 20.03.2015
@author: Dennis Ligtenberg
'''
from webservice.testbase import DatabaseTestCase
from webservice.update_fog_height import UpdateFogHeight
from StringIO import StringIO
from datetime import datetime
from webservice.models import Heights, db
import ext_config


class UpdateFogHeightTest(DatabaseTestCase):


    @staticmethod
    def get_test_file():
        '''
        Returns a StringIO object of a sample CSV file with pressure data
        '''
        a = open("test_webservice/forecast_201503160900.csv")
        testfile = StringIO()
        testfile.write(a.read())
        a.close()
        return testfile

    def test_get_file_from_ftp(self):
        update = UpdateFogHeight()
        fog_file = update.get_file_from_ftp(ext_config.FTP_URL, ext_config.FTP_USER, ext_config.FTP_PW)

        self.assertTrue(fog_file)

    def test_csv_file_to_list(self):
        update = UpdateFogHeight()
        testfile = self.get_test_file()
        data = update.csv_file_to_list(testfile)

        self.assertTrue(isinstance(data, list))
        self.assertTrue('066100' in data[0])

    def test_pressure_to_height(self):
        update = UpdateFogHeight()
        testfile = self.get_test_file()
        data = update.csv_file_to_list(testfile)
        data = update.pressure_to_height(data)

        self.assertEqual(int(data[0][1]), 1017)
        self.assertEqual(type(data[0][0]), datetime)

    def test_update_database(self):
        update = UpdateFogHeight()
        testfile = self.get_test_file()
        data = update.csv_file_to_list(testfile)
        data = update.pressure_to_height(data)
        update.update_database(data)

        self.assertEquals(db.session.query(Heights).count(), 48)
        self.assertEquals(db.session.query(Heights).all()[0].height, 1017.48886368041)

        update.update_database(data)
        self.assertEquals(db.session.query(Heights).count(), 48)