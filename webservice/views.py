'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Views for request handling
'''
from flask import Blueprint, jsonify, request, abort
from update_fog_height import UpdateFogHeight
from crossdomain import crossdomain
from query_issuer import pois_at_time, get_heights, stops_within_bounds, height_by_time
from datetime import datetime

webservice = Blueprint("webservice", __name__)


@webservice.route('/v1/')
def index():
    return 'Welcome to the highfog webservice!'


@webservice.route('/v1/update')
@crossdomain(origin='*')
def update():
    UpdateFogHeight().update()
    return 'Data Updated'


@webservice.route('/v1/heights')
@crossdomain(origin='*')
def heights():
    return jsonify(heights=get_heights())


@webservice.route('/v1/pois/')
@crossdomain(origin='*')
def get_pois():
    try:
        year = request.args.get('y')
        month = request.args.get('m')
        day = request.args.get('d')
        hour = request.args.get('h')
        timestamp = datetime.strptime(year + "-" + month + "-" + day + " " + hour, '%Y-%m-%d %H')
    except TypeError:
        abort(400)

    pois = pois_at_time(timestamp)
    return jsonify(pois)


@webservice.route('/v1/public_transport/')
@crossdomain(origin='*')
def public_transport():
    # Dict with Bounds (minx, miny, maxx, maxy from the GET parameters)
    try:
        year = request.args.get('y')
        month = request.args.get('m')
        day = request.args.get('d')
        hour = request.args.get('h')
        timestamp = datetime.strptime(year + "-" + month + "-" + day + " " + hour, '%Y-%m-%d %H')

        bounds = {
            'minx': float(request.args.get('minx')),
            'miny': float(request.args.get('miny')),
            'maxx': float(request.args.get('maxx')),
            'maxy': float(request.args.get('maxy'))
        }
    except TypeError:
        abort(400)

    stops = stops_within_bounds(bounds, timestamp)
    return jsonify(stops)


@webservice.route('/v1/height_at_time/')
@crossdomain(origin='*')
def height_at_time():
    try:
        year = request.args.get('y')
        month = request.args.get('m')
        day = request.args.get('d')
        hour = request.args.get('h')
    except TypeError:
        abort(400)

    timestamp = datetime.strptime(year + "-" + month + "-" + day + " " + hour, '%Y-%m-%d %H')
    return jsonify({'height': height_by_time(timestamp)})