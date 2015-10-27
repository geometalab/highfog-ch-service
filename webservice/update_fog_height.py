'''
Created: 20.03.2015
@author: Dennis Ligtenberg
Class to get a .csv file from a FTP server and read and process the containing data
'''
from ftplib import FTP
from StringIO import StringIO
import math
from datetime import datetime

from config import ext_config
from models import Height, db


class UpdateFogHeightForecast(object):

    @staticmethod
    def get_file_from_ftp(url, user, password):
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

    @staticmethod
    def convert_csv_file_to_list(csv_file):
        '''
        Returns List of CSV lines
        '''
        data_list = [line.split(';') for line in csv_file.getvalue().splitlines()[1:]]
        return data_list

    @staticmethod
    def pressure_to_height(result_list):
        '''
        Returns the actual heights and dates into a list
        The height is calculated with a formula according to Courvoisier
        '''
        processed_data = []
        for i, line in enumerate(result_list[:48]):
            date = datetime.strptime(line[1] + ' ' + line[2], "%Y-%m-%d %H:%M")
            fog_height = 433*(1+math.exp(1)**(-0.3*(float(line[3]) - float(result_list[i+48][3]))))
            processed_data.append([date, fog_height])
        return processed_data

    @staticmethod
    def update_database(calculated_result_list):
        '''
        Deletes old entries and enters new data in the DB
        '''
        db.session.query(Height).delete()
        for row in calculated_result_list:
            new_entry = Height(
                height=row[1],
                date=row[0]
            )
            db.session.add(new_entry)
            db.session.commit()

    def update(self):
        '''
        Update fog height
        '''
        csv_file = self.get_file_from_ftp(ext_config.FTP_URL, ext_config.FTP_USER, ext_config.FTP_PW)
        result_list = self.convert_csv_file_to_list(csv_file)
        calculated_result_list = self.pressure_to_height(result_list)
        self.update_database(calculated_result_list)
