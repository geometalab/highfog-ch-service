function listeners(map, stops_group, peaks_group, fogLayer) {

    // locate user
    map.locate();
    map.on('locationfound', function(e){
        L.marker(e.latlng).addTo(map).bindPopup("Ihr Standort.").openPopup();

        L.ZoomToLocation = mapControls.zoomToLocation(e, map);
        map.addControl(new L.ZoomToLocation());
    });

    // update strops after map is moved
    map.on('moveend', function(){
        pois.loadStops(stops_group, map.getBounds(), map.getZoom());
    });

    // show public transport from after zoom-level 14 and on, keeps display state after zooming out and in again
    var zoomStart = 0;
    var haslayer = true;
    // save the display state on most outer level
    map.on('zoomstart', function () {
        zoomStart = map.getZoom();
        if (zoomStart >= config.show_stops_from_zoom_level) {
            haslayer = map.hasLayer(stops_group)
        }
    });

    // on zoomend remove stops if zoom is smaller than set display level and show if its larger and haslayer is true
    map.on('zoomend', function () {
        if (map.getZoom() < config.show_stops_from_zoom_level) {
            map.removeLayer(stops_group)
        }
        else if (haslayer == true && map.getZoom() >= config.show_stops_from_zoom_level) {
            map.addLayer(stops_group)
        }
    });

    // Update the forecast to the current date if the title is clicked
    $("#title").click(function () {
        forecast_date_now();
        FORECAST_TYPE = 'actual';
        fog.updateFog(fogLayer, stops_group, peaks_group, map);
    });

    // Hide the info box on click
    document.cookie = 'clicked_splash=true';
    $(document).click(function () {
        $("#splash").fadeOut("slow", function () {
        });
    });

}