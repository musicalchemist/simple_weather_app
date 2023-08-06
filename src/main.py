import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from weather import Weather
from session import SessionState
from visuals import plot_forecast

weather = Weather()

@st.cache_data
def get_search_history():
    return []

def main():
    # Get the search history list. This will be preserved between runs thanks to st.cache
    search_history = get_search_history()

    # Create an instance of the SessionState
    session_state = SessionState()

    st.title("Local Weather App")  # Add title to the page
    city_state = st.text_input("Please enter the city and state name: ")

    if st.button('Get Weather'):
        # If this is not the first search, add the current search term to the session state
        if city_state:  # assuming an empty city_state shouldn't be added
            search_history.append(city_state)

        # # Store the current search term in the session state
        # session_state.last_search = city_state

        # Now the 'Get Weather' button was pressed, do the search and display the weather
        st.header(f"Weather Information for {city_state}")

        weather_data = weather.fetch_weather(city_state)
        if weather_data:
            st.header(f"Current Weather in {city_state}:")

            # Card-like layout for weather data
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                st.markdown(f"<div style='background-color: #f5f5f5; padding: 10px; border-radius: 10px; text-align: center;'>"
                            f"<h4 style='color: black;'>Weather</h4>"
                            f"<h3 style='color: black; font-size: medium; word-wrap: break-word;'>{weather_data['weather'][0]['description'].upper()}</h3></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='background-color: #f5f5f5; padding: 10px; border-radius: 10px; text-align: center;'>"
                            f"<h4 style='color: black;'>Temperature</h4>"
                            f"<h3 style='color: black; font-size: medium; word-wrap: break-word;'>{weather_data['main']['temp']}°C</h3></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div style='background-color: #f5f5f5; padding: 10px; border-radius: 10px; text-align: center;'>"
                            f"<h4 style='color: black;'>Humidity</h4>"
                            f"<h3 style='color: black; font-size: medium; word-wrap: break-word;'>{weather_data['main']['humidity']}%</h3></div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)  # Empty line

            col4, col5 = st.columns([1,1])
            with col4:
                st.markdown(f"<div style='background-color: #f5f5f5; padding: 10px; border-radius: 10px; text-align: center;'>"
                            f"<h4 style='color: black;'>Wind Speed</h4>"
                            f"<h3 style='color: black; font-size: medium; word-wrap: break-word;'>{weather_data['wind']['speed']} m/s</h3></div>", unsafe_allow_html=True)
            with col5:
                st.markdown(f"<div style='background-color: #f5f5f5; padding: 10px; border-radius: 10px; text-align: center;'>"
                            f"<h4 style='color: black;'>Sunrise/Sunset</h4>"
                            f"<h3 style='color: black; font-size: medium; word-wrap: break-word;'>"
                            f"{weather.convert_unix_to_localtime(weather_data['sys']['sunrise'], weather_data['timezone'])}/"
                            f"{weather.convert_unix_to_localtime(weather_data['sys']['sunset'], weather_data['timezone'])}"
                            f"</h3></div>", unsafe_allow_html=True)

            forecast_data = weather.fetch_forecast(city_state)
            if forecast_data:
                st.subheader("3-Day Forecast:")
                # Parse date string to only include date (not time)
                dates = [datetime.datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S').date() for forecast in forecast_data]
                temps = [forecast['main']['temp'] for forecast in forecast_data]
                descriptions = [forecast['weather'][0]['description'] for forecast in forecast_data]
                wind_speeds = [forecast['wind']['speed'] for forecast in forecast_data]
                humidities = [forecast['main']['humidity'] for forecast in forecast_data]

                # Create a DataFrame for the forecast data
                forecast_df = pd.DataFrame({
                    'Date': dates,
                    'Weather': descriptions,
                    'Temperature (°C)': temps,
                    'Wind Speed (m/s)': wind_speeds,
                    'Humidity (%)': humidities
                })

                # Display forecast data as a table
                st.table(forecast_df)

                # Plotting forecast data
                plot_forecast(forecast_df, st)

        else:
            st.error("Error fetching weather information.")

    st.sidebar.header("Search History")
    for search in search_history:
        if st.sidebar.button(search):
            # This will re-enter the search term into the text box, triggering a new search
            city_state = search

if __name__ == "__main__":
    main()
