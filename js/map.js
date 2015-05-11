/**
 * Created by dligtenb on 08.05.2015.
 * Modules for base map functionalities
 */
// Module for adding the base maps
var baseMap = (function(){
    // creates leaflet bounds from numerical coordinates
    function createBounds(){
        var p1 = new L.LatLng(config.swiss_bounds[0], config.swiss_bounds[1]),
            p2 = new L.LatLng(config.swiss_bounds[2], config.swiss_bounds[3]);
        return L.latLngBounds(p1, p2);
    }

    // initiates the actual map with default tiles in the background, fits the map to swiss bounds
    function createMap(defaultTiles){

        var bounds = createBounds();

        return L.map('map',{
            maxBounds:bounds,
            layers:[defaultTiles]
        }).fitBounds(bounds);
    }

    // returns a tile layer with predefined attributions
    function createTileLayer(source, attribution){
        return L.tileLayer(source, {
            attribution: attribution,
            minZoom:config.min_zoom,
            maxZoom:config.max_zoom
        });
    }

    // create a predefined attribution with a given url and text
    function createAttribution (url, urlText){
        return "<a href='http://wiki.openstreetmap.org/wiki/Open_Database_License'>OpenStreetMap</a> contributors | " +
            "Map data &copy; <a href=" + url + ">" + urlText + "</a> | " +
            "<a href='http://giswiki.hsr.ch/Webmapping_Clients'>About</a> | " +
            "<a href='http://www.hsr.ch/geometalab'>By GeometaLab</a>";
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

// Module for all positioning related functionalities
var position = (function(){

    // returns true if url hash exists and is valid, false if not
    function checkUrl(){
        // get hash  the URL
        var hash = window.location.hash;
        // check if something is in the hash
        if (hash){
            var splitted = hash.split("/");
            if (splitted.length == 3){
                var zoom = parseInt(splitted[0].substr(1)),
                    lat = parseFloat(splitted[1]),
                    long = parseFloat(splitted[2]);
                // check if parameters are within the swiss bounds and the allowed zoom levels
                if (zoom >= config.min_zoom && zoom <= config.max_zoom &&
                    lat >= config.swiss_bounds[0] && lat <= config.swiss_bounds[2] &&
                    long >= config.swiss_bounds[1] && long <= config.swiss_bounds[3]
                ){
                    return true
                }
            }
            error.showError('Ungültiger weblink!');
            return false
        }
        else{
            return false
        }
    }

    // from http://www.w3schools.com/js/js_cookies.asp
    function readCookie(cname, cookies) {
        var name = cname + "=";
        var ca = cookies.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1);
            if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
        }
        return "";
    }

    // load position data from cookies
    function loadCookies(){
        var cookies = document.cookie;
        if (cookies) {
            var center = [];
            center[0] = readCookie('lat', cookies);
            center[1] = readCookie('lng', cookies);
            center[2] = readCookie('zoom', cookies);
            return center
        }
        return false
    }

    // get the start Position either from the URL or the cookies
    function getStartPosition(map){
        if(!checkUrl()){
            var center = loadCookies();
            var hash = new L.Hash(map);
            if (center) {
                var latlng = new L.latLng(center[0], center[1]);
                map.setView(latlng, center[2])
            }
        }
        else{
            var hash = new L.Hash(map);
        }
    }

    // save the position to the clients cookies after every move event
    function savePositionToCookies(map){
        map.on('moveend', function() {
            var center = map.getCenter(),
                zoom = map.getZoom();
            document.cookie = 'lat= ' + center.lat + ';';
            document.cookie = 'lng=' + center.lng + ';';
            document.cookie = 'zoom=' + zoom + ';';
        });
    }

    return{
        getStartPosition:getStartPosition,
        savePositionToCookies:savePositionToCookies
    };

})();