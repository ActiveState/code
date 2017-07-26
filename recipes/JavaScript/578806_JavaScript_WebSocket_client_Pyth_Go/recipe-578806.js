<!DOCTYPE html>
<html>
    <head>
        <title>
        Disk space monitoring with websocketd (Go) and psutil (Python).
        </title>
    </head>
    <body>
        <h3>
        Disk space monitoring with websocketd (Go) and psutil (Python).
        </h3>
        <p>
            <div id="log"></div>
        </p>
        <script>
            // helper function: log message to screen
            function log(msg) {
                document.getElementById('log').innerText += msg + '\n';
            }

            // setup websocket with callbacks
            var ws = new WebSocket('ws://localhost:8080/');
            ws.onopen = function() {
                log('CONNECT');
            };
            ws.onclose = function() {
                log('DISCONNECT');
            };
            ws.onmessage = function(event) {
                log('MESSAGE: ' + event.data);
            };
        </script>
    </body>
</html>
