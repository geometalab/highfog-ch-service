var HIGHFOG_SERVICE_URL = "$EXTERNAL_HIGHFOG_SERVICE_URL";
/**
 * JSON object for storing configuration data for the app
 */
var config = {
    version:"1.1",
    // Background map URLs, attribution URL and attribution Text
    background_maps: {
        swiss_style:{
            tile_url:"http://tile.osm.ch/osm-swiss-style/{z}/{x}/{y}.png",
            attribution_url:"http://www.openstreetmap.org/copyright",
            attribution_text:"OpenStreetMap"
        },
        mapbox_satellite: {
            tile_url:"http://api.tiles.mapbox.com/v4/sfkeller.k0onh2me/{z}/{x}/{y}.png" +
            "?access_token=pk.eyJ1Ijoic2ZrZWxsZXIiLCJhIjoia3h4T3pScyJ9.MDLSUwpRpPqaV7SVfGcZDw",
            attribution_url:"https://www.mapbox.com/about/maps/",
            attribution_text:'MapBox'
        }
    },

    // Swiss bounding box in Lat/Long coordinates
    swiss_bounds:[45.7300, 5.8000, 47.9000, 10.600],
    swiss_center:[46.8259, 8.2000],

    // Zoom settings
    min_zoom:7,
    max_zoom:19,

    // Zoom level after witch the stops are displayed
    show_stops_from_zoom_level:14,

    // SBB URL to link to a timetable with prefilled destination
    timetable_url:"http://fahrplan.sbb.ch/bin/query.exe/dl?Z=",

    // OSM URL to link to a certain node with its OSM ID
    osm_node_url:"http://www.openstreetmap.org/node/",
    osm_way_url:"http://www.openstreetmap.org/way/",

    // highfog-ch webservice URLs
    heights_url:HIGHFOG_SERVICE_URL + "v1/heights/",
    height_at_time_url:HIGHFOG_SERVICE_URL + "v1/height_at_time/",
    peaks_url:HIGHFOG_SERVICE_URL + "v1/peaks/",
    public_transport_url:HIGHFOG_SERVICE_URL + "v1/public_transport/",

    fog_tiles_url: "$FOG_TILES_URL",

    // Forecast hourly step and days to future settings
    forecast_step_hour:3,
    forecast_days:5,

    // earth radius in meters for CRS reprojecting
    earth_radius:6378137
};
