#!/usr/bin/env python
import subprocess
import json
import os
import time

# define global vars
working_dir = None
manifest_contents = None
manifest_obj = None
current_user = None
manifest_file_path = None
args = None

     
def evalOrDie(cmd, parseJsonFlag, msg):
    try:
        res = subprocess.check_output(cmd, shell=True)
        return res
    except subprocess.CalledProcessError as cmdexep:
        err_str = "\n\nError:\nCOMMAND: {}\nexited with exit value {}\n"
        raise Exception(err_str.format(cmd, cmdexep.returncode, cmdexep.output))
    
def slurp_json(filePath): 
    try:
        with open(filePath, 'r') as open_file:
            data = json.load(open_file)
    except:
        print("Error opening {}".format(filePath))
    return data

def empty(val):
    if val == None:
        return True
    else:
        return False

try:
    working_dir = os.getcwd()
    current_user = os.getlogin()
    print(working_dir)
    print(current_user)
except:
    print("Error in command line arguments in run_git_prod.pl\n")

if empty(current_user):
    current_user = "ec2-user"
assert (not empty(working_dir) or not os.path.isdir(working_dir)), "Error in run_git_prod.pl: working_dir {} does not exist".format(working_dir)


manifest_file_path = working_dir + "/manifest.json"
assert (os.path.isfile(manifest_file_path)), "Error in run_git_prod.pl: no file at {}".format(manifest_file_path)
manifest_obj = slurp_json(manifest_file_path)

just_repo_name = manifest_obj['repo_name']
assert (not empty(just_repo_name)), "Error: manifest must contain repo_name for run_git_prod.pl"

repoUserOrGroup = manifest_obj['owner']
assert (not empty(repoUserOrGroup)), "Error: manifest must contain owner for run_git_prod.pl"

repo = repoUserOrGroup + "/" + just_repo_name

clone_tag = manifest_obj['repo_release']
assert (not empty(clone_tag)), "Error: manifest must contain release_tag for run_git_prod.pl"

master_script = manifest_obj['master_script']
assert (not empty(master_script)), "Error: manifest must contain master_script for run_git_prod.pl"

os.chdir(working_dir)


execResText = ""


gitCloneCmd_pr = "git clone --recursive ssh://git\@biogit.pri.bms.com/{}.git".format(repo)
gitCloneCmd = gitCloneCmd_pr + " 2>&1"
execResText += "RUNNING COMMANDS: {}\n\nRESULTS:\n\n".format(gitCloneCmd_pr)
execResText += evalOrDie(gitCloneCmd, 0, "Error doing git clone of repo {}".format(repo))

repo_dir = working_dir + "/" + just_repo_name + "/"

#for compatibility with production runs that will also be runnable on Domino
os.environ['DOMINO_WORKING_DIR'] = repo_dir
os.environ['DOMINO_PROJECT_OWNER'] = repoUserOrGroup
os.environ['DOMINO_PROJECT_NAME'] = just_repo_name
os.environ['DOMINO_STARTING_USERNAME'] = current_user
os.environ['DOMINO_RUN_ID'] = "run_git_prod.pl:{}:{}:{}".format(repo, current_user, time.localtime())
os.environ['DOMINO_RUN_NUMBER'] = 1
os.chdir(repo_dir)

if not empty(clone_tag):
    gitCheckoutCmd_pr = "git checkout tags/{}".format(clone_tag)
    gitCheckoutCmd = gitCheckoutCmd_pr + " 2>&1"
    execResText += "RUNNING COMMANDS: {}\n\nRESULTS:\n\n".format(gitCheckoutCmd_pr)
    execResText += evalOrDie(gitCheckoutCmd, 0, "Error doing git checkout of tag {}".format(clone_tag))
else:
    raise Exception("Error in run_git_prod.pl: clone_tag is required.")

master_script_fullpath = repo_dir + master_script

assert (os.path.exists(master_script_fullpath)), "Error: master script {} not found".format(master_script)

chmodCmd_pr = "chmod u+x {}".format(master_script_fullpath)
chmodCmd = chmodCmd_pr + " 2>&1"
execResText += "RUNNING COMMANDS: {}\n\nRESULTS:\n\n".format(chmodCmd_pr)
execResText += evalOrDie(chmodCmd, 0, "Error making master script executable.")

execResText += "RUNNING COMMANDS: {}\n\nRESULTS:\n\n".format(master_script_fullpath)
execResText += evalOrDie("{} 2>&1".format(master_script_fullpath), 0, "Error executing master script {}".format(master_script))

print(execResText)