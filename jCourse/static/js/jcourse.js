$(function() {

    // For lazy loading images
    $("img.course-image").lazyload({
        effect : "fadeIn"
    });

    indexCourses = function(btn_studies) {
        var courses = $('.panel-course');
        var checked = $('.major-checkbox').filter( ':checked' );
        var allMajors = false;
        var allStudies = false;
        if (checked.not( '#all-majors-cb' ).length == 0) {
            allMajors = true;
        }
        if (btn_studies == undefined && $('#st_Both').parent().hasClass('active')) {
            allStudies = true;
        }
        if (btn_studies != undefined && btn_studies == "Both") {
            allStudies = true
        }

        courses.each( function() {
            var show = true;
            classesArr = this.classList;
            if (!allMajors) {
                for(var i=0; i< classesArr.length; i++) {
                    if (classesArr[i].match('^major-') != undefined) {
                        major = classesArr[i].replace('major-', '');
                        if (!$('#checkbox_' + major).is(':checked')) {
                            show = false;
                        }
                    }
                }
            }
            if (show && !allStudies) {
                found = false;
                for(var i=0; i<classesArr.length; i++) {
                    if (classesArr[i].match('^studies-') != undefined) {
                        studies = classesArr[i].replace('studies-', '');
                        if (btn_studies == undefined && !$('#st_' + studies).parent().hasClass('active')) {
                            show = false;
                        }
                        if (btn_studies != undefined && btn_studies != studies) {
                            show = false;
                        }
                        found = true;
                    }
                }
                if (found == false) {
                    show = false;
                }
            }
            if (show) {
                credits = parseFloat( $(this).find('.course-credits').text() );
                values = $("#credit-slider").slider("values");
                if (credits < creditValues[values[0]] || credits > creditValues[values[1]]) {
                    show = false;
                }
            }

            if (show) {
                $(this).parent().show();
            } else {
                $(this).parent().hide();
            }
        });

        $("img.course-image").lazyload({
            event : "click"
        });
        
    }

    // Studies handle code!
    $('.btn-studies').click( function() {
        studies = $(this).children('.studies-radio')[0].id.replace('st_','')
        indexCourses(studies)
    });

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

    // Credit slider handle code!
    var creditValues = [0.1, 0.15, 0.2, 0.3, 1.1, 2.5, 3.0, 3.75, 5.0, 7.5, 10.0, 12.0, 15.0, 30.0];
    var nrCredits = creditValues.length;

    function sliderStop(event, ui) {
        indexCourses()
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
    majorCheckboxHandle();

    // Course page JS
    $('.rating-stars').raty( {
        starOn: '/static/images/star-on.png',
        starOff: '/static/images/star-off.png',
        starHalf: '/static/images/star-half.png',
        number: 5,
        mouseover: function(score, evt) {
            $(this).parents('form').find('.rating-my-score').text(score);
        },
        mouseout: function() {
            var form = $(this).parents('form');
            var score = form.find('input[name="old_score"]').val();
            form.find('.rating-my-score').text(score);
        },
        noRatedMsg: "To rate please log in!",
        score: function() {
            var form = $(this).parents('form');
            form.find('input[name="rating_value"]')
            return form.find('input[name="rating_value"]').val()
        },
        click: function(score, evt) {
            var form = $(this).parents('form');
            form.find('input[name="rating_value"]').val(score)
            var user = form.find('input[name="username"]')
            if (user.length > 0) {
                form.submit();
            }
        },
        readOnly: function() {
            var is_auth = $(this).parents('form').find('input[name="authenticated"]')
            return (is_auth.length == 0);
        },
        hints: ['bad', 'poor', 'regular', 'good', 'very good']
    });
    
});