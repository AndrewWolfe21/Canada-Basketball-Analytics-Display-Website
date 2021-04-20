#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 20:39:02 2020

@author: Andrew
"""

import pandas as pd
import wikipedia as wp
import requests
from bs4 import BeautifulSoup
from datetime import datetime


filename = str(datetime.date(datetime.now())) + '-Canadians_WNBA_Active.csv'

#Wikipedia link with foreign players
url = 'https://en.wikipedia.org/wiki/List_of_foreign_WNBA_players'

#Get the html source
html = wp.page("List_of_foreign_WNBA_players").html().encode("UTF-8")
df = pd.read_html(html)[1]

#Find only players which have a Canadian nationality 
df_Canada = df.loc[df['Nationality[A]']=='Canada']

#Find only active players
df_Canada_Active = df_Canada[df_Canada['Player'].str.contains('*',regex=False)==True]

df_Canada_Active = df_Canada_Active['Player'].str.replace('*','',regex=False)

#Blank dataframe to capture career stats
df_player_careers_total = pd.DataFrame(columns=['Year','Tm','Age','G','GS', 'MP', 'FG', 'FGA','FG%','3P', 
                                 '3PA','3P%','2P', '2PA','2P%','FT', 'FTA','FT%','ORB',
                                 'DRB','TRB','AST','STL','BLK','TOV','PF','PTS'])

#Loop through all the players we just grabbed from Wikipedia
for i in df_Canada_Active: 
    strUrl = 'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fwnba%2Fplayers%2F'
    strPlayer = i
    #Add to url first initial of lastname
    strUrl = strUrl + strPlayer.split()[1][0].lower() + '%2F'
    #First five characters of last name
    strUrl = strUrl + strPlayer.split()[1][:5].lower() 
    #First two characters of first name
    strUrl = strUrl + strPlayer.split()[0][:2].lower() 
    #Plus 01w.html
    strUrl = strUrl + '01w.html&div=div_per_game0'
    
    page = requests.get(strUrl)
    page.content
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    table = soup.find('table')
    
    df = pd.read_html(str(table))[0]
    
    df = df[df.Year != 'Career']
    df['Player'] = strPlayer

    df['Year'] = df['Year'].str[:4]
    
    df_player_careers_total = df_player_careers_total.append(df)
    
    
df_player_careers_total.to_csv(filename,index=False)