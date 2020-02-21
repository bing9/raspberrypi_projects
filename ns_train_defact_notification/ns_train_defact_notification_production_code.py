#!/usr/bin/env python
# coding: utf-8

# # NS delayes notification
#
# NS API address: https://www.ns.nl/en/travel-information/ns-api
#
# credentials management: https://dev.to/jamestimmins/django-cheat-sheet-keep-credentials-secure-with-environment-variables-2ah5
# https://pypi.org/project/python-dotenv/
#

# In[151]:


#!pip install python-dotenvb
#!pip install osa


# In[152]:


#pip install jupyter_helpers


# In[153]:


import http.client, urllib.request, urllib.parse, urllib.error, base64, pandas as pd
import json
import os
from pandas.io.json import json_normalize
import numpy as np
#from jupyter_helpers.namespace import NeatNamespace
import datetime
import time
import requests
#import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict

pd.set_option('display.max_columns', 300) # display 300 columns without shrinking
pd.set_option('display.max_rows', 100) # Show more rows


# In[154]:


from dotenv import load_dotenv
load_dotenv(override=True)


# ## Manual data insert

# In[155]:


# user_data=defaultdict()
# user_data['daily_work_leave'] = {'from_uic': 8400061, 'to_uic': 8400319, 'h':6, 'm':26, 'enabled':True}
# user_data['daily_work_return_4'] = {'from_uic': 8400319, 'to_uic': 8400061, 'h':16, 'm':8, 'enabled':True}
# user_data['daily_work_return_6'] = {'from_uic': 8400319, 'to_uic': 8400061, 'h':18, 'm':38, 'enabled':True}
# user_data['session_key'] = 'None'
# user_data['email_sent'] = 'False'

# with open('user_data.json', 'w') as fp:
#     json.dump(user_data, fp)


# # Workflow read json file

# In[156]:


def read_user_data():
    global imported_json

    with open('user_data.json') as json_file:
        imported_json = json.load(json_file)

    global user_data
    user_data = imported_json.copy()
    del user_data['session_key'], user_data['email_sent']

    global session_key
    session_key = imported_json['session_key']

    df_user_data = pd.DataFrame(user_data).T
    df_user_data[df_user_data['enabled']==True]
    df_user_data['search_date_time'] = df_user_data.apply(lambda row: datetime.datetime.today().replace(hour=row.h, minute=row.m, second =0).strftime('%Y-%m-%dT%T%z') ,axis=1)
    df_user_data['current_date_time'] = datetime.datetime.today()
    df_user_data['diff'] = pd.to_datetime(df_user_data['search_date_time']) - pd.to_datetime(df_user_data['current_date_time'])

    global df_user_data_input
    df_user_data_input = df_user_data[df_user_data['diff']>pd.Timedelta(0, unit='s')].sort_values(by='diff', ascending=True).head(1).to_dict(orient='records')
    return None


# In[157]:


def date_time_column(x):
    '''Function to find JSON dict date columns by name and then convert them in pandas to_datetime.'''
    date_time_col=[]
    l = list(x.columns)
    for i in l:
        if i.find('DateTime')==-1:
            continue
        else:
            date_time_col.append(i)
            x[i] = pd.to_datetime(x[i])
    return x


# In[158]:


def send_email(status, delayed_min, url_to_html ):

    sender_email = os.getenv('GMAIL_USER')
    receiver_email = [i.strip() for i in list(os.getenv("SEND_TO").split(";"))][1]
    password = os.getenv('GMAIL_PWD')

    message = MIMEMultipart("alternative")
    message["Subject"] = 'Train '+status+'!' + '('+ str(delayed_min) + ' mins)'
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """    Hi there,
    The train scheduled on {seach_date_time} has status {status} by {delayed_min} minutes.
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
    return None


# In[159]:


def connect_to_ns_api(from_uic, to_uic, search_date_time):
    # all ride information
    # https://apiportal.ns.nl/docs/services/public-reisinformatie-api/operations/ApiV3TripsGet?

    key = os.getenv("NS_KEY")

    headers = {
        # Request headers
        'Accept': '',
        'X-Request-ID': '',
        'X-Caller-ID': '',
        'x-api-key': '',
        'Authorization': '',
        'Ocp-Apim-Subscription-Key': '%s' % key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'originUicCode': '%s' % from_uic,
        'destinationUicCode': '%s' % to_uic,
        'dateTime': '%s' % search_date_time,
        'previousAdvices': 2,
        'nextAdvices': 8 ,
    })

    try:
        conn = http.client.HTTPSConnection('gateway.apiportal.ns.nl')
        conn.request("GET", "/public-reisinformatie/api/v3/trips?%s" % params, "{body}", headers)
        response = conn.getresponse()

        data = response.read()

        #print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data


# In[160]:


def status(target_train):

    status='normal'
    delayed_min = 0
    url_to_html = target_train['meta_shareUrl'].values.item()['uri']
    if target_train['cancelled'].bool() == True:
        status = 'cancelled'
    else:
        try:
            diff = target_train['origin_actualDateTime'] - target_train['origin_plannedDateTime']
            delayed_min = diff.values.item()/60000000000
            if delayed_min > 5 :
                status = 'delayed > 5 mins'
            else:
                status = 'normal'
        except:
            if target_train['meta_status'].values.item() != 'NORMAL':
                status = target_train['meta_status'].values.item()
            else:
                status = 'normal'
        pass

    return status, int(delayed_min), url_to_html


# In[161]:


def get_data_from_ns(from_uic, to_uic, search_date_time, **kwargs):

    data = connect_to_ns_api(from_uic, to_uic, search_date_time)

    d = json.loads(data)
    lenghth = len(d)
    if lenghth >0:
        print(f'Data successfully got from NS. len={lenghth}')

    df_unpack = json_normalize(data=d['trips'], record_path=['legs'], meta=['ctxRecon','status','transfers','plannedDurationInMinutes','actualDurationInMinutes','punctuality'
                                                                       , 'realtime','optimal','shareUrl'], errors='ignore',meta_prefix='meta_' , sep='_')
    #print(type(df_unpack['origin_plannedDateTime']))

    date_time_column(df_unpack)

    df_unpack['time_to_target'] = df_unpack['origin_plannedDateTime'].apply(lambda x: abs(x - pd.Timestamp(search_date_time+'+0100') ) )
    #print(df_unpack['time_to_target'])

    #target_train = df_unpack.copy()[df_unpack['origin_plannedDateTime']==search_date_time+'+0100'].head(1)
    target_train = df_unpack.copy().sort_values(by='time_to_target', ascending =True).head(1)
    selected_len = len(target_train)
    #TODO: try to write function that get the n top values closes to target search time.

    #date_time_column(target_train)

    global status, delayed_min, url_to_html
    if selected_len>0:
        print(f'Target time selected. Time={search_date_time}')
        status, delayed_min, url_to_html = status(target_train)
        print(f'Status {status}; Delayed {str(delayed_min)} mins.')
    else:
        print(f'No train selected for time {search_date_time}')


    if status == 'normal':
        print('Train is Normal. No need to send email.')
        return 'False'
    else:
        try:
            send_email(status, delayed_min, url_to_html)
            print('email sent successfully')
            return 'True'
        except:
            print('email error')
            return 'False'


# In[162]:


#def check_which_job_to_run(df_user_data_input, ):
read_user_data()

if len(df_user_data_input)>0 and session_key != df_user_data_input[0]['search_date_time']:
    # If the search time has changed. Then re-initiate the status
    imported_json['session_key'] = df_user_data_input[0]['search_date_time']
    session_key = imported_json['session_key']
    imported_json['email_sent'] = 'False'

    try:
        email_sent = get_data_from_ns( **df_user_data_input[0]) #Current email_se
        imported_json['email_sent'] = email_sent
        with open('user_data.json', 'w') as fp:
            json.dump(imported_json, fp)
    except:
        print('error: email not sent')

elif len(df_user_data_input)>0:
    if imported_json['email_sent'] == 'True':
        print('Email already sent before. No need to duplicate.')
    else:
        try:
            email_sent = get_data_from_ns( **df_user_data_input[0])
            imported_json['email_sent'] = email_sent
            with open('user_data.json', 'w') as fp:
                json.dump(imported_json, fp)
        except:
            print('error: email not sent')
else:
    print('No more trains to check for today!')


# In[ ]:
