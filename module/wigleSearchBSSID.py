#!/usr/bin/python
from gmplot import gmplot
import sys
import requests
import json
from requests.auth import HTTPBasicAuth

wigle_username = sys.argv[1]
wigle_password = sys.argv[2]
BSSID = sys.argv[3]

payload = {'netid': BSSID, 'api_key': (wigle_username + wigle_password).encode('base64','strict')}
results = requests.get(url='https://api.wigle.net/api/v2/network/search', params=payload, auth=HTTPBasicAuth(wigle_username, wigle_password)).json()

lat = 0.0
lon = 0.0

for result in results['results']:
    lat = float(result['trilat'])
    lon = float(result['trilong'])

print"Creating map..."
#setup map in AoI
gmap = gmplot.GoogleMapPlotter(lat, lon, 6)
gmap.marker(lat, lon, color='#FF0000', title=BSSID)

#detail search aka every observation
results = requests.get(url='https://api.wigle.net/api/v2/network/detail', params=payload, auth=HTTPBasicAuth(wigle_username, wigle_password))
json_data = json.loads(results.text)

print "Creating markers..."
for x in json_data[u'results']:
  for y in x[u'locationData']:
    #drop marker
    gmap.marker(y[u'latitude'], y[u'longitude'], color='#FF0000', title=BSSID)

print "Creating wiglemap.html..."
gmap.draw("wiglemap.html")


