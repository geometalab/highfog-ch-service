/**
 * Created by dligtenb on 11.05.2015.
 */
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

    // returns the content from element in cookies with name cname, from http://www.w3schools.com/js/js_cookies.asp
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

    // load position data from cookies, returns false if fails
    function centerFromCookies(){
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
    function setStartPosition(map){
        // if no url parameters given or parameters are faulty
        if(!checkUrl()){
            var center = centerFromCookies();
            // initiate leafelt.hash plugin, but overwrite its center
            var hash = new L.Hash(map);
            if (center) {
                var latlng = new L.latLng(center[0], center[1]);
                map.setView(latlng, center[2])
            }
            // set default center (Switzerland) if no other center is found
            else{
                var latlng = new L.latLng(config.swiss_center);
                map.setView(latlng, config.min_zoom)
            }
        }
        else{
            // initiate leaflet.hash plugin
            var hash = new L.Hash(map);
        }
    }

    // save the position to the clients cookies after every move event
    function updateCookies(map){
        map.on('moveend', function() {
            var center = map.getCenter(),
                zoom = map.getZoom();
            document.cookie = 'lat= ' + center.lat + ';';
            document.cookie = 'lng=' + center.lng + ';';
            document.cookie = 'zoom=' + zoom + ';';
        });
    }

    return{
        setStartPosition:setStartPosition,
        updateCookies:updateCookies
    };

})();