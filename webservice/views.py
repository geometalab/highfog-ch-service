'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Views for request handling
'''
from flask import Blueprint, jsonify, request, abort
from update_fog_height import UpdateFogHeightForecast
from crossdomain import crossdomain
from query_issuer import get_peaks_at_forecasted_date, get_heights, get_stops_within_bounds_at_forecasted_date, get_max_forecasted_height_by_time
from datetime import datetime
import ext_config
webservice = Blueprint("webservice", __name__)


@webservice.route('/' + ext_config.REST_API_VERSION + '/' + ext_config.UPDATE_URL)
@crossdomain(origin='*')
def update():
    UpdateFogHeightForecast().update()
    return 'Data Updated'


@webservice.route('/' + ext_config.REST_API_VERSION + '/' + ext_config.HEIGHTS_FORECAST_URL)
@crossdomain(origin='*')
def heights():
    return jsonify(heights=get_heights())


@webservice.route('/' + ext_config.REST_API_VERSION + '/' + ext_config.FORECASTED_PEAKS_URL + '/')
@crossdomain(origin='*')
def get_pois():
    try:
        year = request.args.get('y')
        month = request.args.get('m')
        day = request.args.get('d')
        hour = request.args.get('h')
        timestamp = datetime.strptime(year + "-" + month + "-" + day + " " + hour, '%Y-%m-%d %H')
        pois = get_peaks_at_forecasted_date(timestamp)
        return jsonify(pois)
    except TypeError:
        abort(400)


@webservice.route('/' + ext_config.REST_API_VERSION + '/' + ext_config.FORECASTED_PUBLIC_TRANSPORT_URL + '/')
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
        stops = get_stops_within_bounds_at_forecasted_date(bounds, timestamp)

        return jsonify(stops)
    except TypeError:
        abort(400)


@webservice.route('/' + ext_config.REST_API_VERSION + '/' + ext_config.FORECASTED_HEIGHTS_URL + '/')
@crossdomain(origin='*')
def height_at_time():
    try:
        year = request.args.get('y')
        month = request.args.get('m')
        day = request.args.get('d')
        hour = request.args.get('h')
        timestamp = datetime.strptime(year + "-" + month + "-" + day + " " + hour, '%Y-%m-%d %H')
        return jsonify({'height': get_max_forecasted_height_by_time(timestamp)})
    except TypeError:
        abort(400)
