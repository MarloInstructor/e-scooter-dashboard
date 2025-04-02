import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib

# --- Load Data ---
X_forecasting = pd.read_csv("data/data.csv")
train_pred_df = pd.read_csv("data/train_pred_df.csv")

# --- Load Trained Model ---
boost_model = joblib.load("models/boost_model.pkl")

# --- Prepare Forecasting Data ---
X_forecasting['baseline'] = train_pred_df['yhat'].rolling(window=74).mean()
X_forecasting.dropna(subset=['baseline'], inplace=True)
X_forecasting.set_index('ds', inplace=True)

X_train = X_forecasting[X_forecasting['y'].notna()].copy()
y_train = X_train.pop('y')

# --- Sidebar Controls ---
st.sidebar.header("Customize Forecast Scenario")

day_of_week = st.sidebar.slider("Day of Week", 0, 6, 1)
month = st.sidebar.slider("Month", 1, 12, 8)
start_hour = st.sidebar.slider("Start Hour", 0, 21, 10)

custom_temp = st.sidebar.slider("Temperature (°C)", -10.0, 40.0, 15.0, step=0.5)
custom_rain = st.sidebar.slider("Rainfall (mm/h)", 0.0, 40.0, 0.0, step=1.0)
custom_snow = st.sidebar.slider("Snowfall (mm/h)", 0.0, 7.0, 0.0, step=1.0)
custom_wind = st.sidebar.slider("Wind Speed (m/s)", 0.0, 20.0, 2.0, step=0.5)
custom_humidity = st.sidebar.slider("Humidity (%)", 0, 100, 50, step=1)

# --- Helper to Create Scenario DataFrame ---
def make_scenario_df(X_train, day_of_week, month, start_hour, temp, rain, snow, wind, humidity):
    df = pd.DataFrame({'hour': range(24)})
    df['day_of_week'] = day_of_week
    df['month'] = month
    df['temp'] = 15.0
    df['rain_1h'] = 0.0
    df['snow_1h'] = 0.0
    df['wind_speed'] = 2.0
    df['humidity'] = 50

    # Fill in any missing columns
    for col in X_train.columns:
        if col not in df.columns:
            df[col] = X_train[col].mode()[0]

    # Apply custom values to the 3-hour window
    mask = (df['hour'] >= start_hour) & (df['hour'] <= start_hour + 2)
    df.loc[mask, 'temp'] = temp
    df.loc[mask, 'rain_1h'] = rain
    df.loc[mask, 'snow_1h'] = snow
    df.loc[mask, 'wind_speed'] = wind
    df.loc[mask, 'humidity'] = humidity

    # Set baseline, cap, and floor
    df['baseline'] = 3000
    df['cap'] = X_train['cap'].max()
    df['floor'] = X_train['floor'].min()

    return df[X_train.columns]

# --- Prediction Helper ---
def predict(df):
    return boost_model.predict(df)

# --- Plotting ---
def plot_forecast():
    custom_df = make_scenario_df(
        X_train, day_of_week, month, start_hour,
        custom_temp, custom_rain, custom_snow, custom_wind, custom_humidity
    )
    baseline_df = make_scenario_df(
        X_train, day_of_week, month, start_hour,
        15.0, 0.0, 0.0, 2.0, 50
    )

    custom_preds = predict(custom_df)
    baseline_preds = predict(baseline_df)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=custom_df['hour'], y=custom_preds,
        mode='lines+markers', name='Custom Scenario', line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=baseline_df['hour'], y=baseline_preds,
        mode='lines+markers', name='Baseline', line=dict(color='black', dash='dash')
    ))

    fig.update_layout(
        title=f"Forecast Comparison (Start Hour: {start_hour})",
        xaxis_title="Hour of Day",
        yaxis_title="Predicted Trip Count",
        xaxis=dict(tickmode='linear', dtick=1),
        shapes=[
            dict(
                type="rect", xref="x", yref="paper",
                x0=start_hour, x1=start_hour + 2, y0=0, y1=1,
                fillcolor="lightblue", opacity=0.3, layer="below", line_width=0
            )
        ]
    )

    return fig

# --- Show Plot ---
st.plotly_chart(plot_forecast())

# Optional: Export as HTML
# st.download_button("Download Plot", data=open("plot.html", "rb"), file_name="forecast_plot.html", mime="text/html")
