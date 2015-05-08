/**
 * Created by dligtenb on 08.05.2015.
 * Module for displaying error messages
 */
var error = (function(){
    function showError(message){
        console.log(message)
        $('#message').html(message);
        $('#error').show();

        $('#close').click(function() {
            $("#error").fadeOut('slow');
        });

        $(function() {
            setTimeout(function() {
                $("#error").fadeOut('slow');
                $('#message').html('');
            }, 5000);
        });
    }

    return{
        showError:showError
    }
})();