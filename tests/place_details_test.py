import unittest
from place_details import get_nearby_restaurants

class TestFindPlaces(unittest.TestCase):
    def setUp(self):
        kenosha = get_nearby_restaurants((42.566195, -87.835055), limit=10)


if __name__ == "__main__":
    unittest.main()