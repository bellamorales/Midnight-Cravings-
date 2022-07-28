import googlemaps
import json
from datetime import datetime
from geo_code import get_coordinates

client = googlemaps.Client(key='AIzaSyC1H9ZV4GICVuy_rY2sq4BqcQllJoWeKrU')


def get_nearby_restaurants(
    location, user_lang="en-US", user_region="US", radius=50
    ):
    """
    Returns: dict of nearby restaurants as nearby_restaurants
        Keys:
            "place_id": string identifying restaurant in Google's Places API
            "formatted_address": string
            "types": list of strings identifying services at and classification of restaurant 
            "price_level": int on scale of 0 (least expensive) to 4 (most expensive)
            "rating": float on scale of 0-5 
            "open_now": boolean

    """
    response = client.places(
        query="restuarant", location=location, radius=radius,
        region=user_region, language=user_lang, open_now=True,
        type="restaurant"
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

    return nearby_restaurants



# assert nearby_restaurants["Uptown Restaurant"]["open_now"] == True

# print(json.dumps(response['results'], indent=4))

# parsed = nearby_restaurants

# print(json.dumps(nearby_restaurants, indent=4))
