'''
Created: 08.04.2015
@author: Dennis Ligtenberg
'''
from tests.testbase import DatabaseTestCase
from webservice.query_issuer import get_heights, height_by_time
from webservice.update_fog_height import UpdateFogHeight
from datetime import datetime


class TestQueryIssuer(DatabaseTestCase):

    def fill_db_with_pois(self):
        update = UpdateFogHeight()
        testfile = self.get_test_file()
        data = update.csv_file_to_list(testfile)
        data = update.pressure_to_height(data)
        update.update_database(data)

    def test_get_heights(self):
        self.fill_db_with_pois()
        heights = get_heights()
        self.assertEqual(heights[0]['height'], 1017.48886368041)

    def test_height_by_time(self):
        self.fill_db_with_pois()
        date = datetime.strptime("2015-03-16 00:00", "%Y-%m-%d %H:%M")
        res = height_by_time(date)
        self.assertEqual(res, 1017.48886368041)