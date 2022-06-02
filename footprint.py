# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 20:42:35 2022

@author: ritwik
"""


import requests
import browser_history as bh
import pandas as pd
import datetime


def get_footprint(url):
    if(url.startswith('https://')==False and url.startswith('http://')==False):
        url='https://'+url
    
    req='https://api.websitecarbon.com/site?url='
    print(url)
    s=requests.get(req+url)
    print(s)
    return s.json()


def get_history():
    gchrome=bh.browsers.Chrome()
    history_list=pd.DataFrame(gchrome.fetch_history().histories)
    return history_list

def preprocessing(browsing_data):
    browsing_data.columns=['dates','site']
    browsing_data['url']=browsing_data['site'].str.split('/',expand=True)[2]
    browsing_data.drop(columns=['site'],inplace=True)
    
    aaj=datetime.date.today()
    week=aaj-datetime.timedelta(days=7)
    month=aaj-datetime.timedelta(days=30)
    
    todays_data=browsing_data[browsing_data['dates'].dt.date==aaj]
    todays_data.drop_duplicates(subset=['url'],inplace=True)
    
    weeks_data=browsing_data[browsing_data['dates'].dt.date>=week]
    weeks_data.drop_duplicates(subset=['url'],inplace=True)
    
    months_data=browsing_data[browsing_data['dates'].dt.date>=month]
    months_data.drop_duplicates(subset=['url'],inplace=True)
    #browsing_data.drop_duplicates(subset=['url'],inplace=True)
    
    return todays_data,weeks_data,months_data
    


browsing_history=get_history()
data_1,data_7,data_30=preprocessing(browsing_history)

#footprintdata1=list(data_1['url'].apply(lambda x:print(x)))
footprintdata1=list(data_1['url'].apply(lambda x:get_footprint(x)))