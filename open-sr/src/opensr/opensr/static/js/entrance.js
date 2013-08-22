$(document).ready(function() {  
    var attributeHandler = function() {
        if ($("#password").val()) {
            $("#continue").removeAttr("disabled");
        } else {
            $("#continue").attr("disabled", "");
        };
    }
    
    $("#password").on("keyup", attributeHandler);
});