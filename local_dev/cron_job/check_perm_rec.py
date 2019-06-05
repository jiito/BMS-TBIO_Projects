import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from acl import Acl # for dealing with ACLs

#import self made classes
import AclParse


#establish the directory to check 
path = "C:\\Users\\rahillab\\Desktop\\local_dev"
x_paths = []
AclParse = AclParse.AclParse()


#define a function that check if each file in a directory is readable and 
# sends an email if not.
def checkPermissionsRec(directory, user, perm):
    print(directory)
    for r, d, f in os.walk(directory):    
        for file in f:
            # TODO: Change to ACL commands
            if AclParse.checkPerm(str(r + "/" + file), user, perm): # Check for read access
                # test w/o sever
                print("user has access to "+ str(r + "/" + file))
            else:
                # add path to list of paths
                x_paths.append(str(r + "/" + file))
                print("user DOES NOT have access to "+ file)
                continue
        for direc in d:
            checkPermissionsRec(str(r + "\\" + direc), user, perm)                        

def emailResults(files, to_e, from_e,  user):
    MAILHOST = "mailhost.bms.com"

    # establish email parameters

    msg = MIMEMultipart()
    from_addr = from_e
    to_addr = to_e
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "[BMS] User does not have access"

    # write body of the email
    body = "Hi Andrew, \n I believe I have got the script working with ACLs on test directories! Check it out! \n \n"
    body = user + " does NOT have access to: \n"
    for path in files:
        body += path + "\n"
    msg.attach(MIMEText(body, 'plain'))

    print("creates email")
    # establsih SMTP server and send email
    s = smtplib.SMTP(MAILHOST)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

    print("sent email")    

if __name__ == "__main__":
    from_email = "benjamin.Rahill-Allan@bms.com"
    to_email = input("Enter the desired dest email address:  ")

    root_path = input("Path of root:  ")
    user = input("Which user are you checking?  ")
    perm = input("Permission (0-Read;1-Write;2-Execute):  ")

    checkPermissionsRec(root_path, user, perm)
    emailResults(x_paths, to_email, from_email, user)


