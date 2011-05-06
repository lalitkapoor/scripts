#!/usr/bin/python

import json
import os
import time
from urllib2 import urlopen
from pprint import pprint

"""store the data collected from the dribbble api, using the username as the key"""
all_players_data = {}

def get_player(name):
    response = urlopen('http://api.dribbble.com/players/'+player+"/following?per_page=30&page="+str(page))
    return json.load(response)

"""Get followers given a current players"""
def get_following(player, page=1, filter=None, username_only=True):
    response = None
    try:
        response = urlopen('http://api.dribbble.com/players/'+player+"/following?per_page=30&page="+str(page))
    except:
        time.sleep(3)
        try:
            response = urlopen('http://api.dribbble.com/players/'+player+"/following?per_page=30&page="+str(page))
        except:
            return None

    data = json.load(response)
    players = data['players']
    results = []

    if filter:
        for p in players:
            if filter(p):
                if username_only==True:
                    results.append(p['username'])
                else:
                    results.append(p)
    else:
        if username_only==True:
            results = [p['username'] for p in players]
        else:
            results = players

    #print "page",data['page']," of",data['pages']

    if data['page'] < data['pages']:
        results.extend(get_following(player, page+1, filter, username_only))
    
    return results

"""Find all followers given a starting player recursively (doesn't include the 
starting player by default, it will if another user is following the starting player)"""
def find_all(player, players, filter=None, max_depth=0):
    print player
    if max_depth<0:
        return
    
    #players.add(player)
    new_users = get_following(player, filter=filter, username_only=False)
    new_usernames = set([user['username'] for user in new_users]).difference(players)
    players.update(new_usernames)
    
    for user in new_users:
        all_players_data[user['username']] = user
    
    for username in new_usernames:
        find_all(username, players, filter, max_depth-1)

"""Filter a player based on geographical criteria"""
def geo_filter(player, location):
    if player['location']:
        if location in player['location']:
            return player
    return None

"""Find all players based in Texas"""
def texas_filter(player):
    return geo_filter(player, "TX")

"""Find all players based in Dallas, TX"""
def dallas_filter(player):
    return geo_filter(player, "Dallas, TX")

"""Find all players based in California"""
def california_filter(player):
    return geo_filter(player, ", CA")

#texas_users = get_following('idefine', filter=texas_filter, username_only=False)
#pprint(texas_users)

all_players_names = set()
find_all('idefine', players=all_players_names, filter=dallas_filter, max_depth=25)

output = "username,shots_count,followers_count,likes_received_count\n"
for name in all_players_names:
    output+=name+","
    output+=str(all_players_data[name]['shots_count'])+","
    output+=str(all_players_data[name]['followers_count'])+","
    output+=str(all_players_data[name]['likes_received_count'])+","
    output+=str("http://www.dribbble.com/"+name)+"\n"

pprint(all_players_names)
print len(all_players_names)

#write to disk
os.remove("users.csv")
users = open('users.csv', "a")
users.write(output)
users.close()

