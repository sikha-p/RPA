#!/bin/bash
echo ============= Create a CA for the server cert =============
./create_ca.sh ca_server

echo ============= Create a server cert =============
./create_server.sh ca_server

echo ============= Create a client certificate for localhost with ca_server as its CA Certificate =============
./create_client.sh ca_server localhost
