var scheme = window.location.protocol == "https:" ? "https://" : "http://";
var path = scheme + window.location.host + "/static/jquery/jquery-3.3.1.min.js";
window.jQuery||document.write('<script src="'+path+'"><\/script>');
