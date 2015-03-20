'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Views for request handling
'''
from flask import Blueprint, jsonify
from models import db, TestTable

web_service = Blueprint("webservice", __name__)


@web_service.route('/v1/')
def hello_world():
    query1 = db.session.query(TestTable).all()[0].test
    query2 = db.session.query(TestTable).all()[1].test
    hello = {query1: query2}
    return jsonify(hello)

@web_service.route('/v1/fogmap')
def fogmap():
    return jsonify({'Fog': 'Here', 'NoFog': 'There'})