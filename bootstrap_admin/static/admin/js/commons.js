(function($) {
    $.fn.isAfter = function(sel){
        return this.prevAll(sel).length !== 0;
    }
    $.fn.isBefore= function(sel){
        return this.nextAll(sel).length !== 0;
    }
    $("input.sortedm2m:checkbox:not(:checked)").parent().parent().css("display", "none").css("visibility", "hidden");
})(django.jQuery);