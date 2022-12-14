from urllib import response, error
import googlemaps
import json
from datetime import datetime
from geo_code import get_coordinates

client = googlemaps.Client(key='AIzaSyC1H9ZV4GICVuy_rY2sq4BqcQllJoWeKrU')


def get_nearby_restaurants(
    location, user_lang="en-US", user_region="US", radius=5000, limit=0,
    types=["restaurant", "meal_delivery", "meal_takeaway"]
    ):
    """Retrieves nearby restaurants that are open right now.

    :param location: The latitude/longitude value for which you wish to obtain the
                     closest, human-readable address.
    :type location: str, dict, list, or tuple

    :param user_lang: The language in which to return results, optional parameter.
    :type user_lang: str

    :param user_region: The region code, optional parameter.
        See more @ https://developers.google.com/places/web-service/search

    :type user_region: str

    :param limit: The number of results to return, optional parameter.
    :type limit: int

    :param types: Restricts the results to places matching the specified type, optional parameter.
        The full list of supported types is available here:
        https://developers.google.com/places/supported_types

    :type types: list of str

    :param radius: Distance in meters within which to bias results, optional parameter.
    :type radius: int

    :rtype: list of dicts with the following keys:
        place_id: str identifying restaurant in Google's Places API
        formatted_address: str
        types: list of str identifying services at and classification of restaurant 
        price_level: int on scale of 0 (least expensive) to 4 (most expensive)
        rating: float on scale of 0-5 
        open_now: boolean
    """
    # Make request using google places API python library
    api_response = client.places(
        query="restuarant", location=location, radius=radius,
        region=user_region, language=user_lang, open_now=True,
        type=types
        )

    # return value is list of dicts of open nearby restaurants 
    nearby_restaurants = []
    message = None

    while True:
        if api_response["status"] != "OK":
            return nearby_restaurants
        # list of dicts representing restaurants returned by request 
        restaurant_results = api_response["results"]

        # print(json.dumps(restaurant_results, indent=4))

        # filter out only the data we want (see below) from the result data 
        for restaurant in restaurant_results:
            # Only return restaurants that are both operational and open now. 
            if restaurant['business_status'] == "OPERATIONAL":
                # data we want: name, place_id, formatted_address, types,
                # price_level, rating, open_now
                r = {
                    "name": restaurant["name"],
                    "place_id": restaurant["place_id"],
                    "formatted_address": restaurant["formatted_address"],
                    "types": restaurant["types"],
                    'url': "https://www.google.com/maps/search/?api=1&query=" + restaurant["name"] +"&query_place_id=" + restaurant["place_id"],
                    # "url":restaurant["photos"][0]["html_attributions"],
                    # "price_level": restaurant["price_level"],
                    "rating": restaurant["rating"],
                    "open_now": restaurant['opening_hours']['open_now']
                }
                # url contruction using name and place_id
                name = r["name"]
                url_name = name.replace(" ", "+")
                url_name = url_name.replace(",", "%2C")
                url_name = url_name.replace("&", "%26")

                r['url'] = "https://www.google.com/maps/search/?api=1&query=" + url_name +"&query_place_id=" + restaurant["place_id"],

                nearby_restaurants.append(r)

        try:
            if api_response["next_page_token"]:
                api_response = client.places(
                    page_token=api_response["next_page_token"]
                )
        except KeyError:
            break
        except googlemaps.exceptions.ApiError:
            message = f"ERRORED WITH NEXT_PAGE_TOKEN: {api_response['next_page_token']}"
            break


    if type(limit) == int and limit > 0:
        nearby_restaurants = nearby_restaurants[0: limit]
    
    if message is not None:
        nearby_restaurants.append(message)

    return nearby_restaurants


# restaurants = get_nearby_restaurants((42.580842, -87.821801))
# print(restaurants)

# print(json.dumps(restaurants, indent=4))
# print(len(restaurants))

# assert nearby_restaurants["Uptown Restaurant"]["open_now"] == True

# print(json.dumps(response['results'], indent=4))

# parsed = nearby_restaurants

# print(json.dumps(nearby_restaurants, indent=4))
