import plotly.graph_objs as go

def plot_forecast(forecast_df, streamlit_object):
    fig = go.Figure()

    # Add traces for temperature and humidity
    fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Temperature (°C)'],
                             mode='lines+markers', name='Temperature (°C)'))
    fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Humidity (%)'],
                             mode='lines+markers', name='Humidity (%)', yaxis='y2'))

    # Customize aspects of the layout
    fig.update_layout(
        title='Weather forecast',
        xaxis=dict(
            tickmode='auto',
            nticks=len(forecast_df['Date']),
        ),
        yaxis=dict(
            title='Temperature (°C)',
        ),
        yaxis2=dict(
            title='Humidity (%)',
            overlaying='y',
            side='right'
        )
    )

    streamlit_object.plotly_chart(fig)
