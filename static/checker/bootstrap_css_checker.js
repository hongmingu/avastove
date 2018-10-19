$(function(){
    if($('#bootstrapCssTest').is(':visible')){
        var path = 'https://' + window.location.host + "/bootstrap/css/bootstrap.min.css";
        $("head").prepend('<link rel="stylesheet" href="' + path + '">')
    }
});
