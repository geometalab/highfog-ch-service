/**
 * Created by dligtenb on 08.05.2015.
 * Module for creating control elements on the map
 */

var mapControls = (function(){

    function fitBoundControl(bounds){
        L.FitBounds = L.Control.extend({

            // position the element in the topleft corner of the map under the zoom controls
            options: {
                position: 'topleft'
            },

            onAdd: function (map) {
                // create control element with standard leaflet control styling
                var container = L.DomUtil.create('div', 'leaflet-control leaflet-bar fitbounds'),
                    link = L.DomUtil.create('a', '', container);
                link.href = '#';
                link.title = 'Zur gesamten Schweiz zoomen';
                link.innerHTML = 'CH';

                // use leaflets fitBounds method to fit view to the bounds
                L.DomEvent.on(link, 'click', L.DomEvent.stop).on(link, 'click', function () {
                    map.fitBounds(bounds);
                });

                return container;
            }
        });
        return L.FitBounds;
    }

    return{
        boundControl:fitBoundControl
    };

})();