import googlemaps
import json
from datetime import datetime



user_location = (42.556162, -87.825082)
place_type = "restaurant"
user_language = "en-US"
user_region = "US"
radius = 100

client = googlemaps.Client(key='AIzaSyC1H9ZV4GICVuy_rY2sq4BqcQllJoWeKrU')


nearby_restaurants = client.places(
    query="restuarant", location=user_location, radius=radius,
    region=user_region, language=user_language, open_now=True,
    type=place_type
    )

print(nearby_restaurants.keys())

# parsed = nearby_restaurants

# print(json.dumps(nearby_restaurants, indent=4))
