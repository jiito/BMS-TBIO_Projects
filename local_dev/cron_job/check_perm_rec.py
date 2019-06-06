import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#import self made classes
import AclParse

#establish the directory to check 
x_paths = []
x_dir = {}

#initialize ACLParse Class
AclParse = AclParse.AclParse()


#define a function that check if each file in a directory is readable and 
# sends an email if not.
def checkPermissionsRec(directory, user, perm):
    print(directory)
    for r, d, f in os.walk(directory):
        #print(d)
        #print(f) 
        for file in f:
            if AclParse.checkPermFile(os.path.join(r,file), user, perm): # Check for read access
                continue
            else: #user does not have access 
                # add path to list of paths
                x_paths.append(os.path.join(r,file))
                #print("user DOES NOT have access to "+ file)
                continue
        for direc in d:
            #print(direc)
            result = AclParse.checkPermDir(os.path.join(r,direc), user)
            #print("RESULT is: " + str(result))
            if result == 3:
                continue  # can access, continue to next directory                        
            elif result == 0:  
                #print("user does not have READ OR EXEC access")
                x_dir[os.path.join(r,direc)] = 0
                continue
            elif result == 1:
                #print("user does not have EXEC access")
                x_dir[os.path.join(r,direc)] = 1
                continue
            elif result == 2:
                #print("user does not have READ access")
                x_dir[os.path.join(r,direc)] = 2
                continue

def emailResults(files, directories, to_e, from_e,  user):
    MAILHOST = "mailhost.bms.com"

    # establish email parameters
    msg = MIMEMultipart()
    from_addr = from_e
    to_addr = to_e
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "[BMS ACCESS ALERT] User does not have access"

    # write body of the email
    body = user + " does NOT have access to: \n \n FILES: \n"
    for path in files:
        body += path + "\n"
    body += "\n DIRECTORIES: \n"
    for direc in directories:
        if directories[direc] == 0:  # user does not have read or exec access
            body += direc + "-- no READ OR EXEC access \n"
        elif directories[direc] == 1:  # user does not have exec access
            body += direc + "-- no EXEC access \n"
        elif directories[direc] == 2:  # user does not have read access
            body += direc + "-- no READ access \n"
    msg.attach(MIMEText(body, 'plain'))

    # print("creates email")
    # establish SMTP server and send email
    s = smtplib.SMTP(MAILHOST)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()

    #print("sent email")    

if __name__ == "__main__":
    from_email = "benjamin.Rahill-Allan@bms.com"
    to_email = raw_input("Enter the desired dest email address:  ")

    root_path = raw_input("Path of root:  ")
    user = raw_input("Which user are you checking?  ")
    # perm = input("Permission (0-Read;1-Write;2-Execute):  ")

    checkPermissionsRec(root_path, user, 0)
    emailResults(x_paths, x_dir, to_email, from_email, user)


