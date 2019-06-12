#!/usr/bin/env python
import os
import sys
import subprocess as sp


#so can do git operations (git clone, etc.) as the user via that user's ssh key
def writeSshConfig():
    try:
        with open("/home/domino/.ssh/config", 'w') as file:
            file.write(
                "host biogit.pri.bms.com\n"
                "HostName biogit.pri.bms.com\n"
                " IdentityFile /home/domino/.ssh/id_rsa_{}\n"
                " User git\n"
                " StrictHostKeyChecking no\n".format(current_user)
            )
    except:
        raise Exception("Error opening ssh config file to write: ")
    
    call("chmod 400 /home/domino/.ssh/config")

def call(cmd):
    try:
        out = sp.check_output(cmd, stderr=sp.STDOUT, shell=True)
        return out
    except sp.CalledProcessError as exc:
        raise Exception("\nfailed to execute: {} \n  w/ CODE: {} \n OUTPUT: {}\n".format(cmd, exc.returncode, exc.output))
        
def empty(val):
    if val == None or re.match(r"^\s*$", val):
        return True
    else:
        return False

if __name__ == "__main__":
    current_user = sys.argv[1]

    os.environ['PATH'] = '/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/jvm/java-8-oracle/bin:/usr/lib/jvm/java-8-oracle/db/bin:/usr/lib/jvm/java-8-oracle/jre/bin'

    uid = call('id -u domino')
    uid = uid.rstrip()

    gid = call('id -g domino')
    gid = gid.rstrip()

    call("mkdir -p /home/domino/{}".format(current_user))
    call("sshfs {0}\@stash.pri.bms.com:/stash /stash -o IdentityFile=/home/domino/.ssh/id_rsa_{0} " \
            "-o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o uid={1} -o gid={2}".format(current_user, uid, gid))
    call("sshfs {0}\@kraken.pri.bms.com:/home/{0} /home/domino/{0} -o IdentityFile=/home/domino/.ssh/id_rsa_{0} " \
        "-o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o uid={1} -o gid={2}".format(current_user, uid, gid))

    writeSshConfig()
