#!/usr/bin/env python
# coding: utf-8

# ### A project that will send you a mail at a specific time regarding the COVID19 updates of the state and district you have registered for. The first time you will register, it will send a mail  and then from next day it will send @9 am

# ### Import Libraries

import requests
import json
import pandas as pd
import smtplib
import sys
import os
from datetime import datetime
from email.message import EmailMessage
from pretty_html_table import build_table


# ### Read from the API and get the JSON data

def get_json_data(url) :
    response = requests.get(url)
    json_data = json.loads(response.text)    
    return json_data


# ### Get the state and district input from User and create a dataframe from it

def get_user_info(json_data,state,district) :

    if state not in json_data.keys() : 
        print("State doesn't exist. Please Try Again")
        sys.exit()

    if district not in json_data[state]['districtData'].keys() : 
        print("District doesn't exist. Please Try Again")
        sys.exit()
    
    district_df = pd.json_normalize(data=json_data[state]['districtData'][district])
    df = district_df[['active','confirmed','deceased','recovered','delta.confirmed','delta.deceased','delta.recovered']]
    df1 = df.rename(columns={'active':'Total Active','confirmed':'Total Confirmed','deceased':'Total Deceased','recovered':'Total Recovered','delta.confirmed':'Today Confirmed','delta.deceased':'Today Deceased','delta.recovered':'Today Recovered'})
    
    return df1


# ### Ask User for Inputs and write it to into a text file

def write_contacts_file(file,name,email,state,district) :
    with open(file,'a+') as f :
        contact = [name,email,state,district]
        f.write('\n'+','.join(contact))


# ### Send email with the state and district info as input by the user

def send_email(name,email,state,district,table) :
    
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PWD')
    
    msg = EmailMessage()
    msg['Subject'] = 'COVID19 Update on {}'.format(datetime.today().date())
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(f"Hey {name}! Here is your today's COVID19 update of {district},{state}")
    html_table = build_table(table,'grey_dark')
    
    msg.add_attachment(html_table,subtype='html')
    
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp :
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)
    
# ### Main function where all the other functions are called.

def main_function(name_input,email_input,state_input,district_input) :
    # get the json data from the api
    url = 'https://api.covid19india.org/state_district_wise.json'
    json_data = get_json_data(url)

    # create a dataframe using the user inputs from the json_data
    dataframe = get_user_info(json_data,state_input,district_input)
    
    # send the dataframe as email to the user
    send_email(name_input,email_input,state_input,district_input,dataframe)
    
    # write the user inputs into text files for sending them daily updated emails based on their district
    #write_contacts_file('contacts.txt',name_input,email_input,state_input,district_input)
    

if __name__ == '__main__' :

    # user inputs
    name_input = input('Enter your name:').capitalize()
    email_input = input('Enter your E-MAIL:').lower()
    state_input = ' '.join([i.capitalize() for i in input('Enter the name of State:').split() if i != 'and'])
    district_input = input('Enter the name of District:')
    
    main_function(name_input,email_input,state_input,district_input)
