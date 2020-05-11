#to create pdf report
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
#to automate email
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def notify(issue):
    '''
    Send an email when the scraper is force quitted or data has been contaminated
    -:param issue: 'forcequit' or 'contamination' to specify the content of the email
    '''
        
    subject = "Craiglist Scraper Issue Report"


    body = body_text(issue)

    sender_email = "scraperinfosender@yahoo.com"
    receiver_email = "scraperinfosender@yahoo.com"
    file = "automate_report.pdf" # in the same directory as script
    password = "svoaptqjbjzghbmy"
    # Create the email head (sender, receiver, and subject)
    email = MIMEMultipart()
    email["From"] = sender_email
    email["To"] = receiver_email 
    email["Subject"] = subject
    # Add body and attachment to email
    email.attach(MIMEText(body, "plain"))
    attach_file = open(file, "rb") # open the file
    report = MIMEBase("application", "octate-stream")
    report.set_payload((attach_file).read())
    encoders.encode_base64(report)
    #add report header with the file name
    report.add_header("Content-Decomposition", "attachment", filename = file)
    email.attach(report)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP("smtp.mail.yahoo.com",587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_email, password) #login with mail_id and password
    text = email.as_string()
    session.sendmail(sender_email, receiver_email, text)
    session.quit()
    


def body_text(issue):
    '''
    Determines the body of the email message based on the type of issue
    -:param issue: 'forcequit' or 'contamination' to specify the content of the email
    '''



    if issue == "forcequit":
        body = "(This e-mail is automaticlly generated from the virtual machine: sysadmin@hrc.scarp.ubc.ca) The Craiglist scraper has been interrupted unexpectedly. To restart the scraper, Please follow the instructions attached."
    elif issue == "contamination":
        body = "(This e-mail is automaticlly generated from the virtual machine: sysadmin@hrc.scarp.ubc.ca) The Craiglist data collected during " + datetime.date.today().month + " seems to have been contaminated since the total number of listings was lower than 100."
    else:
        body = "There is an error with the Craiglist scraper"


    return body