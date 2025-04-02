import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load Model and Data ---
@st.cache_data(show_spinner=False)
def load_data():
    with open("models/demand_model.pkl", "rb") as f:
        demand_model = pickle.load(f)

    X_demand = pd.read_csv("data/X_demand.csv", index_col=0, parse_dates=True)
    model_features = X_demand.columns.tolist()

    Y_demand = pd.read_csv("data/Y_demand.csv")
    target_columns = Y_demand.columns.tolist()

    return demand_model, X_demand, model_features, target_columns

demand_model, X_demand, model_features, target_columns = load_data()

# --- Default Weather Values ---
BASE_TEMP = 15.0
BASE_HUMIDITY = 70
BASE_WIND = 5.0
BASE_RAIN = 0.0
BASE_CLOUDS = 50

# --- Scenario Builder ---
def build_scenario_predictions(net_flow_hour, weekday, month, temp, humidity, wind, rain, clouds, selected_team):
    # Use median values from the dataset as defaults
    base_values = {col: X_demand[col].median() for col in model_features}
    df = pd.DataFrame([base_values])

    # Override relevant features
    df["hour"] = net_flow_hour
    df["day_of_week"] = weekday
    df["month"] = month
    df["temp"] = temp
    df["humidity"] = humidity
    df["wind_speed"] = wind
    df["rain_1h"] = rain
    df["clouds_all"] = clouds
    df["baseline"] = 1000

    # Reset team flags
    df["Team_ChicagoBulls"] = 0
    df["Team_FireFC"] = 0
    df["Team_StarsFC"] = 0

    if selected_team == "ChicagoBulls":
        df["Team_ChicagoBulls"] = 1
    elif selected_team == "FireFC":
        df["Team_FireFC"] = 1
    elif selected_team == "StarsFC":
        df["Team_StarsFC"] = 1

    # Fill any missing columns
    for col in set(model_features) - set(df.columns):
        df[col] = 0
    df = df[model_features]

    # Predict and reshape
    preds = demand_model.predict(df)
    preds_df = pd.DataFrame(preds, columns=target_columns)
    return preds_df.melt(var_name="hex_id", value_name="pred_demand")

# --- Color Scaling ---
def compute_rgba(value, min_val, max_val):
    red = np.array([255, 0, 0, 250])
    green = np.array([0, 255, 0, 250])
    blue = np.array([0, 0, 255, 250])

    if np.isclose(value, 0.0):
        return tuple(green)
    elif value < 0:
        ratio = np.clip(value / -6, 0, 1)
        return tuple((green + ratio * (red - green)).astype(int))
    else:
        ratio = np.clip(value / 6, 0, 1)
        return tuple((green + ratio * (blue - green)).astype(int))

# --- Build Pydeck Map ---
def build_deck_for_hour(net_flow_hour, weekday, month, temp, humidity, wind, rain, clouds, selected_team):
    preds = build_scenario_predictions(net_flow_hour, weekday, month, temp, humidity, wind, rain, clouds, selected_team)
    if preds.empty:
        view = pdk.ViewState(latitude=41.8781, longitude=-87.6298, zoom=10, pitch=45)
        return pdk.Deck(layers=[], initial_view_state=view, tooltip={"text": "No data available"})

    preds["adj_demand"] = preds["pred_demand"]
    cmin, cmax = preds["adj_demand"].min(), preds["adj_demand"].max()

    color_df = preds["adj_demand"].apply(lambda x: compute_rgba(x, cmin, cmax))
    color_df = pd.DataFrame(color_df.tolist(), columns=["colorR", "colorG", "colorB", "colorA"])
    preds = pd.concat([preds, color_df], axis=1)
    preds["elev"] = preds["adj_demand"].abs()

    data = preds.to_dict(orient="records")

    layer = pdk.Layer(
        "H3HexagonLayer",
        data=data,
        get_hexagon="hex_id",
        get_elevation="elev",
        elevation_scale=500,
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
        tooltip={"text": "Hex {hex_id}\nPredicted Demand: {adj_demand}"}
    )

# --- Plot Helper: Distribution of Net Flow ---
def plot_net_flow_distribution(net_flow_series):
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.histplot(net_flow_series, bins=30, kde=True, ax=ax, color='gray')
    ax.axvline(0, color='black', linestyle='--')
    ax.set_title("Distribution of Net Trip Flow across Hexes")
    ax.set_xlabel("Net Flow (Trips Start - End)")
    ax.set_ylabel("Hex Count")
    fig.tight_layout()
    return fig

# --- Streamlit Interface ---
st.title("Net Trip Flow Map (6-Hour Window)")

TIME_BINS = [2.5, 8.5, 14.5, 20.5]
TEAM_OPTIONS = ["No Team", "ChicagoBulls", "FireFC", "StarsFC"]

st.sidebar.header("Forecast Settings")
net_flow_hour = st.sidebar.selectbox("6-Hour Net Flow Window (Center Hour)", options=TIME_BINS, index=0)
weekday = st.sidebar.slider("Day of Week", 0, 6, 0)
month = st.sidebar.slider("Month", 1, 12, 1)
temp = st.sidebar.slider("Temperature (°C)", -10.0, 40.0, BASE_TEMP, step=0.5)
humidity = st.sidebar.slider("Humidity (%)", 0, 100, BASE_HUMIDITY)
wind = st.sidebar.slider("Wind Speed (m/s)", 0.0, 20.0, BASE_WIND, step=0.5)
rain = st.sidebar.slider("Rainfall (mm/h)", 0.0, 10.0, BASE_RAIN, step=0.1)
clouds = st.sidebar.slider("Cloud Cover (%)", 0, 100, BASE_CLOUDS)
team = st.sidebar.selectbox("Team", options=TEAM_OPTIONS, index=0)

deck = build_deck_for_hour(net_flow_hour, weekday, month, temp, humidity, wind, rain, clouds, team)
st.pydeck_chart(deck)

# --- Show Global Net Flow Histogram ---
st.subheader("Net Flow Distribution (All Hexes)")
preds = build_scenario_predictions(net_flow_hour, weekday, month, temp, humidity, wind, rain, clouds, team)
fig = plot_net_flow_distribution(preds["pred_demand"])
st.pyplot(fig)