/**
 * Created by dligtenb on 07.05.2015.
 * Main JavaScript file, Initializes map
 */
// global List of public transport ids that have already been added to the map
var IDS = [];
// global currently selected forecast date, default now
var FORECAST_DATE = new Date();

$(document).ready(function () {

    // Swiss Style background map
    var swissStyle = baseMap.createLayer(
       config.background_maps.swiss_style.url,
       config.background_maps.swiss_style.attribution_url,
       config.background_maps.swiss_style.attribution_text
    );

    // Mapbox Satellite background map
    var mapbox = baseMap.createLayer(
        config.background_maps.mapbox_satellite.url,
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
                '<img class="icon" src="img/peak.svg" >' +
                '<div class="count">' + cluster.getChildCount() + '</div></span></div>' });
        }
    });
    var stops_group = new L.markerClusterGroup({
        maxClusterRadius: 40,
        iconCreateFunction: function(cluster) {
            return new L.DivIcon({className: "pois",
                html: '<div><span>' +
                '<img class="icon" src="img/stop.svg" >' +
                '<div class="count">' + cluster.getChildCount() + '</div></span></div>' });
        }
    });

    // initiate map
    var map = baseMap.createMap(swissStyle, fogLayer, peaks_group, stops_group);

    // background map control group
    var baseMaps={
        "OSM Swiss-Style":swissStyle,
        "Mapbox Satellite":mapbox
    };

    // overlay map control group
    var overlayMaps={
        "Nebel":fogLayer,
        "Bergspitzen":peaks_group,
        "Oev-Haltestellen":stops_group
    };

    // Add current fog overlay
    fog.updateFog(fogLayer);
    pois.loadPeaks(peaks_group);

    position.setStartPosition(map);
    // initiate position updater
    position.updateCookies(map);

    map.locate();
    map.on('locationfound', function(e){
        L.marker(e.latlng).addTo(map);

        L.ZoomToLocation = mapControls.zoomToLocation(e, map);
        map.addControl(new L.ZoomToLocation());
    });

    map.on('moveend', function(){
        pois.loadStops(stops_group, map.getBounds(), map.getZoom());
    });

    L.FitBounds = mapControls.boundControl(baseMap.createBounds());
    L.DateTimePicker = dateTimePicker.mapControl();
    // add control elements to the map
    L.control.layers(baseMaps, overlayMaps).addTo(map);
    map.addControl(new L.FitBounds());
    map.addControl(new L.DateTimePicker());

    dateTimePicker.initiatePicker(fogLayer, peaks_group, stops_group, map)

});