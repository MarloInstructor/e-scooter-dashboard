import streamlit as st
import pandas as pd
import pydeck as pdk
import pickle

# --- Load Model and Data ---
@st.cache_resource
def load_model():
    with open("models/xgb_model.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_data():
    X_hex = pd.read_csv("data/X_hex.csv", index_col=0, parse_dates=True)
    Y_hex = pd.read_csv("data/Y_hex.csv")
    return X_hex, Y_hex

xgb_model = load_model()
X_hex, Y_hex = load_data()
model_features = X_hex.columns.tolist()
target_columns = Y_hex.columns.tolist()

# --- Default Weather Values ---
BASE_TEMP = 15.0
BASE_HUMIDITY = 70
BASE_WIND = 5.0
BASE_RAIN = 0.0
BASE_CLOUDS = 50

# --- Build Scenario Predictions ---
def build_scenario_predictions(hour, day_of_week, month, temp, humidity, wind, rain, clouds, selected_team=None):
    """
    Create a scenario DataFrame using most frequent values,
    override scenario-relevant features, and return melted predictions.
    """
    # Start from mode values for all features
    most_frequent = {col: X_hex[col].mode()[0] for col in model_features}
    df = pd.DataFrame([most_frequent])

    # Override weather and time features
    df["hour"] = hour
    df["day_of_week"] = day_of_week
    df["month"] = month
    df["temp"] = temp
    df["humidity"] = humidity
    df["wind_speed"] = wind
    df["rain_1h"] = rain
    df["clouds_all"] = clouds

    # --- Dynamically set baseline to mean of selected month ---
    baseline_month = X_hex[X_hex["month"] == month]
    if not baseline_month.empty and "baseline" in baseline_month.columns:
        df["baseline"] = baseline_month["baseline"].mean()
    else:
        df["baseline"] = X_hex["baseline"].mean()  # fallback if month filter returns nothing

    # Reset all team flags to 0
    df["Team_ChicagoBulls"] = 0
    df["Team_FireFC"] = 0
    df["Team_StarsFC"] = 0

    # Set selected team flag
    if selected_team:
        df[f"Team_{selected_team}"] = 1

    preds = xgb_model.predict(df[model_features])
    preds_df = pd.DataFrame(preds, columns=target_columns)
    return preds_df.melt(var_name="hex_id", value_name="pred_trip")

# --- Map Coloring ---
def compute_rgba(count, cmin, cmax):
    if cmax == cmin:
        return (128, 128, 128, 255)
    ratio = (count - cmin) / (cmax - cmin)
    r = int(255 * ratio)
    g = int(255 * (1 - ratio))
    return (r, g, 0, 255)

# --- Build Pydeck Layer ---
def build_deck_for_hour(hour, day_of_week, month, temp, humidity, wind, rain, clouds):
    preds = build_scenario_predictions(hour, day_of_week, month, temp, humidity, wind, rain, clouds)

    cmin, cmax = preds["pred_trip"].min(), preds["pred_trip"].max()
    color_df = preds["pred_trip"].apply(lambda x: compute_rgba(x, cmin, cmax))
    color_df = pd.DataFrame(color_df.tolist(), columns=["colorR", "colorG", "colorB", "colorA"])
    preds = pd.concat([preds, color_df], axis=1)

    data = preds.to_dict(orient="records")

    layer = pdk.Layer(
        "H3HexagonLayer",
        data=data,
        get_hexagon="hex_id",
        get_elevation="pred_trip",
        elevation_scale=100,
        extruded=True,
        coverage=1,
        pickable=True,
        get_fill_color=["colorR", "colorG", "colorB", "colorA"]
    )

    view = pdk.ViewState(latitude=41.8781, longitude=-87.6298, zoom=10, pitch=45)
    return pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        map_provider="carto",
        map_style="light",
        tooltip={"text": "Hex {hex_id}\nPredicted Trips: {pred_trip}"}
    )

# --- Streamlit Interface ---
st.title("Trip Distribution by Hour")

st.sidebar.header("Forecast Settings")
hour = st.sidebar.slider("Hour", 0, 23, 0)
day_of_week = st.sidebar.slider("Day of Week", 0, 6, 0)
month = st.sidebar.slider("Month", 1, 12, 1)
temp = st.sidebar.slider("Temperature (°C)", -10.0, 40.0, BASE_TEMP, step=0.5)
humidity = st.sidebar.slider("Humidity (%)", 0, 100, BASE_HUMIDITY)
wind = st.sidebar.slider("Wind Speed (m/s)", 0.0, 20.0, BASE_WIND, step=0.5)
rain = st.sidebar.slider("Rainfall (mm/h)", 0.0, 10.0, BASE_RAIN, step=0.1)
clouds = st.sidebar.slider("Cloud Cover (%)", 0, 100, BASE_CLOUDS)

deck = build_deck_for_hour(hour, day_of_week, month, temp, humidity, wind, rain, clouds)
st.pydeck_chart(deck)
