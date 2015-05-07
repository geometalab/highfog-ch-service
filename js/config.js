/**
 * Created by dligtenb on 07.05.2015.
 * General configuration for changeable variables
 */
// JSON object for storing configuration data for the app
var config = {
    // Background map URLs, attribution URL and attribution Text
    background_maps: {
        swiss_style:{
            url:"http://tile.osm.ch/osm-swiss-style/{z}/{x}/{y}.png",
            attribution_url:"http://www.openstreetmap.org/copyright",
            attribution_text:"OSM"
        },
        mapbox_satellite: {
            url:"http://api.tiles.mapbox.com/v4/sfkeller.k0onh2me/{z}/{x}/{y}.png" +
            "?access_token=pk.eyJ1Ijoic2ZrZWxsZXIiLCJhIjoia3h4T3pScyJ9.MDLSUwpRpPqaV7SVfGcZDw",
            attribution_url:"https://www.mapbox.com/about/maps/",
            attribution_text:'MapBox'
        }
    },

    // Swiss bounding box in Lat/Long coordinates from http://giswiki.hsr.ch/Geographische_Koordinaten#Bounding_Box
    swiss_bounds:[45.45627757127799,5.69091796875,47.92738566360356,10.5194091796875 ],

    // Zoom settings
    min_zoom:9,
    max_zoom:18,

    // SBB URL to link to a timetable with prefilled destination
    sbb_url:"http://fahrplan.sbb.ch/bin/query.exe/dl?Z=",

    // OSM URL to link to a certain node with its OSM ID
    osm_node_url:"http://www.openstreetmap.org/node/",

    // highfog-ch webservice URLs
    heights_url:"http://sifsv-80047.hsr.ch/v1/heights/",
    peaks_url:"http://sifsv-80047.hsr.ch/v1/pois/",
    public_transport_url:"http://sifsv-80047.hsr.ch/v1/public_transport/",

    fog_tiles_url:"http://sifsv-80047.hsr.ch/tiles/",

    // Forecast hourly step and days to future settings
    forecast_step_hour:3,
    forecast_days:2
};