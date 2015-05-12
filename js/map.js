/**
 * Created by dligtenb on 08.05.2015.
 * Modules for base map functionalities
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