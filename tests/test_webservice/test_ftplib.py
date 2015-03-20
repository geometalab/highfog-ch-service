'''
Created: 20.03.2015
@author: Dennis Ligtenberg
'''
from webservice.testbase import DatabaseTestCase
from webservice.update_fog_height import UpdateFogHeight
import ext_config


class UpdateFogHeightTest(DatabaseTestCase):

    def test_get_file_from_ftp(self):
        '''
        Tests if a file is received
        '''
        update = UpdateFogHeight()
        fog_file = update.get_file_from_ftp(ext_config.FTP_URL, ext_config.FTP_USER, ext_config.FTP_PW)
        self.assertTrue(fog_file)

    def test_csv_file_to_list(self):
        '''
        Tests if  is csv to list conversion works properly
        '''
        update = UpdateFogHeight()
        fog_file = update.get_file_from_ftp(ext_config.FTP_URL, ext_config.FTP_USER, ext_config.FTP_PW)
        data = update.csv_file_to_list(fog_file)
        self.assertTrue(isinstance(data, list))