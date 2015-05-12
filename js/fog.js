/**
 * Created by dligtenb on 12.05.2015.
 */

// module for getting data from the webservice
var fog = (function(){

    function height(response, fogLayer){
        var rounded_height = (20 * Math.round(response.height / 20) + 100);

        var url = 'http://sifsv-80047.hsr.ch/tiles/' + rounded_height + '/{z}/{x}/{y}.png';
        fogLayer.setUrl(url)
    }

    function updateFog(date_time, fogLayer){
        var day = date_time.getDate(),
            // month +1 because getMonth() returns a value starting at 0
            month = date_time.getMonth() + 1,
            hour = date_time.getHours(),
            year = date_time.getFullYear(),
            url = 'http://sifsv-80047.hsr.ch/v1/height_at_time/' +
                '?y=' + year + '&m=' + month + '&d=' + day + '&h=' + hour + '';
        $.getJSON(url, function(response){
            height(response, fogLayer)
        });
    }

    return{
        updateFog:updateFog
    }

})();
