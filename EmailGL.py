import smtplib



email_sender='bigbroprox@gmx.com'#server's email username
email_passwd='YONloz96' #server's email password

def SendMail (to,subject,text):
    """Sends a mail."""
    server=smtplib.SMTP('smtp.gmx.com',25) #server is the smtp server.
    server.ehlo()#smtp handshake.

    server.ehlo
    server.login(email_sender,email_passwd)
    body="\r\n".join([
        'To: %s' %to,
        'From: %s' %email_sender,
        'Subject: %s' %subject,
        '',
        text
        ])
    try:
        server.sendmail(email_sender,[to],body)
        print 'Email sent successfully!'
    except:
        print "Failed to send the email."
