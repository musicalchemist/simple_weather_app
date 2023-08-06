# Simple Weather App

## Overview

Simple Weather App is a Python-based web application built with Streamlit. It fetches and displays the current weather and a 3-day forecast for any given city. The weather data includes temperature and humidity information, which is represented both in a table and graphically.

## Features

- Fetch and display current weather and a 3-day forecast for a city.
- Graphical representation of temperature and humidity for the forecast period.
- Convert Unix timestamps to the local time according to the city's timezone.

## Getting Started

### Prerequisites

- Python 3.8 or later
- Anaconda or Miniconda
- Streamlit
- OpenWeatherMap API key
- Google Maps API key

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/musicalchemist/simple_weather_app.git
   ```

2. Create and activate a new conda environment:

   ```
   conda create -n weather_app python=3.8
   conda activate weather_app
   ```

3. Install required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root of the project and add your API keys:

   ```
   OPENWEATHERAPIKEY=your_openweathermap_api_key
   GOOGLEMAPKEY=your_google_maps_api_key
   ```

5. Run the app:
   ```
   streamlit run src/main.py
   ```

## Usage

1. Enter a city and state in the input field.
2. The app fetches and displays the current weather and a 3-day forecast of temperature and humidity.
3. The sunrise and sunset times are shown in the local time of the entered city.

## Built With

- Python
- Streamlit
- OpenWeatherMap API
- Google Maps Geocoding API
- Matplotlib
- Pandas
