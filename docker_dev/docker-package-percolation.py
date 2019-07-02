#!/usr/bin/env python 
# Script to handle docker build errors 
from __future__ import print_function  # accomodate Python 2
from colors import *
from difflib import get_close_matches
import dockerfile
import os
import re
import subprocess

def runBuild(tag):
    cmd = 'docker build -t {}:latest . &> out.txt'.format(tag)

    try:
        res = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)      
        return res
    except subprocess.CalledProcessError as cmdexep:
        image, commands, err_msg = getImageAndCommands()

        cid = runNewContainer(image)
        print("Container ID: {}".format(cid))
        #print(commands)
        print("Docker specified error is: {}".format(color(err_msg, fg='red')))
        try:
            #print("yeet")
            runCmdsBin(cid[:3], commands)
        except Exception as exc:
            print(exc)
        finally:
            print("CLEANING UP...")
            cleanUpContainer(cid[:3])
        #raise Exception(err_str.format(cmd, cmdexep.returncode, cmdexep.output))

def rewriteDockerfile(package_name, )

def getAptPackages():
    try:
        grep_cmd = ["grep", "-e", "^[^#] apt-get.*install", "Dockerfile"]
        res = subprocess.check_output(grep_cmd)
    except subprocess.CalledProcessError as excp:
        print(color("There was an error in reading the Docker for apt packages", fg='red'))
        exit(0)

    res = re.sub('-[a-z][\s*]|\sapt-get\s|install\s|#|update|&|[\s*.*]\n', '', res).replace("\\", '').strip().split()

    return res

def getRPackages():
    grep_cmd = ["grep", "-Fe", "--->", "-n", "out.txt"]
    res = subprocess.check_output(grep_cmd)
    #print(res)

    lines = res.split('\n')

    #print(lines[len(lines) - 1])
   
    image = re.findall('\S{12}', lines[len(lines) - 3])[0]
    #print(container)
    line_num = int(re.findall('^\d*:', lines[len(lines) - 3])[0].strip(':'))+1
    #print(line_num)

    sed_cmd = 'sed -n {}p out.txt'.format(line_num)
    cmd_line = subprocess.check_output(sed_cmd, shell=True)
    cmd_line = re.sub('\s&&\s', '\n', cmd_line)
    #print(cmd_line)
    cmd_list = re.findall('\s{2}.*\n', cmd_line)   
    map_iter = map(lambda x: x.strip(), cmd_list)
    cmd_list = list(map_iter)
    #print(cmd_list)

    #find error message
    error_msg = tryCmd('grep E: out.txt')

    return image, cmd_list, error_msg

def runNewContainer(image):
    docker_run_cmd = 'docker run --rm -t -d {}'.format(image)

    containterID = tryCmd(docker_run_cmd)
    print("New CID is : {}".format(containterID))
    exit(0)
    return containterID

def runCmdsBin(cid, cmd_list):
    if len(cmd_list) == 1:
        return runCmdInContainer(cid, str(cmd_list[0]))
    else:
        j = " && "
        beg = j.join(cmd_list[:(len(cmd_list) / 2)])
        #print("BEG: {}".format(beg))
        end = j.join(cmd_list[(len(cmd_list) / 2):])
        #print("END: {}".format(end))

        try:
            runCmdInContainer(cid, beg)
        except Exception as excp:
            runCmdsBin(cid, cmd_list[:(len(cmd_list) / 2)])
        else:
            try:
                runCmdInContainer(cid, end)
            except:
                #print("END FAILED")
                runCmdsBin(cid, cmd_list[(len(cmd_list) / 2):])
            

def runCmdsSep(cid, cmd_list):
    for cmd in cmd_list:
        runCmdInContainer(cid, cmd)

def runCmdInContainer(cid, cmd):
    d_exec_cmd = 'docker exec -u root {} {}'.format(cid, cmd)
    #print(d_exec_cmd)
    return tryCmd(d_exec_cmd)

def cleanUpContainer(cid):
    d_stop_cmd = 'docker stop {}'.format(cid)
    tryCmd(d_stop_cmd)

def pruneContainers():
    subprocess.check_output('docker container prune -f', shell=True)

def tryCmd(cmd):
        proc = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE)
        stdout, stderr = proc.communicate()

        #print(stdout)
        if proc.returncode != 0:
            err_str = "\nERR:\nCOMMAND: {}\nexited with exit value {}\nwith output: {}\nand error: {}\n"
            raise Exception(color(err_str.format(color(cmd, fg='white'), proc.returncode,proc.stdout,stderr), fg ='red'))

        return stdout

if __name__ == "__main__":
    apt_packages = getAptPackages()

    adj_dictlist = {}
    for package in apt_packages:
        adj_dictlist[package] = tuple()

    print(adj_dictlist)
