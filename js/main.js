/**
 * Created by dligtenb on 07.05.2015.
 * Main JavaScript file
 */

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

    var mapCenter = [46.7803,8.1985];

    // initiate map
    var map = baseMap.create(swissStyle, mapCenter);

    // add base tiles to the map
    var baseMaps={
        "OSM Swiss-Style":swissStyle,
        "Mapbox Satellite":mapbox
    };

    map.locate();
    map.on('locationfound', function(e){
        L.marker(e.latlng).addTo(map);

        L.ZoomToLocation = mapControls.zoomToLocation(e);
        map.addControl(new L.ZoomToLocation());
    });

    L.FitBounds = mapControls.boundControl(baseMap.bounds());
    // add control elements to the map
    L.control.layers(baseMaps).addTo(map);
    map.addControl(new L.FitBounds());

    error.showError('Ungültige URL Parameter übergeben!');
});