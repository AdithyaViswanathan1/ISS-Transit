import urllib.request as urllib2
import requests
import json
import pandas as pd
import datetime
import geocoder

# Get current location
g = geocoder.ip('me')

lat = str(g.latlng[0])
lon = str(g.latlng[1])
print("Current Latitude", lat)
print("Current Longitude", lon)

# Save query
query = "http://api.open-notify.org/iss-pass.json?lat=" + lat + "&lon=" + lon

# Get info from API
# req = requests.get("http://api.open-notify.org/iss-pass.json?lat=LAT&lon=LON", params=parameters)
req = requests.get(query)

obj = req.json()
#print(obj)

# Save the resulting information
json_list = json.dumps(req.json()['response'])
#print(json_list)

df = pd.read_json(json_list)
#print(type(df))

#Convert seconds into YYYY-MM-DD hh:mm:ss
df['risetime'] = pd.to_datetime(df['risetime'], unit='s')
df['risetime'] = df['risetime'] - datetime.timedelta(hours=6)
df['duration'] /= 60
print(df)