/**
 * Created by dligtenb on 08.05.2015.
 * Modules for background map and overlay maps
 */
// module for adding the base maps
var baseMap = (function(){
    // creates leaflet createBounds from numerical coordinates
    function createBounds(){
        var p1 = new L.LatLng(config.swiss_bounds[0], config.swiss_bounds[1]),
            p2 = new L.LatLng(config.swiss_bounds[2], config.swiss_bounds[3]);
        return L.latLngBounds(p1, p2);
    }

    // initiates the actual map with default tiles in the background, fits the map to swiss createBounds
    function createMap(defaultMap, fogLayer, peaks, stops){

        var bounds = createBounds();

        return L.map('map',{
            maxBounds:bounds,
            layers:[defaultMap, fogLayer, peaks, stops]
        }).fitBounds(bounds);
    }

    // returns a tile layer wit predefined attributions
    function createTileLayer(source, attribution){
        return L.tileLayer(source, {
            attribution: attribution,
            minZoom:config.min_zoom,
            maxZoom:config.max_zoom
        });
    }

    // createMap a predefined attribution with a given tile_url and text for the background map copyright
    function createAttribution (url, urlText){
        return "<a href='http://giswiki.hsr.ch/Hochnebelkarte'>Über...</a> | " +
            "<a href='http://geometalab.tumblr.com/'>Blog</a> | v" + config.version + " | " +
            "Weather &copy; <a href='http://www.meteocentrale.ch/de/wetter/freizeitwetter/hochnebelobergrenze.html'>MeteoGroup</a> | " +
            "Hillshade &copy; <a href='http://www2.jpl.nasa.gov/srtm/'>NASA</a> | " +
            "Map &copy; <a href=" + url + ">" + urlText + "</a> | " +
            "<a href='http://www.openstreetmap.org/fixthemap'>Verbessere die Karte</a>";
    }

    // createMap background layers
    function createLayer(tileSource, attributionSource, description ){
        var attribution = createAttribution(attributionSource, description);
        return createTileLayer(tileSource, attribution);
    }

    return{
        createMap:createMap,
        createLayer:createLayer,
        createBounds:createBounds
    };

})();

// module for updating the overlay fog
var fog = (function(){

    function updateFog(fogLayer, stops_groups, peaks_group, map){
        var day = FORECAST_DATE.getDate(),
            // month +1 because getMonth() returns a value starting at 0
            month = FORECAST_DATE.getMonth() + 1,
            hour = FORECAST_DATE.getHours(),
            year = FORECAST_DATE.getFullYear();

        var url = config.height_at_time_url +
                '?y=' + year + '&m=' + month + '&d=' + day + '&h=' + hour + '';
        // JQuery AJAX request for getting the height data, shows error if not successful
        $.ajax({
            url:url,
            dataType:'json',
            success:function(response){
                // round the fog to 20
                var rounded_height = (20 * Math.round(response.height / 20));
                // update the displayed fogheight in the bottom left corner
                var hour_plus_3 = hour+3;
                $('#info').html('Potentielle Hochnebelobergrenze ' + day + '.' + month + '.' +
                    year + ', ' + hour + '-' + hour_plus_3 + ' Uhr<br>'
                    + rounded_height +' m ü.M. (&plusmn 100 m)');
                FORECAST_HEIGHT = rounded_height;

                // load fog (set new URL) if its inside the displayable range, show error if not and set empty URL
                if (rounded_height <= 2000 &&rounded_height >= 500) {
                    var url = config.fog_tiles_url + '' + rounded_height + '/{z}/{x}/{y}.png';
                    fogLayer.setUrl(url);
                }
                else if(rounded_height > 2000){
                    fogLayer.setUrl('');
                    error.showError('Hochnebelgrenze über der anzeigbaren Höhe!');
                    FORECAST_HEIGHT = 0;

                }
                else{
                    fogLayer.setUrl('');
                    error.showError('Hochnebelgrenze unter der anzeigbaren Höhe!');
                    FORECAST_HEIGHT =0;
                }
                pois.reloadPois(stops_groups, peaks_group, map);
                $("#slider").val(FORECAST_HEIGHT);
                slider._updateValue();
                FORECAST_TYPE = 'custom';
            },
            error:function(){
                // don't show any fog and fogheight if error occurs
                fogLayer.setUrl('');
                $('#height').html('');
                error.showError('Fehler beim Abrufen der Hochnebelgrenze!');
            }
        });
    }

    return{
        updateFog:updateFog
    }

})();
