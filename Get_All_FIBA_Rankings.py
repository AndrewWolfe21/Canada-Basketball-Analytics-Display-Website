#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 18:13:08 2020

@author: Andrew
"""

import requests 
import lxml.html as lh
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import pymysql
import mysql.connector as sql
import boto3
from io import StringIO


pd.set_option('display.max_columns', None)

#Url listing of the websites to grab FIBA rankings from 
urlList = {
    'Men':'https://www.fiba.basketball/rankingmen',
    'Women':'https://www.fiba.basketball/rankingwomen',
    'Boys':'https://www.fiba.basketball/rankingboys',
    'Girls':'https://www.fiba.basketball/rankinggirls'
    }

filename = str(datetime.date(datetime.now())) + '-FIBA_Rankings.csv'
df_rankings_all = pd.DataFrame(columns=['As_Of', 'Worldrank', 'Country', 'Area', 'Zonerank', 'IOC', 'Current points', '+/- Rank *'])

for key in urlList: 
    #Create a handle, page, to handle the contents of the website
    page = requests.get(urlList[key])#Store the contents of the website under doc
    doc = lh.fromstring(page.content)#Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')
    
    tr_elements = doc.xpath('//tr')#Create empty list
    col=[]
    i=0#For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        '%d:"%s"'%(i,name)
        col.append((name,[]))
        
    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]
        
        #If row is not of size 10, the //tr data is not from our table 
        if len(T)!=6:
            break
        
        #i is the index of our column
        i=0
        
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1
    
    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    
    df = df.replace(r'\r\n','',regex=True)
    
    df = df.loc[df['IOC'] == 'CAN']
    
    df.insert(2,'Area',key)
    df.insert(0, 'As_Of',datetime.date(datetime.now()))

    #df.to_csv('FIBA Rankings.csv', mode='a', index=False)
    df_rankings_all = df_rankings_all.append(df)
  
#df_rankings_all.to_csv(filename, index=False)

####Load onto S3 bucket 
ACCESS_KEY_ID = <S3 access key ID here> 
ACCESS_SECRET_KEY = <S3 secret key here> 
BUCKET_NAME = <S3 bucket name here> 
FILE_NAME = 'FIBA/Historial_Rankings/' + filename

# S3 Connect
s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY, 
    region_name = 'ca-central-1'
)

csv_buffer = StringIO()
df_rankings_all.to_csv(csv_buffer, index=False)

#Upload File
s3.Object(BUCKET_NAME, FILE_NAME).put(Body=csv_buffer.getvalue())
print ("Code worked to load file into S3 bucket!")


#####Load data into MySQL Database
# Credentials to database connection
host= <MySQL host name here> 
db= <MySQL database name here> 
usr= <MySQL User ID here>  
pwd= <MySQL User ID Password here> 

engine = create_engine("mysql+pymysql://" + usr + ":" + pwd + "@" + host + "/" + db)
print("Connected to MySQLDB")

df_rankings_all.to_sql(con=engine, name= <MySQL database table name here>, if_exists='append',index=False)
print("Code worked to load data into MySQL")