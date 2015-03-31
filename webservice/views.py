'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Views for request handling
'''
from flask import Blueprint, jsonify
from update_fog_height import UpdateFogHeight
from models import Heights, db

webservice = Blueprint("webservice", __name__)


@webservice.route('/v1/')
def index():
    hello = {'Hello': 'world!'}
    return jsonify(hello)


@webservice.route('/v1/fogmap')
def fogmap():
    return jsonify({'Fog': 'Here', 'NoFog': 'There'})


@webservice.route('/v1/update')
def update():
    UpdateFogHeight().update()
    return 'Data Updated'


@webservice.route('/v1/get_heights')
def get_heights():
    heights = []
    query = db.session.query(Heights).all()
    for entry in query:
        heights.append({'height': entry.height, 'date': entry.date})
    return jsonify(heights=heights)