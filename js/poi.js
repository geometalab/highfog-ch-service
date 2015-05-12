/**
 * Created by dligtenb on 12.05.2015.
 * Modules for POIs
 */
// module for adding and updating peaks
var peaks = (function(){

    function loadPeaks(date_time, peaks_group, map){
        var day = date_time.getDate(),
            // month +1 because getMonth() returns a value starting at 0
            month = date_time.getMonth() + 1,
            // round the hourly forecast to 3 hours
            hour = 3 * Math.round(date_time.getHours() / 3),
            year = date_time.getFullYear();

        var url = config.peaks_url +
            '?y=' + year + '&m=' + month + '&d=' + day + '&h=' + hour + '';
        peaks_group.clearLayers();
        // asynchronous AJAX request to retreive and display mountain peaks
        $.ajax({
            url:url,
            dataType:'json',
            success:function(response){
                var peaks = L.geoJson(response, {
                    // bind a popup on each marker with a link to the node on OSM
                    onEachFeature: function(feature, layer){
                        layer.bindPopup('' + feature.properties.name + '<br />' +
                        '<a target="_blank" href="' + config.osm_node_url + '' + feature.id + '">OSM </a>');
                    },
                    // add the points to the layer, but first reproject the coordinates to WGS 84
                    pointToLayer: function (feature, latlng) {
                        var point = new L.Point(latlng.lng,latlng.lat);
                        var newlatlng = L.Projection.SphericalMercator.unproject(point.divideBy(6378137));
                        return L.marker(newlatlng);
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