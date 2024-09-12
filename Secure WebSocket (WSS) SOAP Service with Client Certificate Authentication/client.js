const WebSocket = require('ws');
const fs = require('fs');

const soap = require('soap');


const ws = new WebSocket('wss://localhost', {
    key: fs.readFileSync('certs/localhost-key.pem'),
    cert: fs.readFileSync('certs/localhost-crt.pem'),
    ca: fs.readFileSync('certs/ca_server-crt.pem')
});


// const ws = new WebSocket('wss://localhost', {
//     key: fs.readFileSync('ca_client-key.pem'),
//     cert: fs.readFileSync('ca_client-crt.pem'),
//     ca: fs.readFileSync('ca-crt.pem')
// });

ws.on('open', function open() {
    console.log('Connected to server');
    ws.send('wsdl');
});

ws.on('message', function incoming(data) {
    console.log(`Received: ${data}`);
});

ws.on('error', function error(err) {
    console.error('Connection error:', err);
});

ws.on('close', function close() {
    console.log('Disconnected from server');
});


