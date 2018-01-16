/**
 * Created by dligtenb on 07.05.2015.
 * Main JavaScript file, Initializes map
 */
// global currently selected forecast date, default now
var FORECAST_DATE = new Date();
// global current forecast height
var FORECAST_HEIGHT = 0;
// used to save the source type of the forecast currently displayed
var FORECAST_TYPE;

// sets the forecast date to the current rounded date
function forecast_date_now(){
    FORECAST_DATE = new Date();
    FORECAST_DATE.setHours(Math.floor(FORECAST_DATE.getHours()/3.0) * 3);
    FORECAST_DATE.setMinutes(0);
    FORECAST_DATE.setSeconds(0);
}

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
        opacity: 0.8,
        tms: true
    });

    // markerClusterGroups for displayed points
    var peaks_group = new L.markerClusterGroup({
        maxClusterRadius: 40,
        iconCreateFunction: function(cluster) {
            return new L.DivIcon({className: "pois",
                html: '<div><span>' +
                '<img class="peak-icon" src="img/Npeak.png" >' +
                '<div class="count">' + cluster.getChildCount() + '</div></span></div>' });
        }
    });
    var stops_group = new L.markerClusterGroup({
        maxClusterRadius: 40,
        iconCreateFunction: function(cluster) {
            return new L.DivIcon({className: "pois",
                html: '<div><span>' +
                '<img class="stop-icon" src="img/Nstop.png" >' +
                '<div class="count">' + cluster.getChildCount() + '</div></span></div>' });
        }
    });

    // initiate map
    var map = baseMap.createMap(swissStyle, fogLayer, peaks_group, stops_group);
    // remove "Leaflet" prefix from attributions
    map.attributionControl.setPrefix("");

    // background map control group
    var baseMaps={
        "OSM Swiss-Style":swissStyle,
        "MapBox Satellite":mapbox
    };

    // overlay map control group
    var overlayMaps={
        "Hochnebel":fogLayer,
        "Berggipfel":peaks_group
    };
    // Set the forecast date to now
    forecast_date_now();
    // Add current fog overlay
    FORECAST_TYPE = 'actual';
    fog.updateFog(fogLayer, stops_group, peaks_group, map);

    // Show info bar if new session
    position.showInfoBarOnNewSession();
    position.setStartPosition(map);
    // initiate position updater
    position.updateCookies(map);

    // add control elements to the map
    L.FitBounds = mapControls.boundControl(baseMap.createBounds());
    L.DateTimePicker = dateTimePicker.mapControl();
    L.InfoButton = mapControls.infoButton();
    L.control.layers(baseMaps, overlayMaps).addTo(map);
    map.addControl(new L.FitBounds());
    map.addControl(new L.DateTimePicker());
    map.addControl(new L.InfoButton);

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
            $('#info').html('Nebel-Simulation<br>' + value + ' m ü.M.');
        }
        else if(first_load){
            FORECAST_HEIGHT = value;
            $('#info').html('Nebel-Simulation<br>' + value + ' m ü.M.');
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

    // Add zoom level to the layer control (without checkbox)
    $('.leaflet-control-layers-overlays').after('<div class="leaflet-control-layers-separator"></div>' +
        '<div class="leaflet-control-layers-custom">' +
        '<label><span>  Haltestellen (ab Zoom-Stufe 14)</span></label></div>'
    );
    listeners(map, stops_group, peaks_group, fogLayer);
}

$(document).ready(main);