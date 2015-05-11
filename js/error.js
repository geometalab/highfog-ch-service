/**
 * Created by dligtenb on 08.05.2015.
 * Module for displaying error messages
 */
var error = (function(){
    function showError(message){
        // Add error message to DOM element
        $('#message').html(message);
        $('#error').show();

        // Fade message out on click
        $('#close').click(function() {
            $("#error").fadeOut('slow');
        });

        // Fade out after 5 seconds
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