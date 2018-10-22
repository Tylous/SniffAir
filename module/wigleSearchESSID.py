#!/usr/bin/python
from gmplot import gmplot
import requests
from requests.auth import HTTPBasicAuth
import sys

wigle_username = sys.argv[1]
wigle_password = sys.argv[2]
ESSID = sys.argv[3]

payload = {'ssid': ESSID, 'api_key': (wigle_username + wigle_password).encode('base64','strict')}
results = requests.get(url='https://api.wigle.net/api/v2/network/search', params=payload, auth=HTTPBasicAuth(wigle_username, wigle_password)).json()

lat = 39.7392
lon = -104.9903

print "Creating map..."
#setup map in AoI
gmap = gmplot.GoogleMapPlotter(lat, lon, 5)

print "Creating markers..."
for result in results['results']:
    lat = float(result['trilat'])
    lon = float(result['trilong'])
    #drop marker for each point
    gmap.marker(lat, lon, color='#FF0000', title=ESSID)

print "Creating wiglemap.html..."
gmap.draw("wiglemap.html")
