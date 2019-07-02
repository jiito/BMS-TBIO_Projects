#!/usr/bin/perl -w

#Query for the availability-zone where currently running
my $avail_zone = `/usr/bin/curl -s --noproxy "*" http://169.254.169.254/latest/meta-data/placement/availability-zone`;

#take off last character to get region
my $region = substr $avail_zone,0,(length($avail_zone)-1);

#mount the EFS drive using URL for current region
my $mnt_cmd = "sudo mount -t nfs -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-352a06d5.efs.${region}.amazonaws.com:/ /efs/ukb-storage";

system($mnt_cmd);
exit 0;
