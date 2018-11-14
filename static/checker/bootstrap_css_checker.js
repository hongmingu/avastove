$(function(){
    if($('#bootstrapCssTest').is(':visible')){
        var scheme = window.location.protocol == "https:" ? "https://" : "http://";
        var path = scheme + window.location.host + "/static/bootstrap/css/bootstrap.min.css";
        $("head").prepend('<link rel="stylesheet" href="' + path + '">')
    }
});
