# check_perm_rec.py
# Script to check the file and directory permissions 
# Benjamin Allan-Rahill (benjamin.Allan-Rahill@bms.com)
# 6/6/19 

import os
import sys
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#import self made classes
import AclParse

# initialize to data sctructures to store the paths the user cannot access  
x_paths = [] # files
x_dir = {} # directories 

#initialize ACLParse class
AclParse = AclParse.AclParse()


# define a function that checks if each file and directory starting at a root node is readable and 
# sends an email if not. Uses AclParse class (imported above)
#
# INPUT:    directory (str) -- root directory to start the search from 
#           user (str) -- which user's permissions you want to check in the ACL
#           perm (int) -- which permission are you checking (0-read, 1-write, 2-exec); default is 0
#
# OUTPUT: Adds paths to list and directories to dict that are used by the emailResults function               
def checkPermissionsRec(directory, user, perm):
    for r, d, f in os.walk(directory): # loop through all files staring at root directory (done recursively)
        for file in f:
            if AclParse.checkPermFile(os.path.join(r,file), user, perm): # Check for read access
                continue
            else: #user does not have access 
                # add path to list of unaccessible paths
                x_paths.append(os.path.join(r,file))
                continue
        for direc in d:
            result = AclParse.checkPermDir(os.path.join(r,direc), user)
            if result == 3:# can access, continue to next directory
                continue                          
            elif result == 0:  # does not have READ or EXEC access
                x_dir[os.path.join(r,direc)] = 0
                continue
            elif result == 1: # does not have EXEC access 
                x_dir[os.path.join(r,direc)] = 1
                continue
            elif result == 2: # does not have READ access
                x_dir[os.path.join(r,direc)] = 2
                continue

# define a function that emails the results of the permission check
# 
# INPUT:        files -- list of paths that cannot be read
#               directories -- dictionary of directories that cannot be access; key indicates which permission is revoked
#               to_e -- the email to send to 
#               from_e -- the email to send from 
#               user -- the user who's permissions we check

def emailResults(files, directories, to_e, from_e,  user):
    #establish mail server
    MAILHOST = "mailhost.bms.com"

    # establish email parameters
    msg = MIMEMultipart()
    from_addr = from_e
    to_addr = to_e
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "[BMS ACCESS ALERT] " + user.upper() + " does not have access"

    # write body of the email
    body = "[" + user + "] does NOT have access to: \n"
    if len(files) >= 1:
        body += "\n FILES: \n"
        for path in files:
            body += path + "\n"
    
    if len(directories) >=1 :
        body += "\n DIRECTORIES: \n"
        for direc in directories:
            if directories[direc] == 0:  # user does not have read or exec access
                body += direc + "-- no READ OR EXEC access \n"
            elif directories[direc] == 1:  # user does not have exec access
                body += direc + "-- no EXEC access \n"
            elif directories[direc] == 2:  # user does not have read access
                body += direc + "-- no READ access \n"
    msg.attach(MIMEText(body, 'plain'))

    # establish SMTP server and send email
    s = smtplib.SMTP(MAILHOST)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=)
    from_email = "benjamin.Rahill-Allan@bms.com"
    
    #establish user input (does not require quotation marks)
    to_email = sys.argv[1]
    root_path = sys.argv[2]
    user = sys.argv[3]

    # comment following line in if you want the change the permission that is being checked on the files
    # perm = input("Permission (0-Read;1-Write;2-Execute):  ")

    # generate lists
    checkPermissionsRec(root_path, user, 0)
    
    # send results
    if len(x_paths) == 0 and len(x_dir) == 0:
        exit()
    
    emailResults(x_paths, x_dir, to_email, from_email, user)


