import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from weather import Weather

weather = Weather()

def main():
    city_name = st.text_input("Please enter the city name: ")
    if st.button('Get Weather'):
        st.title(f"Weather Information for {city_name}")

        weather_data = weather.fetch_weather(city_name)
        if weather_data:
            st.header(f"Current Weather in {city_name}:")

            # Card-like layout for weather data
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"<div style='background-color: #f5f5f5; padding: 10px; border-radius: 10px;'>"
                            f"<h3 style='color: black;'>Weather</h3>"
                            f"<h2 style='color: black;'>{weather_data['weather'][0]['description'].upper()}</h2></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='background-color: #f5f5f5; padding: 10px; border-radius: 10px;'>"
                            f"<h3 style='color: black;'>Temperature</h3>"
                            f"<h2 style='color: black;'>{weather_data['main']['temp']}°C</h2></div>", unsafe_allow_html=True)
            
            forecast_data = weather.fetch_forecast(city_name)
            if forecast_data:
                st.subheader("3-Day Forecast:")
                # Parse date string to only include date (not time)
                dates = [datetime.datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S').date() for forecast in forecast_data]
                temps = [forecast['main']['temp'] for forecast in forecast_data]
                descriptions = [forecast['weather'][0]['description'] for forecast in forecast_data]

                # Create a DataFrame for the forecast data
                forecast_df = pd.DataFrame({
                    'Date': dates,
                    'Weather': descriptions,
                    'Temperature (°C)': temps
                })

                # Display forecast data as a table
                st.table(forecast_df)
                
                # Plotting forecast data
                fig, ax = plt.subplots()
                ax.plot(forecast_df['Date'], forecast_df['Temperature'], marker='o')
                ax.set_xlabel('Date')
                ax.set_ylabel('Temperature (°C)')
                ax.set_title('3-Day Temperature Forecast')
                plt.xticks(rotation=45)
                ax.xaxis.set_major_locator(plt.MaxNLocator(3))  # Reduce number of x-axis ticks
                st.pyplot(fig)

            # Log search history...
        else:
            st.error("Error fetching weather information.")

if __name__ == "__main__":
    main()

