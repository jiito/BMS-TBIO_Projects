#!/bin/sh

sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport 172.25.131.169:/ /efs/ukb-storage
