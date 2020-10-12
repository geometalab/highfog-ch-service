'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Unittests for views
'''
from tests.testbase import DatabaseTestCase
from webservice.models import Height, db
from webservice.update_fog_height import UpdateFogHeightForecast
from config import api_config


class TestViews(DatabaseTestCase):
    '''
    Tests for views of the webservice
    '''

    def test_update_view(self):
        update = UpdateFogHeightForecast()
        testfile = self.get_test_file()
        data = update.convert_csv_file_to_list(testfile)
        data = update.pressure_to_height(data)
        update.update_database(data)
        old_date = db.session.query(Height).first().date

        self.client.get('/v1/update')
        self.assertTrue(db.session.query(Height).first().date != old_date)

    def test_heights_view(self):
        update = UpdateFogHeightForecast()
        testfile = self.get_test_file()
        data = update.convert_csv_file_to_list(testfile)
        data = update.pressure_to_height(data)
        update.update_database(data)

        response = self.client.get('/v1/heights').json
        self.assertAlmostEqual(
            response['heights'][0]['height'], 1017.48886368041, places=6)

    def test_peaks_view(self):
        update = UpdateFogHeightForecast()
        update.update()
        url = api_config.FORECASTED_PEAKS_URL + '?height=1000'
        response = self.client.get(url).json
        self.assertEqual(response['type'], 'FeatureCollection')

    def test_public_transport_view(self):
        update = UpdateFogHeightForecast()
        update.update()
        url = api_config.FORECASTED_PUBLIC_TRANSPORT_URL + '' \
                                                           '?minx=874586.691776&miny=5935368.32345' \
                                                           '&maxx=1053008.39186&maxy=6065208.87423&height=1000'
        response = self.client.get(url).json
        self.assertEqual(response['type'], 'FeatureCollection')
