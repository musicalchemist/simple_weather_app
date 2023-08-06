import requests
from dotenv import load_dotenv, find_dotenv
import os
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from tzwhere.tzwhere import tzwhere
import pytz
from pytz import timezone
from geopy.geocoders import GoogleV3
from timezonefinder import TimezoneFinder

class Weather:
    def __init__(self):
        # load environment variables from .env file
        load_dotenv() #path to env file
        _ = load_dotenv(find_dotenv())
        self.weather_api_key = os.environ['OPENWEATHERAPIKEY']
        self.map_api_key = os.environ['GOOGLEMAPKEY']
        self.base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
        self.forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric'
        self.geolocator = GoogleV3(api_key=self.map_api_key)  # initialize the geolocator attribute
        self.tf = TimezoneFinder()

    def fetch_weather(self, city_name):
        url = self.base_url.format(city_name, self.weather_api_key)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_forecast(self, city_name, days=3):
        url = self.forecast_url.format(city_name, self.weather_api_key)
        response = requests.get(url)
        if response.status_code == 200:
            # Filter the forecast for the number of days requested
            forecast_data = response.json()
            return [forecast_data['list'][i] for i in range(0, days*8, 8)]
        else:
            return None
        
    @staticmethod
    def convert_unix_to_time(unix_time):
        return datetime.utcfromtimestamp(unix_time).strftime('%H:%M:%S')
    
    def convert_unix_to_localtime(self, unix_time, city):
        try:
            location = self.geolocator.geocode(city)
            tz_str = self.tf.timezone_at(lng=location.longitude, lat=location.latitude)  # get the timezone from the latitude and longitude
            local_tz = pytz.timezone(tz_str)
            local_dt = datetime.fromtimestamp(unix_time, local_tz)
            return local_dt.strftime('%H:%M:%S')
        except GeocoderTimedOut:
            return "Error: geocode failed on input %s with message %s"%(city, "Timed out")