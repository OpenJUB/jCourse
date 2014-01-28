$(function() {

    // Checkboxes handle code!
    majorCheckboxHandle = function() {
        if (this.id == "all-majors-cb") {
            $('.major-checkbox').prop('checked', false);
            $('#all-majors-cb').prop('checked', true);
        }
        var checked = $('.major-checkbox').filter( ':checked' );
        if (checked.length > 0) {
            if (checked.not( '#all-majors-cb' ).length > 0) {
                $('#all-majors-cb').prop('checked', false);
            }
        } else {
            $('#all-majors-cb').prop('checked', true);
        }
    }
    $('.major-checkbox').change(majorCheckboxHandle);
    majorCheckboxHandle();



    // Credit slider handle code!
    var creditValues = [0.1, 0.2, 0.5, 2.5, 3.75, 5.0, 7.5, 10.0]
    var credits = creditValues.map( function(val) { return val * 100 } )

    function sliderStop(event, ui) {
        var mvals = [0, 0]
        for(var v=0; v<=1; v++) {
            for (var i=1; i<credits.length; i++) {
                if (Math.abs(credits[i] - ui.values[v]) < Math.abs(credits[mvals[v]] - ui.values[v])) {
                    mvals[v] = i;
                }
            }
        }
        $('#credit-slider').slider("values", [ credits[mvals[0]], credits[mvals[1]] ]);
    }
    function sliderChange(event, ui) {
        $("#slider-handle-0").val( ui.values[0] / 100 )
        $("#slider-handle-1").val( ui.values[1] / 100 )
    }

    $("#credit-slider").slider({
        orientation: "horizontal",
        range: true,
        min: credits[0],
        max: credits[credits.length -1],
        values: [credits[0], credits[credits.length -1]],
        change: sliderChange,
        stop: sliderStop,
    });

    $("#slider-handle-0").val( creditValues[0] )
    $("#slider-handle-1").val( creditValues[creditValues.length - 1] )
});