import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    body = "THIS IS A TEST! \n" + user + " does NOT have access to: \n"
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
    from_email = "Benjamin.Rahill-Allan@bms.com"
    to_email  = "Andrew.Smith1@bms.com"
    emailResults(["Dog", "a", "BMS", "Cat"], to_email, from_email, "rahillab")    
    