"""
Created: 01.04.2015
@author: Dennis Ligtenberg
Script for updating peaks from EOSMDBOne
"""
import psycopg2
import csv

from pathlib import Path
from config.ext_config import EOSM_LOGIN
from webservice.models import Peak, db
from webservice import app


# Register an app for SQLAlchemy so this script can be executed standalone
db.init_app(app)
db.app = app


def load_existing_data():
    peaks_file_path = Path(__file__).parent / "initial_data" / "peaks.csv"
    with open(peaks_file_path, newline="") as csvfile:
        peaks = csv.reader(csvfile)
        db.session.query(Peak).delete()
        for row in peaks:
            new_entry = Peak(
                osm_id=int(row[3]), name=row[1], height=int(row[2]), geometry=row[0]
            )
            db.session.add(new_entry)
            db.session.commit()


def update_from_db():
    conn = psycopg2.connect(EOSM_LOGIN)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            WITH peaks AS (
            SELECT osm_id,name,way,substring(ele,'([-]?[0-9]{1,5})')::int AS ele
            FROM osm_point
            WHERE tags @> hstore('natural', 'peak')
            AND name is not null
            ),
            public_transport AS (
            SELECT *
            FROM osm_poi
            WHERE
            tags @> hstore('highway', 'bus_stop')
            OR tags @> hstore('public_transport', 'station')
            OR tags @> hstore('amenity', 'bus_station')
            OR hstore(tags)->'railway' IN ('stop', 'station', 'funicular', 'halt')
            ),
            viewpoints AS (
            SELECT *
            FROM osm_poi
            WHERE tags @> hstore('tourism', 'viewpoint')
            )
            SELECT DISTINCT ST_AsText(peaks.way) geom, COALESCE(peaks.name,'') as name,
            COALESCE(peaks.ele,0) as height,  COALESCE(peaks.osm_id,0) as osm_id
            FROM peaks, public_transport, viewpoints
            WHERE ST_DWithin(peaks.way, public_transport.way, 5000)
            AND ST_DWithin(peaks.way, viewpoints.way, 1000)
            ORDER BY 2;
        """
        )
        if cursor.rowcount:
            db.session.query(Peak).delete()
            for row in cursor:
                print(row)
                new_entry = Peak(
                    osm_id=row[3], name=row[1], height=row[2], geometry=row[0]
                )
                db.session.add(new_entry)
                db.session.commit()
            print("--------------------------------")
            print("Done!")
        else:
            print("--------------------------------")
            print("No results!")
    finally:
        cursor.close()


def run_update():
    try:
        update_from_db()
    except Exception as e:
        print(e)
        print("couldn't connect to OSMDBOne")
        load_existing_data()
        print("loaded preexisting data from October 2020")
    finally:
        print(f"Done Updating Peaks, containing {db.session.query(Peak).count()} Peaks")


if __name__ == "__main__":
    run_update()
