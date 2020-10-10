"""
Created: 22.04.2015
@author: Dennis Ligtenberg
Script for updating poi heights using the elevation webservice
Executing this will take a very long time!
"""
import ast
import os
import requests

from pyproj import Proj, transform
from pyproj import Transformer
from geoalchemy2 import func

from config.ext_config import ELEVATION_SERVICE_URL
from webservice import app
from webservice.models import Peak, PublicTransport, db

# Register an app for SQLAlchemy so this script can be executed standalone
db.init_app(app)
db.app = app


def update_heights(table):
    query = db.session.query(
        func.ST_X(table.geometry), func.ST_Y(table.geometry), table.osm_id
    )
    for res in query:
        x = res[0]
        y = res[1]
        transformer = Transformer.from_crs("epsg:3857", "epsg:4326")
        x, y = transformer.transform(x, y)
        print(x, y)

        try:
            url = ELEVATION_SERVICE_URL + "?lat=" + str(x) + "&lon=" + str(y) + ""
            with requests.get(url) as response:
                heightdict = response.json()
        # Set height to 0 if a HTTPError occurs
        except Exception as e:
            print(e)
            heightdict = {"geometry": {"coordinates": [0, 0, 0]}}
        result = db.session.query(table).filter(table.osm_id == res[2]).first()
        result.height = heightdict["geometry"]["coordinates"][2]
        db.session.commit()


def run_update():
    # TODO: use logging and log error correctly
    try:
        update_heights(Peak)
    except Exception as e:
        print(e)

    try:
        update_heights(PublicTransport)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    run_update()
