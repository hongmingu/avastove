if(typeof($.fn.modal)==='undefined'){
    var scheme = window.location.protocol == "https:" ? "https://" : "http://";
    var path = scheme + window.location.host + "/static/bootstrap/js/bootstrap.min.js";
    document.write('<script src="'+ path +'"><\/script>')
}
