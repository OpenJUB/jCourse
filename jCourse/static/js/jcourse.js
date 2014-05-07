$(function() {

    // (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    // (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    // m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    // })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    // ga('create', 'UA-47744399-1', 'jcourse.herokuapp.com');
    // ga('send', 'pageview');

    // // For lazy loading images
    // $("img.course-image").lazyload({
    //     effect : "fadeIn"
    // });

    indexCourses = function(offset, size, btn_studies, btn_terms) {
        if ($(".sidebar-panel").length == 0) {
            return ;
        }
        var courses = $('.panel-course');
        var checked = $('.major-checkbox').filter( ':checked' );
        var allMajors = false;
        var allStudies = false;
        var allTerms = false;
        var searchTerm = $('.course-search-bar').val().toLowerCase();
        if (checked.not( '#all-majors-cb' ).length == 0) {
            allMajors = true;
        }
        if (btn_studies == undefined && $('#st_Both').parent().hasClass('active')) {
            allStudies = true;
        }
        if (btn_studies != undefined && btn_studies == "Both") {
            allStudies = true
        }
        if (btn_terms == undefined && $('#tm_All').parent().hasClass('active')) {
            allTerms = true;
        }
        if (btn_terms != undefined && btn_terms == "All") {
            allTerms = true
        }

        var showedSoFar = 0;

        courses.each( function() {
            if (showedSoFar < offset + size) {
                // If it has to be shown
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
                if (show && !allTerms) {
                    found = false;
                    for(var i=0; i<classesArr.length; i++) {
                        if (classesArr[i].match('^term-') != undefined) {
                            term = classesArr[i].replace('term-', '');
                            if (btn_terms == undefined && !$('#tm_' + term).parent().hasClass('active')) {
                                show = false;
                            }
                            if (btn_terms != undefined && btn_terms != term) {
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
                    course_name = $(this).find('.course-name').find('a').text();
                    cname = course_name.toLowerCase()
                    if (cname.indexOf(searchTerm) == -1) {
                        show = false;
                    }
                }

                if (show) {
                    $(this).parent().show();
                    showedSoFar += 1;
                } else {
                    $(this).parent().hide();
                }
            } else {
                // If there are enough hits just hide it
                $(this).parent().hide();
            }
        });

        if (showedSoFar < offset + size) {
            $(".no-more-courses").show();
            $(".loading-courses").hide();
        } else {
            $(".loading-courses").show();
            $(".no-more-courses").hide();
        }

        $("img.course-image").lazyload({
            event : "click"
        });
    }

    // Search handle code!
    $(".course-search-bar").keypress(function(event) {
        if (event.which == 13) {
            indexCourses(0, 16);
        }
    });
    $(".course-search-bar").keyup(function() {
        if ($(this).val() == "") {
            indexCourses(0, 16);
        }
    });

    // Studies handle code!
    $('.btn-studies').click( function() {
        studies = $(this).children('.studies-radio')[0].id.replace('st_','')
        indexCourses(0, 16, studies)
    });

    // Term handle code!
    $('.btn-terms').click( function() {
        term = $(this).children('.terms-radio')[0].id.replace('tm_','')
        indexCourses(0, 16, undefined, term)
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

        indexCourses(0, 16)
    }
    $('.major-checkbox').change(majorCheckboxHandle);

    // Credit slider handle code!
    var creditValues = [0.1, 0.15, 0.2, 0.3, 1.1, 2.5, 3.0, 3.75, 5.0, 7.5, 10.0, 12.0, 15.0, 30.0];
    var nrCredits = creditValues.length;

    function sliderStop(event, ui) {
        indexCourses(0, 16)
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

    // Endless scroll
    $(window).scroll(function() {
        if ($(".loading-courses:visible").length > 0) {
            if(( $(document).height() - $(window).height() ) - $(window).scrollTop() < 10 ) {
                cnt = $('.panel-course:visible').length;
                indexCourses(0, cnt + 16);
            }
        }
    });




    // Course compare JS 
    $(".course-block-course-url").click( function(event) {
        if ($('.compare-course-link').parent().hasClass("active")) {
            event.preventDefault();
            window.location = "./" + $(this).attr("slug");
        }
    });



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
        hints: ['1', '2', '3', '4', '5']
    });

    // Logged out rating tooltip
    var ratingTooltips = $('.ratings-tooltip')
    if (ratingTooltips.length > 0) {
        ratingTooltips.tooltip({
            placement: 'left',
            html: false,
            title: 'Log in to vote!'
        });
        ratingTooltips.attr('data-original-title', 'Log in to vote!')
    }
    var ratingClarif = $('.ratings-tooltip-clarif')
    if (ratingClarif.length > 0) {
        ratingClarif.tooltip({
            placement: 'top',
            title: function() {
                var type = $(this).parents('form').find('input[name="rating_type"]').val();
                if (type == 'ALL') {
                    return "How do you rate the course in general?"
                } else if (type == 'WKL') {
                    return "More stars means higher workload"
                } else if (type == 'DIF') {
                    return "More stars means higher difficulty"
                } else if (type == 'PRF') {
                    return "How do you rate this professor's performance?"
                } 
            }
        })
    }

    // Tooltip for CampusNet
    $("#campusnet-popover").tooltip({title: 'Please log in with your CampusNet credentials!'})
});