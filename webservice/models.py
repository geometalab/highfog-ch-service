'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Models for DB OR mapping
'''

from data import db

db = db


class TestTable(db.Model):
    __tablename__ = 'test'
    __bind_key__ = 'internal'

    id = db.Column(db.Integer, primary_key=True)
    test = db.Column(db.String(100))