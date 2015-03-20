'''
Created: 20.03.2015
@author: Dennis Ligtenberg
Class to get a .csv file from a FTP server and read and process the containing data
'''
from ftplib import FTP
from StringIO import StringIO
import ext_config


class UpdateFogHeight(object):

    def get_file_from_ftp(self, url, user, password):
        '''
        Returns the most recent file from the FTP Server as StrinIO object
        '''
        ftp = FTP(url)
        ftp.login(user=user, passwd=password)
        filenames = []
        ftp.retrlines('NLST', filenames.append)
        ftp_file = StringIO()
        ftp.retrbinary("RETR " + filenames[-1], ftp_file.write)
        ftp.close()
        return ftp_file

    def csv_file_to_list(self, csv_file):
        '''
        Returns List of CSV lines
        '''
        data_list = []
        splitted = csv_file.getvalue().splitlines()
        for line in splitted[1:]:
            data_list.append(line.split(';'))

        return data_list

    def pressure_to_height(self, data_list):
        for line in data_list[:48]:
            print line
        return data_list

    def update(self):
        '''
        Update fog height
        '''
        csv_file = self.get_file_from_ftp(ext_config.FTP_URL, ext_config.FTP_USER, ext_config.FTP_PW)
        data_list = self.csv_file_to_list(csv_file)
        data_list = self.pressure_to_height(data_list)