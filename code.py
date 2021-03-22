import smtplib

recipiant_address = 'rossbergm@britishschoolmuscat.com'


def send_email(body):

    gmail_user = 'woodcockj@britishschoolmuscat.com'
    gmail_password = 'B2Spirit'

    sent_from = gmail_user

    to = [recipiant_address]
    subject = 'Subject: Test'
    body = body

    email_text = f'{subject} \n\n {body}'

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        print('Email Setup Complete')

        server.sendmail(sent_from, to, email_text)
        print('Email sent')

        server.close()

        print('Server Closed')

    except:
        print('Rip something went wrong in the sending of the email')


message = 'Hey mike does this work'

send_email(body=message)
