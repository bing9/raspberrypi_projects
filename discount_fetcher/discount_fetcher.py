#!/usr/bin/env python
# coding: utf-8

# # Discount Fetcher

# ## Modules:
# 1. Source website API/location
# 2. Data cleansing
# 3. Logging and reporting
# 4. Notification

# In[1]:


# !pip install html5lib 


# In[2]:


import os
import requests
from dotenv import load_dotenv


# In[3]:


from bs4 import BeautifulSoup


# In[4]:


from pathlib import Path


# In[5]:


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# In[6]:


load_dotenv()


# In[7]:


urls = os.getenv('URL_TO_PASS')


# In[8]:


def source_website(url, test = False):
    if test == True:
        proxy = os.getenv('PROXIES')
        r = requests.get(url, proxies = {'http': proxy, 'https': proxy}, verify = False)
    else:
        r = requests.get(url)
    html = r.content
    return html


# In[9]:


def data_cleansing(html):
    bs = BeautifulSoup(html, 'html.parser')

    prices = bs.find_all('div', attrs = {'class': 'btn btn-block btn-primary'})

    prices = [i.contents[0].strip('\n€').replace(',', '.') for i in prices]
    return prices


# In[10]:


def data_logging(path, file_name, prices):
    p = Path(path, file_name)
    with open(p, mode = 'a+') as f:
        f.write('\n'+str(prices))


# In[11]:


def send_email(url, threshold):
    sender_email = os.getenv('GMAIL_USER')
    receiver_email = [i.strip() for i in list(os.getenv("SEND_TO").split(";"))][1]
    password = os.getenv('GMAIL_PWD')

    message = MIMEMultipart("alternative")
    message["Subject"] = f'Good news! Monitored product has been discounted.'
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""    Hi there,
    Your product {url} has been below threshold {threshold}.
    """ 
    html = ''  #requests.get(url_to_html).text 

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


# In[12]:


def notify_user(prices, threshold):
    current_price =    min([float(i) for i in prices])
    if current_price<=threshold:
        send_email(url, threshold)
    else:
        None


# In[14]:


for url in urls.split(';'):
    html = source_website(url, test = True)
    prices = data_cleansing(html)
    data_logging('.', 'mario_kart_prices.txt', prices)
    notify_user(prices, 90)


# In[ ]:




