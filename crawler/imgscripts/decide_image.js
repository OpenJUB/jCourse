




var jq = document.createElement('script');
jq.src = "http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(jq);








jQuery.noConflict();
$ = jQuery
$('.img-links').click( function() {
    console.log("cp " + $(this).attr('src') + " /home/daniel/hacks/jCourse/crawler/imgscripts/downloaded_images/" + $(this).attr('id'));
});





