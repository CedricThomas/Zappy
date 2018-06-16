#!/usr/bin/node

const net = require('net');

const app = require('express')();
const server = require('http').Server(app);
const io = require('socket.io')(server);
const serveStatic = require('serve-static');

server.listen(33333);

app.use(serveStatic('public/', {'index': ['index.html', 'index.htm']}));

io.on('connection', function (sock) {
    console.log('Got connection');
    let cli = null;
    let isConnected = false;

    cli = net.connect(33334, "127.0.0.1", () => {
        isConnected = true;
        console.log("connected");
    });

    cli.on('error', (err) => {
        isConnected = false;
        sock.emit('my_error', {code: err.code});
    });

    sock.on('data', (msg) => {
        if (cli && isConnected) {
            cli.write(msg);
        } else {
            sock.emit('my_error', {code: "NOTCONNECTED"});
        }
    });

    cli.on('data', (msg) => {
       sock.emit('my_data', msg);
    });

    sock.on('disconnect', () => {
        cli.end();
        isConnected = false;
        console.log('Got disconnection');
    });
});
