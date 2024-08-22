# Secure WebSocket (WSS) SOAP Service with Client Certificate Authentication

This repository provides a Node.js implementation of a SOAP service streaming via Secure WebSockets (WSS) with client certificate authentication. The service is designed to ensure secure communication between clients and the server using certificate-based authentication.


### Features

* **Secure WebSocket (WSS)**: Communication over WebSockets with TLS encryption.
* **SOAP Protocol**: Implements a SOAP service for structured message exchange
* **Client Certificate Authentication**: Authenticates clients using X.509 certificates.
* **Node.js Based**: Built with Node.js and commonly used libraries like ws, soap, and https.


### Prerequisites

Before running this project, ensure you have the following installed:

* **Node.js** (version 14.x or higher)
* **OpenSSL** (for generating certificates)
* A valid client and server certificate pair

### Installation

* Clone the repository:
* Install dependencies:
```
npm install
```

### Running the Service

* Start the SOAP Service over WSS:
```
node server.js
```

### Testing the Service

* Using the Provided Client:

```
node client.js
```

## Authors

Contributors names and contact info

ex. Sikha Poyyil

