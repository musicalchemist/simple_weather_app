import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from weather import Weather

weather = Weather()

def main():
    st.title("Local Weather App")  # Add title to the page
    city_name = st.text_input("Please enter the city and state name: ")
    if st.button('Get Weather'):
        st.header(f"Weather Information for {city_name}")

        weather_data = weather.fetch_weather(city_name)
        if weather_data:
            st.header(f"Current Weather in {city_name}:")

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
                            f"{Weather.convert_unix_to_localtime(weather_data['sys']['sunrise'], weather_data['timezone'])}/"
                            f"{Weather.convert_unix_to_localtime(weather_data['sys']['sunset'], weather_data['timezone'])}"
                            f"</h3></div>", unsafe_allow_html=True)

            forecast_data = weather.fetch_forecast(city_name)
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
                fig, ax1 = plt.subplots()
                ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

                color = 'tab:blue'
                ax1.set_xlabel('Date')
                ax1.set_ylabel('Temperature (°C)', color=color)
                ax1.plot(forecast_df['Date'], forecast_df['Temperature (°C)'], 'o-', color=color)
                ax1.tick_params(axis='y', labelcolor=color)

                color = 'tab:green'
                ax2.set_ylabel('Humidity (%)', color=color) 
                ax2.plot(forecast_df['Date'], forecast_df['Humidity (%)'], 'o-', color=color)
                ax2.tick_params(axis='y', labelcolor=color)

                # Set x-ticks manually
                ax1.set_xticks(forecast_df['Date'])

                # Rotation of X-axis labels
                for label in ax1.get_xticklabels():
                    label.set_rotation(45)

                fig.tight_layout()  
                st.pyplot(fig)

            # Log search history...
        else:
            st.error("Error fetching weather information.")

if __name__ == "__main__":
    main()
