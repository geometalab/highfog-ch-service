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
                    link = L.DomUtil.createMap('a', 'controlicon', container);
                link.href = '#';
                link.title = 'Zur momentanen Position zoomen';
                link.innerHTML = '<img src="img/locate.png">';
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

// module for the datetime picker
var dateTimePicker = (function(){

    // returns a new leaflet control element for de picker
    function mapControl(){
        L.DateTimePicker = L.Control.extend({

            // position the element in the topleft corner of the map under the zoom controls
            options: {
                position: 'topleft'
            },

            onAdd: function () {
                // createMap control element with standard leaflet control styling
                var container = L.DomUtil.createMap('div', 'leaflet-control leaflet-bar datetimepicker'),
                    link = L.DomUtil.createMap('a', 'controlicon', container);
                link.href = '#';
                link.title = 'Prognosedatum und Uhrzeit auswählen';
                link.innerHTML = '<img src="img/clock.png">';

                return container;
            }
        });
        return L.DateTimePicker;
    }

    // initiate the datetime picker and add its event litener
    function initiatePicker(fogLayer, peaks_group, stops_groups, map){
        // limit the picker to 3 full hours and the next 3 days (including the current one)
        $('.datetimepicker').datetimepicker({
            allowTimes: [
                '00:00', '03:00', '06:00',
                '09:00', '12:00', '15:00', '18:00', '21:00'
            ],
            minDate:'0',
            maxDate:'+1970/01/03',
            // update layers and set new global forecast date when the picker is closed
            onClose:function(date_time){
                FORECAST_DATE = date_time;
                fog.updateFog(fogLayer);
                pois.reloadPois(stops_groups, peaks_group, map);
            }
        });

        // show the picker when the user clicks on the control element
        $('.datetimepicker').click(function(){
            $('.datetimepicker').datetimepicker('show');
        });
    }

    return{
        mapControl:mapControl,
        initiatePicker:initiatePicker
    }
})();
