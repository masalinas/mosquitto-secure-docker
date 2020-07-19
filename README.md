# Description
Mosquitto Secure Docker Docker Deployment Deployment Steps

## Mosquitto certificates
Generate mosquitto certificates ca.crt, localhost.crt and localhost.key for localhost server from shell script

```shell
generate-CA.sh localhost
```

Generate certificates manually from openssl tool
- 1. Create a CA key pair:
```shell
openssl genrsa -des3 -out ca.key 2048
```
- 2. Create CA certificate and sign it with the private key from step 1:
```shell
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt
```

- 3. Create the broker key pair:
```shell
openssl genrsa -out localhost.key 2048
```

- 4. Create a CA certificate sign request using the key from step 3:
```shell
openssl req -new -out localhost.csr -key localhost.key
```

- 5. Use the CA certificate from step 2 to sign the request from step 4:
```shell
openssl x509 -req -in localhost.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out localhost.crt -days 3650
```

## Mosquitto tools
Install mosquitto tools for mosquitto_pub and mosquitto_sub tools
```shell
sudo apt-get install mosquitto-clients
```

## Mosquitto password tool
Install mosquitto for mosquitto_passwd tool and desable mosquitto service installed

```shell
sudo apt-get install mosquitto

sudo systemctl (start|stop) mosquitto
sudo systemctl (enable|disable) mosquitto
```

## Mosquitto authentication account
Create an authentication file for an authentication account: underground/underground

```shell
mosquitto_passwd -c passwordfile underground
```

## Docker Mosquitto container
Create eclipse-mosquitto docker container with SSL, persistence and authentication password from previous data created. These ports are opened:

- Port 1883 mqtt open for localhost
- Port 8883 mqtt SSL
- Port 9002 mqtt overwebsockets SSL

```shell
docker run --name mosquitto -it -p 8883:8883 -p 9002:9002 -v $PWD/mosquitto.conf:/mosquitto/config/mosquitto.conf -v $PWD/certs/ca.crt:/mosquitto/certs/ca.crt -v $PWD/certs/localhost.crt:/mosquitto/certs/localhost.crt -v $PWD/certs/localhost.key:/mosquitto/certs/localhost.key -v $PWD/password_file:/mosquitto/config/password_file eclipse-mosquitto
```

## Mosquitto debug
Login inside mosquitto container

```shell
docker exec -u root -ti mosquitto /bin/ash
```

## Test Mosquitto mqtt SSL port: 8883
Just a little test using mosquitto tools

```shell
mosquitto_sub -h localhost -p 8883 -u "underground" -P "underground" -t test -d --cafile certs/ca.crt --insecure

mosquitto_pub -h localhost -p 8883 -u "underground" -P "underground" -t test -m 'Hello SSL Mosquitto' -d --cafile certs/ca.crt --insecure
```

## Test Mosquitto mqtt over websockets SSL port: 9002
```shell
pip3 install paho-mqtt

python3 paho-client.py
```
