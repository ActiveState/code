#!/usr/bin/env node
//
// nicerest -- pipe your REST API `curl` calls through this for nicer output
//

var stdin = process.openStdin();
var EventEmitter = require('events').EventEmitter;

var buffer = "";

stdin.setEncoding('utf8');
stdin.on('data', function (chunk) {
    buffer += chunk;
});

stdin.on('end', function () {
    if (buffer.slice(0,5) === "HTTP/") {
        var index = buffer.indexOf('\r\n\r\n');
        var sepLen = 4;
        if (index == -1) {
            index = buffer.indexOf('\n\n');
            sepLen = 2;
        }
        if (index != -1) {
            process.stdout.write(buffer.slice(0, index+sepLen));
            buffer = buffer.slice(index+sepLen);
        }
    }
    if (buffer[0] === '{' || buffer[0] === '[') {
        try {
            process.stdout.write(JSON.stringify(JSON.parse(buffer), null, 2));
            process.stdout.write('\n');
        } catch(ex) {
            process.stdout.write(buffer);
            if (buffer[buffer.length-1] !== "\n") {
                process.stdout.write('\n');
            }
        }
    } else {
        process.stdout.write(buffer);
        if (buffer[buffer.length-1] !== "\n") {
            process.stdout.write('\n');
        }
    }
});
