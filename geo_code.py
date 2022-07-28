import requests
import os
import pandas as pd
import sqlalchemy as db

# Main purpose of this code is to get the 
# latitude and longitude of an inputted city
# to input it into the Google Maps API

def get_coordinates(city):
        params = {
            # 'key': os.environ.get('WEATHERAPI_API_KEY'),
            'key': '51872ff903844da98c321057220607',
            'q': str(city),
            'days': '1',
            'aqi': "no",
            'alerts': "no"}
        BASE_URL = 'https://api.weatherapi.com/v1/forecast.json?'
        r = requests.get(BASE_URL, params)
        r = r.json()
        latitude = r["location"]["lat"]
        longitude = r["location"]["lon"]
        return (latitude, longitude)

# Testing case:
# city = "New York"
# print(get_info_to_parse(city))


