$(function() {

    // For lazy loading images
    $("img.course-image").lazyload({
        effect : "fadeIn"
    });

    indexCourses = function() {
        var checked = $('.major-checkbox').filter( ':checked' );
        if (checked.not( '#all-majors-cb' ).length > 0) {
            majors = $('.major-checkbox').not( '#all-majors-cb' )
            majors.each( function(idx, elem) {
                var mid = elem.id.replace("checkbox_", "")
                if ($(elem).is(':checked')) {
                    $('.major-' + mid).show()
                } else {
                    $('.major-' + mid).hide()
                }
            });
        } else {
            $('.panel-course').show()
        }
    }

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

        indexCourses()
    }
    $('.major-checkbox').change(majorCheckboxHandle);
    majorCheckboxHandle();

    // Credit slider handle code!
    var creditValues = [0.1, 0.15, 0.2, 0.3, 1.1, 2.5, 3.0, 3.75, 5.0, 7.5, 10.0, 12.0, 15.0, 30.0];
    var nrCredits = creditValues.length;

    function sliderStop(event, ui) {
        // Put here code to change the courses
    }
    function sliderChange(event, ui) {
        $("#slider-handle-0").val( creditValues[ ui.values[0] ] )
        $("#slider-handle-1").val( creditValues[ ui.values[1] ] )
    }
    $("#credit-slider").slider({
        orientation: "horizontal",
        range: true,
        max: nrCredits-1,
        values: [0, nrCredits-1],
        slide: sliderChange,
        stop: sliderStop
    });
    $("#slider-handle-0").val( creditValues[0] )
    $("#slider-handle-1").val( creditValues[creditValues.length - 1] )
});