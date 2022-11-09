const io = require("socket.io-client");

let socket = io("ws://localhost:8080");
    socket.on('connect', function() {
        socket.emit('joined', {data: ''});
    });