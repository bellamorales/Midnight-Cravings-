import googlemaps
import json
from datetime import datetime
from geo_code import get_coordinates

user_location = (42.556162, -87.825082)
place_type = "restaurant"
user_language = "en-US"
user_region = "US"
radius = 100

client = googlemaps.Client(key='AIzaSyC1H9ZV4GICVuy_rY2sq4BqcQllJoWeKrU')


response = client.places(
    query="restuarant", location=user_location, radius=radius,
    region=user_region, language=user_language, open_now=True,
    type=place_type
    )

nearby_restaurants = {}

for restaurant in response['results']:
    if (restaurant['business_status'] == "OPERATIONAL" 
        and restaurant['opening_hours']['open_now']):
        nearby_restaurants[restaurant['name']] = {
            "place_id": restaurant["place_id"],
            "formatted_address": restaurant["formatted_address"],
            "types": restaurant["types"],
            "price_level": restaurant["price_level"],
            "rating": restaurant["rating"],
            "open_now": restaurant['opening_hours']['open_now']
        }

assert nearby_restaurants["Uptown Restaurant"]["open_now"] == True

# print(json.dumps(response['results'], indent=4))

# parsed = nearby_restaurants

# print(json.dumps(nearby_restaurants, indent=4))
