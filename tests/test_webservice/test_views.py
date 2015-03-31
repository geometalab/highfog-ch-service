'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Unittests for views
'''
from webservice.testbase import DatabaseTestCase
from webservice.models import Heights, db
from webservice.update_fog_height import UpdateFogHeight


class TestViews(DatabaseTestCase):

    def test_update(self):
        update = UpdateFogHeight()
        testfile = self.get_test_file()
        data = update.csv_file_to_list(testfile)
        data = update.pressure_to_height(data)
        update.update_database(data)
        old_date = db.session.query(Heights).first().date

        self.client.get('/v1/update')
        self.assertTrue(db.session.query(Heights).first().date != old_date)

    def test_get_heights(self):
        update = UpdateFogHeight()
        testfile = self.get_test_file()
        data = update.csv_file_to_list(testfile)
        data = update.pressure_to_height(data)
        update.update_database(data)

        response = self.client.get('/v1/get_heights').json
        self.assertEqual(response['heights'][0]['height'], 1017.48886368041)