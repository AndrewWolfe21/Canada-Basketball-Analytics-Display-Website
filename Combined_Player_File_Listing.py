#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 17:01:41 2020

@author: Andrew
"""

#Combined for all the Canadian NBA Players

from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats import endpoints
import pandas as pd 
import time 


#All NBA Players names to grab for 
playerList = [
#'Tristan Thompson', 
'Trey Lyles',
'Shai Gilgeous-Alexander',
'RJ Barrett', 
'Oshae Brissett', 
'Nickeil Alexander-Walker', 
'Naz Mitrou-Long',
'Mfiondu Kabengele',
'Marial Shayok',
'Luguentz Dort',
'Kyle Alexander',
'Khem Birch',
'Kelly Olynyk',
'Jamal Murray',
'Ignas Brazdeikis',
'Dwight Powell',
'Dillon Brooks',
'Cory Joseph',
'Chris Boucher',
'Brandon Clarke',
'Andrew Wiggins',
#Mychal Mulder
]

seasonToGrab = '2019'
#filename = <insert filename path here> 
filename = filename  + seasonToGrab + '-CombinedPlayerBoxScores.csv'

######Create the dataframe by loading in a player outside of the loop 
player_dict = players.get_players()
time.sleep(2)
#Loop through player listing 
df_player_games_total = pd.DataFrame()
# Use ternary operator or write function 
# Names are case sensitive
player = [player for player in player_dict if player['full_name'] == 'Tristan Thompson'][0]
player_id = player['id']
#Call the API endpoint passing in lebron's ID & which season 
gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = seasonToGrab)
time.sleep(2)
#Converts gamelog object into a pandas dataframe
#can also convert to JSON or dictionary  
df_player_games = gamelog_player.get_data_frames()[0]
df_player_games.insert(2,'Player_Name','Tristan Thompson')
df_player_games_total = df_player_games
time.sleep(2)
######

#####Loop through list of players and append together 
for i in playerList: 
    # Use ternary operator or write function 
    # Names are case sensitive
    player = [player for player in player_dict if player['full_name'] == i][0]
    player_id = player['id']
    #Call the API endpoint passing in lebron's ID & which season 
    gamelog_player = playergamelog.PlayerGameLog(player_id=player_id, season = seasonToGrab)
    time.sleep(2)
    #Converts gamelog object into a pandas dataframe
    #can also convert to JSON or dictionary  
    df_player_games = gamelog_player.get_data_frames()[0]
    #df_player_games
    df_player_games.insert(2,'Player_Name',i)
    time.sleep(2)
    df_player_games_total = df_player_games_total.append(df_player_games)
    print(i) 

#Export to CSV 
df_player_games_total.to_csv(filename)
     