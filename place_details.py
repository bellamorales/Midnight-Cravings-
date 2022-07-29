from urllib import response
import googlemaps
import json
from datetime import datetime
from geo_code import get_coordinates

client = googlemaps.Client(key='AIzaSyC1H9ZV4GICVuy_rY2sq4BqcQllJoWeKrU')


def get_nearby_restaurants(
    location, user_lang="en-US", user_region="US", radius=500, limit=-1,
    types=["restaurant", "meal_delivery", "meal_takeaway"]
    ) -> dict:
    """
    Retrieves nearby restaurants that are open right now.

    :param location: The latitude/longitude value for which you wish to obtain the
                     closest, human-readable address.
    :type location: string, dict, list, or tuple

    :param user_lang: The language in which to return results, optional parameter.
    :type user_lang: string

    :param user_region: The region code, optional parameter.
        See more @ https://developers.google.com/places/web-service/search

    :type user_region: string

    :param limit: The number of results to return, optional parameter.
    :type limit: int

    :param types: Restricts the results to places matching the specified type, optional parameter.
        The full list of supported types is available here:
        https://developers.google.com/places/supported_types

    :type types: string, list of strings

    :param radius: Distance in meters within which to bias results, optional parameter.
    :type radius: int

    :rtype: result list of dicts with the following keys:
        place_id: string identifying restaurant in Google's Places API
        formatted_address: string
        types: list of strings identifying services at and classification of restaurant 
        price_level: int on scale of 0 (least expensive) to 4 (most expensive)
        rating: float on scale of 0-5 
        open_now: boolean
    """
    # Make request using google places API python library
    response = client.places(
        query="restuarant", location=location, radius=radius,
        region=user_region, language=user_lang, open_now=True,
        type=types
        )

    if response["status"] != "OK":
        return {}

    results = response["results"]    

    nearby_restaurants = []

    if limit != -1 and limit > 0:
        results = results[0: limit]

    for restaurant in results:
        # Only return restaurants that are both operational and open now. 
        if (restaurant['business_status'] == "OPERATIONAL" 
            and restaurant['opening_hours']['open_now']):
            r = {
                "name": restaurant["name"],
                "place_id": restaurant["place_id"],
                "formatted_address": restaurant["formatted_address"],
                "types": restaurant["types"],
                "price_level": restaurant["price_level"],
                "rating": restaurant["rating"],
                "open_now": restaurant['opening_hours']['open_now']
            }

            nearby_restaurants.append(r)

    return nearby_restaurants


# restaurants = get_nearby_restaurants((42.55711747257572, -87.82794582470426), limit=100)

# print(json.dumps(restaurants, indent=4))

# assert nearby_restaurants["Uptown Restaurant"]["open_now"] == True

# print(json.dumps(response['results'], indent=4))

# parsed = nearby_restaurants

# print(json.dumps(nearby_restaurants, indent=4))
