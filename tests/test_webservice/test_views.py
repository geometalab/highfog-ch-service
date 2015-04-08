'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Unittests for views
'''
from tests.testbase import DatabaseTestCase
from webservice.models import Heights, db
from webservice.update_fog_height import UpdateFogHeight


class TestViews(DatabaseTestCase):
    '''
    Tests for views of the webservice
    '''

    def test_update(self):
        update = UpdateFogHeight()
        testfile = self.get_test_file()
        data = update.csv_file_to_list(testfile)
        data = update.pressure_to_height(data)
        update.update_database(data)
        old_date = db.session.query(Heights).first().date

        self.client.get('/v1/update')
        self.assertTrue(db.session.query(Heights).first().date != old_date)

    def test_heights(self):
        update = UpdateFogHeight()
        testfile = self.get_test_file()
        data = update.csv_file_to_list(testfile)
        data = update.pressure_to_height(data)
        update.update_database(data)

        response = self.client.get('/v1/heights').json
        self.assertEqual(response['heights'][0]['height'], 1017.48886368041)

    def test_pois(self):
        url = '/v1/pois/?minx=874586.691776&miny=5935368.32345&maxx=1053008.39186&maxy=6065208.87423'
        response = self.client.get(url).json
        print response
        self.assertEqual(response['type'], 'FeatureCollection')