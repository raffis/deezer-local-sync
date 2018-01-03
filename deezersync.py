#!/bin/env python

import os
import requests
import mutagen
import argparse

parser = argparse.ArgumentParser(description='Miugrate music lkibrary to deezer')
parser.add_argument('--path', '-p', dest="path", required=True,
                    help='Path to your music library')
parser.add_argument('--access_token', dest='access_token', required=True,
                    help='deezer access_topkenm)')
args = parser.parse_args()

def find(query_type, query):
    url = 'https://api.deezer.com/search/'+query_type+'?access_token='+args.access_token+'&q='+query
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("failed to search for "+query_type+" "+query)
    
    result = response.json()
    if result['total'] <= 0:
        raise Exception("could not find "+query+" on deezer library")
    
    if "error" in response.json():
        raise Exception(response.json()["error"]["message"])
            
    return result['data'][0]['id']

def addToFavourites(resource_type, resource_identifier, id):
    url = 'https://api.deezer.com/user/'+str(user_id)+'/'+resource_type+'?access_token='+args.access_token+'&'+resource_identifier+'='+str(id)
    response = requests.post(url)
    if response.status_code != 200:
        raise Exception("failed to add "+resource_type+" "+str(id)+" to my library")

    result = response.json()
    if result == False and "error" in result:
        raise Exception(result["error"]["message"])
    
    print "SUCCESSS: added resource "+str(id)+" to my deezer library"
    return True

def fetchUser():
    url = 'https://api.deezer.com/user/me?access_token='+args.access_token
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("failed to fetch user info")
    
    if "error" in response.json():
        raise Exception(response.json()["error"]["message"])        
    
    return response.json()


user_id = fetchUser()["id"]

print "building local database, this can take a while..."
artists = {}
for folder, subs, files in os.walk(args.path):
    for filename in files:
        try: 
            id3 = mutagen.File(os.path.join(folder, filename))
                
            if not artists.has_key(id3['albumartist'][0]):
                artists[id3['albumartist'][0]] = []

            if id3['album'][0] not in artists[id3['albumartist'][0]]:
                artists[id3['albumartist'][0]].append(id3['album'][0])
        except Exception as error: 
            print "ERROR: failed read id3 tags from file "+os.path.join(folder, filename)
            continue 

for artist in artists:
    print "import artist "+artist

    try:
        id = find('artist', artist)
        addToFavourites('artists', 'artist_id', id)
    except Exception as error:
        print "ERROR: "+repr(error)

    for album in artists[artist]:
        print "import album "+album
        try:
            id = find('album', 'artist:"'+artist+'",album:"'+album+'"')
            addToFavourites('albums', 'album_id', id)
        except Exception as error:
            print "ERROR: "+repr(error)
