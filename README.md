# Description
Mosquitto Secure Docker Deployment Steps

## Generate mosquitto certificates ca.crt, localhost.crt and localhost.key for localhost server
```shell
generate-CA.sh localhost
```

## Install mosquitto tools for mosquitto_pub and mosquitto_sub tools
```shell
sudo apt-get install mosquitto-clients
```

## Install mosquitto for mosquitto_passwd tool and desable mosquitto service installed
```shell
sudo apt-get install mosquitto

sudo systemctl (start|stop) mosquitto
sudo systemctl (enable|disable) mosquitto
```

## Create an authentication file for an authentication account: underground/underground
```shell
mosquitto_passwd -c passwordfile underground
```

## Creare eclipse-mosquitto docker container with SSL, persistence and authentication password from previous data created
```shell
docker run --name mosquitto -it -p 8883:8883 -v $PWD/mosquitto.conf:/mosquitto/config/mosquitto.conf -v $PWD/certs/ca.crt:/mosquitto/certs/ca.crt -v $PWD/certs/localhost.crt:/mosquitto/certs/localhost.crt -v $PWD/certs/localhost.key:/mosquitto/certs/localhost.key -v $PWD/password_file:/mosquitto/config/password_file eclipse-mosquitto
```

## Login inside mosquitto container
```shell
docker exec -u root -ti mosquitto /bin/ash
```

## Just a little test using mosquitto tools
```shell
mosquitto_sub -h localhost -p 8883 -u "underground" -P "underground" -t test -d --cafile certs/ca.crt --insecure
mosquitto_pub -h localhost -p 8883 -u "underground" -P "underground" -t test -m 'Hello SSL Mosquitto' -d --cafile certs/ca.crt --insecure
```
