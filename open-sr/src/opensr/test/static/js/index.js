$(document).ready(function() {  
    var attributeHandler = function() {
        if ($("#test").val() && $("#password").val()) {
            $("#continue").removeAttr("disabled");
        } else {
            $("#continue").attr("disabled", "");
        };
    }

    $("#test").on("change", attributeHandler);
    $("#password").on("keyup", attributeHandler);
});