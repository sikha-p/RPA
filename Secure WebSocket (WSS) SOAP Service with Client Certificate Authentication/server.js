const https = require('https');
const fs = require('fs');
const WebSocket = require('ws');
const soap = require('soap');
const xml2js = require('xml2js');

// Load server and client certificates
const serverOptions = {
    key: fs.readFileSync('certs/server-key.pem'),
    cert: fs.readFileSync('certs/server-crt.pem'),
    ca: fs.readFileSync('certs/ca_server-crt.pem'), // Certificate authority (CA)
    requestCert: true, // Request client certificates
    rejectUnauthorized: true, // Reject unauthorized clients
};

const server = https.createServer(serverOptions);

const wss = new WebSocket.Server({ server });
let wsClient = null;

wss.on('connection', (ws, request) => {
    console.log("inside ");
    const clientCert = request.socket.getPeerCertificate();
    if (!request.client.authorized) {
        console.log('Client certificate is not authorized');
        ws.terminate();
        return;
    }

console.log(clientCert);
    console.log('Client connected:', clientCert.subject.CN);
    wsClient = ws;
    
    ws.on('message', (message) => {
        console.log(`Received message: ${message}`);
         if(message=="wsdl"){
                const xml = fs.readFileSync('myservice.wsdl', 'utf8');
                 ws.send(xml);
            }
    });

    ws.on('close', () => {
        wsClient = null;
        console.log('Client disconnected');
    });
});

const myService = {
    MyService: {
        MyPort: {
            MyFunction: function(args, callback) {
                console.log('MyFunction called with args:', args);
                
                // Send a SOAP response
                callback(null, { result: `Hello, ${args.name}` });
                
                // Stream data over WebSocket if client is connected
                if (wsClient) {
                    wsClient.send(`Streaming data for ${args.name}`);
                }
            },
        },
    },
};

 const xml = fs.readFileSync('myservice.wsdl', 'utf8');

server.listen(443, function() {
    soap.listen(server, '/wsdl', myService, xml);
    console.log('SOAP service listening on port 443');
});
