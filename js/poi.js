/**
 * Created by dligtenb on 12.05.2015.
 * Modules for POIs
 */
// module for adding and updating pois
var pois = (function(){

    // changes the projection of a point from web mercator to lat/lng
    function unproject(latlng){
        var point = new L.Point(latlng.lng,latlng.lat);
        return L.Projection.SphericalMercator.unproject(point.divideBy(6378137));
    }

    function loadPeaks(date_time, peaks_group){
        var day = date_time.getDate(),
            // month +1 because getMonth() returns a value starting at 0
            month = date_time.getMonth() + 1,
            // round the hourly forecast to 3 hours
            hour = 3 * Math.round(date_time.getHours() / 3),
            year = date_time.getFullYear();

        var url = config.peaks_url +
            '?y=' + year + '&m=' + month + '&d=' + day + '&h=' + hour + '';
        // empty pois
        peaks_group.clearLayers();
        // asynchronous AJAX request to retreive and display mountain pois
        $.ajax({
            url:url,
            dataType:'json',
            success:function(response){
                // Leaflet icon that will represent the points on the map
                var icon = new L.icon({
                    iconUrl:"img/peak.svg",
                    iconSize:[28,28]
                });
                var peaks = L.geoJson(response, {
                    // bind a popup on each marker with a link to the node on OSM
                    onEachFeature: function(feature, layer){
                        layer.bindPopup('' + feature.properties.name + '<br />' +
                        '<a target="_blank" href="' + config.osm_node_url + '' + feature.id + '">OSM </a>');
                    },
                    // add the points to the layer, but first reproject the coordinates to WGS 84
                    pointToLayer: function (feature, latlng) {
                        var newlatlng = unproject(latlng);
                        return L.marker(newlatlng, {
                            icon:icon
                        });
                    }

                });
                peaks.addTo(peaks_group);
            },
            error:function(){
                error.showError('Fehler beim Abrufen der Bergspitzen!');
            }
        });
    }

    return{
        loadPeaks:loadPeaks
    }
})();