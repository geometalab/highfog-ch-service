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


@webservice.route('/v1/update')
@crossdomain(origin='*')
def update():
    UpdateFogHeight().update()
    return 'Data Updated'


@webservice.route('/v1/height_at_point')
@crossdomain(origin='*')
def height_at_point():
    x = request.args.get('x')
    y = request.args.get('y')
    return '1'

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
        pois = pois_at_time(timestamp)
        return jsonify(pois)
    except TypeError:
        abort(400)


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
        stops = stops_within_bounds(bounds, timestamp)
        return jsonify(stops)
    except TypeError:
        abort(400)


@webservice.route('/v1/height_at_time/')
@crossdomain(origin='*')
def height_at_time():
    try:
        year = request.args.get('y')
        month = request.args.get('m')
        day = request.args.get('d')
        hour = request.args.get('h')
        timestamp = datetime.strptime(year + "-" + month + "-" + day + " " + hour, '%Y-%m-%d %H')
        return jsonify({'height': height_by_time(timestamp)})
    except TypeError:
        abort(400)