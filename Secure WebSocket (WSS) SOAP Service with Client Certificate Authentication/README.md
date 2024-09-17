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

### Create self signed server and client certificates
Ignore if you have certificates with you. Server will check whether the passed client certificate has been issued by the specified CA (as specified in the server.js code)

You should have following files in the certs folder by default
1.ca-template.cnf
2.client-template.cnf
3.create_ca.sh
4.create_client.sh
5.create_server.sh
6.init.sh
7.server.cnf
8.clean.sh


* run init.sh file
```
cd certs
./init.sh
```

* The init.sh initilizes 3 other .sh files. First one for creating a CA certificate for the server. (create_ca.sh). Next one for creating the certificate with the previously created CA certificate as its CA(parent). Next one is for creating the client cretificate. please find the more details about these files below. No need to run these .sh files seperately. init.sh will initiate these.


* Create a CA for the server cert 

./create_ca.sh ca_server
will create 3 files with the help of ca_template.cnf file
ca_server-key.pem
ca_server-crt.pem
ca_server.pfx

This is the CA certificate for the Server certificate.

* Create a server cert 
./create_server.sh ca_server

will create 4 files with the help of config template "server.cnf" file
server-key.pem
server-csr.pem
server-crt.pem
server.pfx

This is the Server certificate issued by the previously created CA certificate(ca_server)


* Create client Certificate 
You can create a CA certificate for the client certificate. 
eg : ./create_ca.sh ca_client
But here I'm using the CA server as the CA for client as well. So directly create client certificate with CA server as its CA.

./create_client.sh <CA certificate name> <client certificate name>
./create_client.sh ca_server localhost

This will create 4 files for the client certificate localhost with the help of config file "client-template.cnf"

localhost-key.pem
localhost-csr.pem
localhost-crt.pem
localhost.pfx

You will be using 
* server-crt.pem, server-key.pem and its CA certificate ca_server-crt.pem inside server.js code.
* localhost-crt.pem, localhost-key.pem and its CA certificate ca_server-crt.pem inside client.js code.

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
If you are getting error, please set the CA certificate as the NODE Extrac CA cert using the below command in command prompt
set NODE_EXTRA_CA_CERTS=C:\Users\Administrator\Documents\SIKHA\PSD\SoapService-AuthWithCert-WebSocket\new\certs\ca_server-crt.pem


You can use the below command to get the configuration set 
echo %NODE_EXTRA_CA_CERTS%

## Authors

Contributors names and contact info

1. Sikha Poyyil

