import requests
from dotenv import load_dotenv, find_dotenv
import os

class Weather:
    def __init__(self):
        # load environment variables from .env file
        load_dotenv() #path to env file
        _ = load_dotenv(find_dotenv())
        self.api_key = os.environ['OPENWEATHERAPIKEY']
        self.base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'
        self.forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric'

    def fetch_weather(self, city_name):
        url = self.base_url.format(city_name, self.api_key)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_forecast(self, city_name, days=3):
        url = self.forecast_url.format(city_name, self.api_key)
        response = requests.get(url)
        if response.status_code == 200:
            # Filter the forecast for the number of days requested
            forecast_data = response.json()
            return [forecast_data['list'][i] for i in range(0, days*8, 8)]
        else:
            return None
