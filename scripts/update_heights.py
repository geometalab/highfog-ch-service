'''
Created: 22.04.2015
@author: Dennis Ligtenberg
Script for updating poi heights using the elevation webservice
Executing this will take a very long time!
'''
from webservice.models import db, Peak, PublicTransport
from webservice import app
from geoalchemy2 import func
import urllib2
import ast
from pyproj import Proj, transform

# Register an app for SQLAlchemy so this script can be executed standalone
db.init_app(app)
db.app = app


def update_heights(table):
    query = db.session.query(func.ST_X(table.geometry), func.ST_Y(table.geometry), table.osm_id)
    for res in query:
        x = res[0]
        y = res[1]
        proj1 = (Proj(init='epsg:3857'))
        proj2 = (Proj(init='epsg:4326'))
        x, y = transform(proj1, proj2, x, y)

        try:
            url = 'http://height-service.dev.ifs.hsr.ch/dtm/v1/elevation?lat=' + str(y) + '&lon=' + str(x) + ''
            response = urllib2.urlopen(url).read()
            heightdict = ast.literal_eval(response)
        # Set height to 0 if a HTTPError occurs
        except urllib2.HTTPError:
            heightdict = {'geometry': {'coordinates': [0, 0, 0]}}
        print heightdict
        result = db.session.query(table).filter(table.osm_id == res[2]).first()
        result.height = heightdict['geometry']['coordinates'][2]
        db.session.commit()

update_heights(Peak)
update_heights(PublicTransport)
print 'Done!'
