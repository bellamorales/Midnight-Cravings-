import requests
import json
import sqlalchemy as db
import pandas as pd

import requests

url = "https://api.content.tripadvisor.com/api/v1/location/nearby_search?language=en"

headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)