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
#print(df)

# Get today's sunrise and sunset times
sun_query = "https://api.sunrise-sunset.org/json?lat=" + lat + "&lng=" + lon + "&date=today"

req = requests.get(sun_query)
obj = req.json()

#print(type(obj))

json_list = json.dumps(req.json()['results'])
loaded_json_list = json.loads(json_list)
#print(type(loaded_json_list))

sunrise = (pd.to_datetime(loaded_json_list['sunrise']) - datetime.timedelta(hours=6))
sunset = (pd.to_datetime(loaded_json_list['sunset']) - datetime.timedelta(hours=6))

print(sunrise, sunset)

acceptable_transit_morning = [(sunrise - datetime.timedelta(hours=2)).time(), sunrise.time()]
acceptable_transit_evening = [sunset.time(), (sunset + datetime.timedelta(hours=2)).time()]
print(acceptable_transit_morning, acceptable_transit_evening)

# Eliminate transit times which are not one hour before sunrise and one hour after sunset


# Send email with list of transit times