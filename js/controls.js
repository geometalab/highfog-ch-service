/**
 * Created by dligtenb on 08.05.2015.
 * Module for creating control elements on the map
 */

var mapControls = (function(){

    // control element to zoom the map view to the full extent of switzerland
    function fitBoundControl(bounds){
        L.FitBounds = L.Control.extend({

            // position the element in the topleft corner of the map under the zoom controls
            options: {
                position: 'topleft'
            },

            onAdd: function (map) {
                // createMap control element with standard leaflet control styling
                var container = L.DomUtil.createMap('div', 'leaflet-control leaflet-bar fitbounds'),
                    link = L.DomUtil.createMap('a', '', container);
                link.href = '#';
                link.title = 'Zur gesamten Schweiz zoomen';
                link.innerHTML = 'CH';

                // use leaflets fitBounds method to fit view to the createBounds
                L.DomEvent.on(link, 'click', L.DomEvent.stop).on(link, 'click', function () {
                    map.fitBounds(bounds);
                });

                return container;
            }
        });
        return L.FitBounds;
    }

    function zoomToLocation(e, map){
        L.ZoomToLocation = L.Control.extend({
            // position the element in the topleft corner of the map under the zoom controls
            options: {
                position: 'topleft'
            },

            onAdd: function () {
                // createMap control element with standard leaflet control styling
                var container = L.DomUtil.createMap('div', 'leaflet-control leaflet-bar zoomposition'),
                    link = L.DomUtil.createMap('a', '', container);
                link.href = '#';
                link.title = 'Zur momentanen Position zoomen';
                link.innerHTML = '&#8982;';

                // use leaflets fitBounds method to fit view to the createBounds
                L.DomEvent.on(link, 'click', L.DomEvent.stop).on(link, 'click', function () {
                    map.setView(e.latlng, 14)
                });

                return container;
            }
        });
        return L.ZoomToLocation;
    }

    return{
        boundControl:fitBoundControl,
        zoomToLocation:zoomToLocation
    };

})();

var dateTimePicker = (function(){

    function mapControl(){
        L.DateTimePicker = L.Control.extend({

            // position the element in the topleft corner of the map under the zoom controls
            options: {
                position: 'topleft'
            },

            onAdd: function () {
                // createMap control element with standard leaflet control styling
                var container = L.DomUtil.createMap('div', 'leaflet-control leaflet-bar datetimepicker'),
                    link = L.DomUtil.createMap('a', '', container);
                link.href = '#';
                link.title = 'Prognosedatum und Uhrzeit auswählen';
                link.innerHTML = 'DT';

                return container;
            }
        });
        return L.DateTimePicker;
    }

    function updateLayers(fogLayer, peaks_group, stops_groups, bounds, zoom_level){
        fog.updateFog(fogLayer);
        pois.reloadPois(stops_groups, peaks_group, bounds, zoom_level);
    }

    function initiatePicker(fogLayer, peaks_group, stops_groups, map){
        $('.datetimepicker').datetimepicker({
            allowTimes: [
                '00:00', '03:00', '06:00',
                '09:00', '12:00', '15:00', '18:00', '21:00'
            ],
            minDate:'0',
            maxDate:'+1970/01/03',
            onClose:function(date_time){
                forecast = date_time;
                updateLayers(fogLayer, peaks_group, stops_groups, map)
            }
        });
        $('.datetimepicker').click(function(){
            $('.datetimepicker').datetimepicker('show'); //support hide,show and destroy command
        });
    }

    return{
        mapControl:mapControl,
        initiatePicker:initiatePicker
    }
})();
