/**
 * Created by dligtenb on 11.05.2015.
 * Module for all positioning related functionalities
 */

var position = (function(){

    // returns true if tile_url hash exists and is valid, false if not
    function checkUrl(){
        // get hash  the URL
        var hash = window.location.hash;
        // check if something is in the hash
        if (hash){
            var splitted = hash.split("/");
            if (splitted.length == 3){
                var zoom = parseInt(splitted[0].substr(1)),
                    lat = parseFloat(splitted[1]),
                    lng = parseFloat(splitted[2]);
                // check if parameters are within the swiss createBounds and the allowed zoom levels
                if (zoom >= config.min_zoom && zoom <= config.max_zoom &&
                    lat >= config.swiss_bounds[0] && lat <= config.swiss_bounds[2] &&
                    lng >= config.swiss_bounds[1] && lng <= config.swiss_bounds[3]
                ){
                    return true
                }
            }
            error.showError('Ungültiger Weblink!');
            return false
        }
        else{
            return false
        }
    }

    // returns the content from element in cookies with name cname
    // from http://www.w3schools.com/js/js_cookies.asp chapter "A Function to Get a Cookie"
    function readCookie(cname, cookie) {
        var name = cname + "=";
        var ca = cookie.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1);
            if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
        }
        return "";
    }

    // load position data from cookies, returns false if fails
    function centerFromCookies(){
        var cookie = document.cookie;
        if (cookie) {
            var center = [];
            center[0] = readCookie('lat', cookie);
            center[1] = readCookie('lng', cookie);
            center[2] = readCookie('zoom', cookie);
            return center
        }
        return false
    }

    // get the start Position either from the URL or the cookies
    function setStartPosition(map){
        // if no tile_url parameters given or parameters are faulty
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

    function showInfoBarOnNewSession(map){
        if(!readCookie('clicked_splash', document.cookie)){
            $("#splash").show();
        }
    }


    // save the position to the clients cookies after every move event
    function updateCookies(map){
        map.on('moveend', function() {
            var center = map.getCenter(),
                zoom = map.getZoom();
            document.cookie = 'lat= ' + center.lat + '; expires=Fri, 31 Dec 9999 23:59:59 GMT;';
            document.cookie = 'lng=' + center.lng + '; expires=Fri, 31 Dec 9999 23:59:59 GMT;';
            document.cookie = 'zoom=' + zoom + '; expires=Fri, 31 Dec 9999 23:59:59 GMT;';
        });
    }

    return{
        setStartPosition:setStartPosition,
        updateCookies:updateCookies,
        showInfoBarOnNewSession:showInfoBarOnNewSession
    };

})();