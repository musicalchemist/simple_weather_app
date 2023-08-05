import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from weather import Weather

weather = Weather()

def main():
    city_name = st.text_input("Please enter the city name: ")
    if st.button('Get Weather'):
        st.title(f"Weather Information for {city_name}")

        weather_data = weather.fetch_weather(city_name)
        if weather_data:
            st.header(f"Current Weather in {city_name}:")
            st.markdown(f"**{weather_data['weather'][0]['description']}**")
            st.markdown(f"**Temperature:** {weather_data['main']['temp']}°C")
            
            forecast_data = weather.fetch_forecast(city_name)
            if forecast_data:
                st.subheader("3-Day Forecast:")
                dates = [forecast['dt_txt'] for forecast in forecast_data]
                temps = [forecast['main']['temp'] for forecast in forecast_data]
                descriptions = [forecast['weather'][0]['description'] for forecast in forecast_data]

                for date, desc, temp in zip(dates, descriptions, temps):
                    st.markdown(f"**Date:** {date}")
                    st.markdown(f"**Weather:** {desc}")
                    st.markdown(f"**Temperature:** {temp}°C")

                # Create a DataFrame for the forecast data
                forecast_df = pd.DataFrame({
                    'Date': dates,
                    'Temperature': temps
                })
                
                # Convert the 'Date' column to datetime for plotting
                forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
                
                # Create a line plot of the forecast temperatures
                fig, ax = plt.subplots()
                ax.plot(forecast_df['Date'], forecast_df['Temperature'], marker='o')
                ax.set_xlabel('Date')
                ax.set_ylabel('Temperature (°C)')
                ax.set_title('3-Day Temperature Forecast')
                st.pyplot(fig)

            # Log search history...
        else:
            st.error("Error fetching weather information.")

if __name__ == "__main__":
    main()
