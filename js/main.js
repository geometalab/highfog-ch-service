/**
 * Created by dligtenb on 07.05.2015.
 * Main JavaScript file, Initializes map
 */
// global List of public transport ids that have already been added to the map
var IDS = [];
// global currently selected forecast date, default now
var FORECAST_DATE = new Date();
FORECAST_DATE.setHours(3 * Math.round(FORECAST_DATE.getHours() / 3));
FORECAST_DATE.setMinutes(0);
FORECAST_DATE.setSeconds(0);
var FORECAST_HEIGHT = 0;
// used to save the source type of the forecast currently displayed
var FORECAST_TYPE;

function main(){

    // Swiss Style background map
    var swissStyle = baseMap.createLayer(
        config.background_maps.swiss_style.tile_url,
        config.background_maps.swiss_style.attribution_url,
        config.background_maps.swiss_style.attribution_text
    );

    // Mapbox Satellite background map
    var mapbox = baseMap.createLayer(
        config.background_maps.mapbox_satellite.tile_url,
        config.background_maps.mapbox_satellite.attribution_url,
        config.background_maps.mapbox_satellite.attribution_text
    );

    // empty layer for the Fog overlay
    var fogLayer = L.tileLayer('',{
        minZoom: config.min_zoom,
        maxZoom: config.max_zoom,
        maxNativeZoom: 14,
        opacity: 0.8
    });

    // markerClusterGroups for displayed points
    var peaks_group = new L.markerClusterGroup({
        maxClusterRadius: 40,
        iconCreateFunction: function(cluster) {
            return new L.DivIcon({className: "pois",
                html: '<div><span>' +
                '<img class="icon" src="img/peak.png" >' +
                '<div class="count">' + cluster.getChildCount() + '</div></span></div>' });
        }
    });
    var stops_group = new L.markerClusterGroup({
        maxClusterRadius: 40,
        iconCreateFunction: function(cluster) {
            return new L.DivIcon({className: "pois",
                html: '<div><span>' +
                '<img class="icon" src="img/stop.png" >' +
                '<div class="count">' + cluster.getChildCount() + '</div></span></div>' });
        }
    });

    // initiate map
    var map = baseMap.createMap(swissStyle, fogLayer, peaks_group, stops_group);
    // rmove "Leaflet" prefix from attributions
    map.attributionControl.setPrefix("");

    // background map control group
    var baseMaps={
        "OSM Swiss-Style":swissStyle,
        "MapBox Satellite":mapbox
    };

    // overlay map control group
    var overlayMaps={
        "Hochnebel (prognostiziert)":fogLayer,
        "Berggipfel":peaks_group,
        "OeV-Haltestellen (ab Zoom 14)":stops_group
    };

    // Add current fog overlay
    FORECAST_TYPE = 'actual';
    fog.updateFog(fogLayer, stops_group, peaks_group, map);

    position.setStartPosition(map);
    // initiate position updater
    position.updateCookies(map);

    map.locate();
    map.on('locationfound', function(e){
        L.marker(e.latlng).addTo(map).bindPopup("Ihr Standort.").openPopup();

        L.ZoomToLocation = mapControls.zoomToLocation(e, map);
        map.addControl(new L.ZoomToLocation());
    });

    map.on('moveend', function(){
        pois.loadStops(stops_group, map.getBounds(), map.getZoom());
    });


    // show public transport from after zoom-level 14 and on, keeps display state after zooming out and in again
    var zoomStart = 0;
    var haslayer = true;
    // save the display state on most outer level
    map.on('zoomstart', function(){
        zoomStart = map.getZoom();
        if(zoomStart >= config.show_stops_from_zoom_level) {
            haslayer = map.hasLayer(stops_group)
        }
    });
    // on zoomend remove stops if zoom is smaller than set display level and show if its larger and haslayer is true
    map.on('zoomend', function(){
        if(map.getZoom() < config.show_stops_from_zoom_level){
            map.removeLayer(stops_group)
        }
        else if(haslayer == true && map.getZoom() >= config.show_stops_from_zoom_level){
            map.addLayer(stops_group)
        }
    });

    // add control elements to the map
    L.FitBounds = mapControls.boundControl(baseMap.createBounds());
    L.DateTimePicker = dateTimePicker.mapControl();
    L.control.layers(baseMaps, overlayMaps).addTo(map);
    map.addControl(new L.FitBounds());
    map.addControl(new L.DateTimePicker());

    // initiate datetime picker after the control button has been created
    dateTimePicker.initiatePicker(fogLayer, peaks_group, stops_group, map);

    // add Leaflet slider to the map
    // don't change the attribute at first initiation or if the slider value gets updated from the actual forecast
    var first_load = true;
    slider = L.control.slider(function(value) {
        var url = config.fog_tiles_url + '' + value + '/{z}/{x}/{y}.png';
        fogLayer.setUrl(url);
        if(FORECAST_TYPE != "actual") {
            FORECAST_HEIGHT = value;
            pois.reloadPois(stops_group, peaks_group, map);
            $('#height').html('Hochnebel auf ' + value + 'm wird simuliert.');
        }
        else if(first_load){
            FORECAST_HEIGHT = value;
            $('#height').html('Hochnebel auf ' + value + 'm wird simuliert.');
        }
        first_load = false;
    }, {
        max: 2000,
        position: 'topright',
        min: 500,
        step: 20,
        value: 0,
        logo: '<i>S</i>',
        orientation:'vertical',
        id: 'slider',
        increment:true,
        collapsed:false
    }).addTo(map);
}

$(document).ready(main);