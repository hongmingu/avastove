    var socket;
    var websocket_on;
    if(window.WebSocket){
        var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
        var ws_path = ws_scheme + '://' + window.location.host + "/re/socket/";
        socket = new ReconnectingWebSocket(ws_path);

        socket.onopen = function () {
            websocket_on = true;

        };
        socket.onclose = function () {
            websocket_on = false;
        };
    } else {
        websocket_on = false;
    }