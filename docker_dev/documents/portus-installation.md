# Portus Installation

- [Portus Installation](#Portus-Installation)
  - [Docker Compose](#Docker-Compose)
  - [Hostname](#Hostname)
  - [Remove .yml files](#Remove-yml-files)
  - [Create Certificates](#Create-Certificates)
  - [Spin it up!](#Spin-it-up)



## Docker Compose

```bash
sudo pip install docker-compose
```

## Hostname

I used my ipaddr as the hostname 

In nginx/nginx.conf 
```
    server {
        listen 443 ssl http2;
        server_name [change it here!];
        root /srv/Portus/public;        
```

in .env file 

    MACHINE_FQDN=[change here!]

## Remove .yml files 

use to only get the one needed .yml file

```bash
rm docker-compose.* && wget https://gist.githubusercontent.com/Patazerty/d05652294d5874eddf192c9b633751ee/raw/6bf4ac6ba14192a1fe5c337494ab213200dd076e/docker-compose.yml
```

## Create Certificates 
used these commands to use IP address instead of DN. see [here](https://www.objectif-libre.com/en/blog/2018/06/11/self-hosting-a-secure-docker-registry-with-portus/) 
```bash
echo "subjectAltName = IP:[MY IP HERE]" > extfile.cnf #You can use DNS:domain.tld too
openssl genrsa -out secrets/rootca.key 2048 -nodes
openssl req -x509 -new -nodes -key secrets/rootca.key \
 -subj "/C=US/ST=CA/O=Acme, Inc." \
 -sha256 -days 1024 -out secrets/rootca.crt
openssl genrsa -out secrets/portus.key 2048
openssl req -new -key secrets/portus.key -out secrets/portus.csr \
 -subj "/C=US/ST=CA/O=Acme, Inc./CN=[MY IP HERE]"
openssl x509 -req -in secrets/portus.csr -CA secrets/rootca.crt -extfile \
 extfile.cnf -CAkey secrets/rootca.key -CAcreateserial \
 -out secrets/portus.crt -days 500 -sha256 
```

other option:
- move already made certificate into secrets/ 

or 

```bash 
openssl genrsa -out server.key 4096 && \
openssl req -new -key server.key -out server.csr && \
cp server.key server.key.org && \
openssl rsa -in server.key.org -out server.key && \
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt && \

mv server.crt portus.crt
mv server.key portus.key
```

## Spin it up! 

```bash
docker-compose up -d
```
