import unittest
from place_details import get_nearby_restaurants

class TestFindPlaces(unittest.TestCase):
    def setUp(self):
        response = get_nearby_restaurants()

if __name__ == "__main__":
    unittest.main()