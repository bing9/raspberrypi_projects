from httplib2 import Http
from json import dumps

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv('./.env', override= True, verbose=True)

def send_hangout(bot_message, webhook: str,
            space_id: str = None, thread_id: str = None):
    try:
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

        http_obj = Http()
        if space_id and thread_id:
            body = dumps({'text': str(bot_message),
                        'thread': {"name": f"spaces/{space_id}/threads/{thread_id}"}
                        })
        else:
            body = dumps({'text': str(bot_message)})

        response = http_obj.request(
            uri=webhook,
            method='POST',
            headers=message_headers,
            body=body,
        )
        return 'success'
    except:
        return 'fail'
    
def send_email(subject, content, receiver_email = None):
    sender_email = os.getenv('GMAIL_USER')
    receiver_email = receiver_email or os.getenv("SEND_TO")
    password = os.getenv('GMAIL_PWD')
    print(f"sending email from {sender_email} to {receiver_email}")

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""    Hi there,
    """
    html = f'  {content} '  

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )