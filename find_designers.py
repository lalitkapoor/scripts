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

count = 0

"""Find all followers given a starting player recursively (doesn't include the
starting player by default, it will if another user is following the starting player)"""
def find_all(player, players, filter=None, max_depth=0):
    global count
    count+=1
    print str(count)+":",player
    if max_depth<0:
        return

    #players.add(player)

    new_users = get_following(player, filter=filter, username_only=False)
    new_usernames = set()
    if new_users:
        new_usernames = set([user['username'] for user in new_users]).difference(players)
        players.update(new_usernames)

        for user in new_users:
            all_players_data[user['username']] = user

    if new_usernames:
        for username in new_usernames:
            find_all(username, players, filter, max_depth-1)

"""Filter a player based on geographical criteria"""
def geo_filter(player, locations):
    if player['location']:
        ploc = player['location'].lower()
        for location in locations:
            if location.lower() in ploc:
                return player
    return None

"""Find all players based in Texas"""
def texas_filter(player):
    return geo_filter(player, ["TX"])

"""Find all players based in Dallas, TX"""
def dallas_surrounding_filter(player):
    cities = [
        "Plano",
        "Flower Mound",
        "Lewisville",
        "Southlake",
        "Highland Village",
        "Allen",
        "McKinney",
        "Frisco",
        "Denton",
        "Mesquite",
        "Garland",
        "Richardson",
        "Carrollton",
        "Grand Prairie",
        "Arlington",
        "Grapevine",
        "Irving",
        "Coppell",
        "Colony"
    ]
    short = map(lambda city: city +", TX", cities)
    lng = map(lambda city: city +", Texas", cities)


    return geo_filter(player, short+lng+['Dallas', 'Fort Worth'])

"""Find all players based in Austin, TX"""
def austin_filter(player):
    return geo_filter(player, ["Austin, TX"])

"""Find all players based in California"""
def california_filter(player):
    return geo_filter(player, [", CA"])

#texas_users = get_following('idefine', filter=texas_filter, username_only=False)
#pprint(texas_users)

all_players_names = set()
find_all('idefine', players=all_players_names, filter=dallas_surrounding_filter, max_depth=25)

output = u"username,shots_count,followers_count,likes_received_count,website_url,twitter\n"
for name in all_players_names:
    output+=name+","
    #output+=unicode(all_players_data[name]['name'])+","
    output+=unicode(all_players_data[name]['shots_count'])+","
    output+=unicode(all_players_data[name]['followers_count'])+","
    output+=unicode(all_players_data[name]['likes_received_count'])+","
    output+=unicode(all_players_data[name]['website_url'])+","
    output+=unicode(all_players_data[name]['twitter_screen_name'])+","
    output+=unicode("http://www.dribbble.com/"+name)+"\n"

pprint(all_players_names)
print len(all_players_names)

#write to disk
try:
    os.remove("users.csv")
except OSError:
    pass
users = open('users.csv', "a")
users.write(output)
users.close()
