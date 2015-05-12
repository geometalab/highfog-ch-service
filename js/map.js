/**
 * Created by dligtenb on 08.05.2015.
 * Modules for background map and overlay maps
 */
// module for adding the base maps
var baseMap = (function(){
    // creates leaflet bounds from numerical coordinates
    function createBounds(){
        var p1 = new L.LatLng(config.swiss_bounds[0], config.swiss_bounds[1]),
            p2 = new L.LatLng(config.swiss_bounds[2], config.swiss_bounds[3]);
        return L.latLngBounds(p1, p2);
    }

    // initiates the actual map with default tiles in the background, fits the map to swiss bounds
    function createMap(defaultMap, fogLayer){

        var bounds = createBounds();

        return L.map('map',{
            maxBounds:bounds,
            layers:[defaultMap, fogLayer]
        }).fitBounds(bounds);
    }

    // returns a tile layer witcreateh predefined attributions
    function createTileLayer(source, attribution){
        return L.tileLayer(source, {
            attribution: attribution,
            minZoom:config.min_zoom,
            maxZoom:config.max_zoom
        });
    }

    // create a predefined attribution with a given url and text
    function createAttribution (url, urlText){
        return "<a href='http://giswiki.hsr.ch/Hochnebelkarte'>About this map</a> | " +
            "Map data &copy; <a href=" + url + ">" + urlText + "</a> | " +
            "<a href='http://wiki.openstreetmap.org/wiki/Open_Database_License'>OpenStreetMap</a> contributors | " +
            "<a href='http://www.hsr.ch/geometalab'>By GeometaLab</a> | " +
            "<a href='http://twitter.com/geometalab'>t</a>";
    }

    // create background layers
    function createLayer(tileSource, attributionSource, description ){
        var attribution = createAttribution(attributionSource, description);
        return createTileLayer(tileSource, attribution);
    }

    return{
        create:createMap,
        createLayer:createLayer,
        bounds:createBounds
    };

})();

// module for updating the overlay fog
var fog = (function(){

    function updateFog(date_time, fogLayer){
        var day = date_time.getDate(),
            // month +1 because getMonth() returns a value starting at 0
            month = date_time.getMonth() + 1,
            // round the hourly forecast to 3 hours
            hour = 3 * Math.round(date_time.getHours() / 3),
            year = date_time.getFullYear(),
            url = config.height_at_time_url +
                '?y=' + year + '&m=' + month + '&d=' + day + '&h=' + hour + '';
        // JQuery AJAX request for getting the height data, shows error if not successful
        $.ajax({
            url:url,
            dataType:'json',
            success:function(response){
                // round the fog to 20
                var rounded_height = (20 * Math.round(response.height / 20));
                // load fog (set new URL) if its inside the displayable range, show error if not and set empty URL
                if (rounded_height <= 2000 &&rounded_height >= 500) {
                    var url = config.fog_tiles_url + '' + rounded_height + '/{z}/{x}/{y}.png';
                    fogLayer.setUrl(url);
                }
                else if(rounded_height <= 2000){
                    fogLayer.setUrl('');
                    error.showError('Nebelgrenze über der anzeigbaren Höhe!');
                }
                else{
                    fogLayer.setUrl('');
                    error.showError('Nebelgrenze unter der anzeigbaren Höhe!');
                }
            },
            error:function(){
                fogLayer.setUrl('');
                error.showError('Fehler beim Abrufen der Nebelgrenze!');
            }
        });
    }

    return{
        updateFog:updateFog
    }

})();
