from requests import request
from urllib.parse import urlencode


class GoogleMapsClient:
    lat = None
    lng = None
    data_type = 'json'
    location_query = None
    api_key = None

    def __init__(self, api_key=None, address_or_zip=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        if self.api_key is None:
            raise Exception("API key is required!")
        self.location_query = address_or_zip
        if self.location_query is not None:
            self.extract_lat_lng()

    @staticmethod
    def response(endpoint, params):
        """Get a response based on a constructed endpoint url."""
        url_params = urlencode(params)
        url = "{}?{}".format(endpoint, url_params)
        response = request('GET', url)
        if response.status_code not in range(200, 299):
            raise Exception('The request is failed!')

        return response.json()

    def extract_lat_lng(self, location=None):
        """Get a tuple of (latitude, longitude) from an address or a viewport"""
        geocode = {}

        loc_query = self.location_query
        if location is not None:
            loc_query = location

        endpoint = "https://maps.googleapis.com/maps/api/geocode/{}".format(self.data_type)
        params = {"address": loc_query, "key": self.api_key}
        response = self.response(endpoint, params)
        try:
            geocode = response['results'][0]['geometry']['location']
        except:
            return response['error_message']

        lat, lng = geocode.get('lat'), geocode.get('lng')
        self.lat = lat
        self.lng = lng

        return lat, lng

    def nearby_search(self, keyword='Chinese Restaurant', location=None, radius=1000):
        """Search the nearly places based on a given keyword"""
        lat, lng = self.lat, self.lng
        if location is not None:
            lat, lng = self.extract_lat_lng()
        endpoint = f"https://maps.googleapis.com/maps/api/place/nearbysearch/{self.data_type}"
        params = {
            'key': self.api_key,
            'location': f'{lat}, {lng}',
            'radius': radius,
            'keyword': keyword
        }

        return self.response(endpoint, params)

    def detail_place_info(self, place_id=None):
        """Retrieve the detailed place information based on a given place ID"""
        endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': f'{place_id}',
            'fields': 'formatted_address,name,rating,formatted_phone_number',
            'key': self.api_key
        }

        return self.response(endpoint, params)

    def get_top_5_places(self):
        """Retrieve the detailed information of top 5 places based on rating"""
        restaurant_list = self.nearby_search()
        top5_restaurant = sorted(restaurant_list['results'], reverse=True,
                                 key=lambda k: ('rating' not in k, k.get('rating')))[:5]
        place_id_list = [r['place_id'] for r in top5_restaurant]
        stores = [self.detail_place_info(id)['result'] for id in place_id_list]

        return stores
