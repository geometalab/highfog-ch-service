'''
Created: 20.03.2015
@author: Dennis Ligtenberg
Class to get a .csv file from a FTP server and read and process the containing data
'''
from ftplib import FTP
from StringIO import StringIO
import math
import ext_config
from datetime import datetime
from models import Heights, db


class UpdateFogHeight(object):

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
    def csv_file_to_list(csv_file):
        '''
        Returns List of CSV lines
        '''
        data_list = []
        splitted = csv_file.getvalue().splitlines()
        for line in splitted[1:]:
            data_list.append(line.split(';'))

        return data_list

    @staticmethod
    def pressure_to_height(data_list):
        '''
        Returns the actual heights and dates into a list
        The height is calculated with a formula according to Courvoisier
        '''
        processed_data = []
        for i, line in enumerate(data_list[:48]):
            date = datetime.strptime(line[1] + ' ' + line[2], "%Y-%m-%d %H:%M")
            fog_height = 433*(1+math.exp(1)**(-0.3*(float(line[3]) - float(data_list[i+48][3]))))
            processed_data.append([date, fog_height])
        return processed_data

    @staticmethod
    def update_database(data_list):
        '''
        Deletes old entries and enters new data in the DB
        '''
        db.session.query(Heights).delete()
        for row in data_list:
            new_entry = Heights(
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
        data_list = self.csv_file_to_list(csv_file)
        data_list = self.pressure_to_height(data_list)
        self.update_database(data_list)