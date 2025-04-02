import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error

#############################
# Extended E-Scooter Dashboard
# Combines:
# 1) High-level overview & forecast
# 2) Monthly map & hex details
# 3) Trip patterns & usage analysis
# 4) Forecast error analysis
# Now with integrated month & hex selection in-page and labeled for accessibility.
#############################

st.set_page_config(layout="wide")

#############################
# CSS Tweaks
#############################
st.markdown(
    """
    <style>
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#############################
# 1) Data Loading
#############################
@st.cache_data
def load_hex_data():
    df = pd.read_csv("data/hex_toolpin.csv")
    df["year_month"] = pd.to_datetime(df["year_month"].astype(str).str.strip(), format="%Y-%m")
    return df


@st.cache_data
def load_forecast_data():
    df = pd.read_csv("data/X_forecasting.csv", parse_dates=["ds"])
    df.set_index("ds", inplace=True)
    return df

hex_data = load_hex_data()
X_forecasting = load_forecast_data()

#############################
# 2) Create Tabs
#############################
st.title("E-Scooter Historical & Forecast Dashboard")
tab_overview, tab_map, tab_patterns, tab_analysis = st.tabs([
    "High-Level Overview",
    "Monthly Hex Map",
    "Usage Patterns",
    "Forecast Analysis"
])

#############################
# HELPER: RGBA for Map
#############################
def compute_rgba(count, cmin, cmax):
    if cmax == cmin:
        return (128, 128, 128, 255)
    ratio = (count - cmin) / (cmax - cmin)
    r = int(255 * ratio)
    g = int(255 * (1 - ratio))
    return (r, g, 0, 250)

#############################
# HELPER: Build Monthly Map
#############################
def build_deck_for_month(ym, highlight_hex=None):
    df_month = hex_data[hex_data["year_month"] == ym].copy()
    if df_month.empty:
        return None, df_month

    # Use fixed color scale across months (hardcoded or percentiles)
    cmin = df_month["trip_count"].min()
    cmax = df_month["trip_count"].max()

    def compute_rgba(count):
        if cmax == cmin:
            return (128, 128, 128, 255)
        ratio = min(max((count - cmin) / (cmax - cmin), 0), 1)
        r = int(255 * ratio)
        g = int(255 * (1 - ratio))
        return (r, g, 0, 250)

    color_df = df_month["trip_count"].apply(compute_rgba).apply(pd.Series)
    color_df.columns = ["colorR", "colorG", "colorB", "colorA"]
    df_month = pd.concat([df_month, color_df], axis=1)

    # Highlight selected hex in bright blue
    if highlight_hex:
        df_month.loc[df_month.hex_id == highlight_hex, ["colorR", "colorG", "colorB", "colorA"]] = [0, 0, 255, 255]

    hex_layer = pdk.Layer(
        "H3HexagonLayer",
        data=df_month,
        get_hexagon="hex_id",
        get_elevation="trip_count",
        elevation_scale=0.5,
        extruded=True,
        coverage=1,
        pickable=True,
        get_fill_color=["colorR", "colorG", "colorB", "colorA"]
    )

    view = pdk.ViewState(latitude=41.8781, longitude=-87.6298, zoom=10, pitch=45)
    deck = pdk.Deck(
        layers=[hex_layer],
        initial_view_state=view,
        map_provider="carto",
        map_style="light"
    )

    return deck, df_month

#############################
# TAB 1: High-Level Overview
#############################
with tab_overview:
    st.subheader("Forecast Overview")

    # Build plot with actual vs. forecast
    fig_future = make_subplots(rows=1, cols=1)

    fig_future.add_trace(go.Scatter(
        x=X_forecasting.index,
        y=X_forecasting['y'],
        mode='lines',
        name='Actual Trips',
        line=dict(color='lightblue')
    ))

    fig_future.add_trace(go.Scatter(
        x=X_forecasting.index,
        y=X_forecasting['preds'],
        mode='lines',
        name='Forecasted Trips',
        line=dict(color='orange', dash='dash')
    ))

    fig_future.update_layout(
        title="Future Forecast",
        xaxis_title="Date",
        yaxis_title="Trip Count",
        xaxis=dict(
            rangeslider=dict(visible=True),
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            )
        ),
        height=400,
        margin=dict(t=50, b=30, l=30, r=30),
        template="plotly_dark"
    )

    st.plotly_chart(fig_future, use_container_width=True)

    # Evaluate forecast accuracy
    eval_df = X_forecasting.loc[X_forecasting['y'] > 0].copy()
    mape_val = mean_absolute_percentage_error(eval_df['y'], eval_df['preds']) * 100
    rmse_val = mean_squared_error(eval_df['y'], eval_df['preds'])

    c_over1, c_over2 = st.columns(2)
    c_over1.metric("MAPE (Days with Actual)", f"{mape_val:.2f}%")
    c_over2.metric("RMSE", f"{rmse_val:.2f}")

    st.write("""
    **Interpretation**: The model's forecasts are compared to actual data.
    A lower MAPE or RMSE indicates better predictive performance.
    """)

#############################
# TAB 2: Monthly Hex Map
#############################
with tab_map:
    st.subheader("Monthly Trip Distribution")

    col_sel1, col_sel2 = st.columns(2)

    with col_sel1:
        st.markdown("**Select Month**")
        available_months = sorted(hex_data['year_month'].dt.strftime('%Y-%m').unique())
        month_str = st.selectbox(
            "Select Month (hidden label for accessibility)",
            available_months,
            index=0,
            label_visibility="collapsed"
        )

    month_dt = pd.to_datetime(month_str, format="%Y-%m")

    deck, df_month = build_deck_for_month(month_dt)

    if df_month.empty:
        st.warning("No data available for the selected month.")
    else:
        df_month_sorted = df_month.sort_values("trip_count", ascending=False)
        hex_ids = df_month_sorted.hex_id.unique()

        with col_sel2:
            st.markdown("**Select Hex by Rank**")
            index = st.slider(
                "Hex Rank (hidden label for accessibility)",
                0, len(hex_ids)-1, 0,
                label_visibility="collapsed"
            )

        selected_hex = hex_ids[index]
        deck_highlight, df_month = build_deck_for_month(month_dt, highlight_hex=selected_hex)

        col_map, col_info = st.columns([3, 2])
        with col_map:
            st.pydeck_chart(deck_highlight)

        with col_info:
            st.subheader("Hexagon Overview")
            st.markdown(f"**Selected Hexagon #{index+1} of {len(hex_ids)}**")

            hex_row = df_month[df_month.hex_id == selected_hex].iloc[0]

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Trips", f"{int(hex_row['trip_count'])}")
            c2.metric("Avg Distance", f"{hex_row['avg_distance']:.0f} m")
            c3.metric("Avg Duration", f"{hex_row['avg_duration']:.0f} s")
            c4.metric("Net Acc.", f"{int(hex_row['net_accumulation'])}")

            breakdown_df = pd.DataFrame({
                "Trip Type": ["Incoming", "Outgoing", "Local"],
                "Count": [
                    hex_row["incoming_trips"],
                    hex_row["outgoing_trips"],
                    hex_row["local_trips"]
                ]
            })

            fig_pie = px.pie(
                breakdown_df,
                names="Trip Type",
                values="Count",
                hole=0.5,
                title="Trip Type Breakdown"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            st.subheader("Monthly Summary")
            total_trips = df_month["trip_count"].sum()
            avg_trips = df_month["trip_count"].mean()

            c_s1, c_s2 = st.columns(2)
            c_s1.metric("Total Trips", f"{int(total_trips)}")
            c_s2.metric("Avg Trips/Hex", f"{avg_trips:.1f}")

            st.caption("Use the slider to highlight different hexagons by rank.")

#############################
# TAB 3: Usage Patterns
#############################
with tab_patterns:
    st.subheader("Trip Usage Patterns & Seasonality")

    st.markdown("**Monthly Trip Trends**")
    monthly_agg = hex_data.groupby("year_month", as_index=False)["trip_count"].sum()
    fig_line = px.line(
        monthly_agg,
        x="year_month",
        y="trip_count",
        title="Total Trips by Month",
        markers=True
    )
    fig_line.update_layout(xaxis_title="Month", yaxis_title="Total Trips")
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("**Day-of-Week vs. Hour Pattern**")
    if ("y" in X_forecasting.columns) and (X_forecasting.index.freq is not None or len(X_forecasting) > 2000):
        if hasattr(X_forecasting.index, 'hour'):
            forecast_copy = X_forecasting.copy()
            forecast_copy["day_of_week"] = forecast_copy.index.dayofweek
            forecast_copy["hour_of_day"] = forecast_copy.index.hour
            usage_pivot = forecast_copy.groupby(["day_of_week", "hour_of_day"])['y'].mean().reset_index()
            usage_matrix = usage_pivot.pivot(index="day_of_week", columns="hour_of_day", values="y")
            usage_matrix = usage_matrix.sort_index(ascending=True)

            fig_heatmap = px.imshow(
                usage_matrix,
                title="Average Trips by Day-of-Week & Hour",
                labels=dict(color="Avg Trips"),
                x=usage_matrix.columns,
                y=usage_matrix.index,
                aspect="auto",
                color_continuous_scale="OrRd"
            )
            fig_heatmap.update_layout(height=400)
            fig_heatmap.update_xaxes(title="Hour of Day")
            fig_heatmap.update_yaxes(title="Day of Week (Mon=0)")
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info("Hourly breakdown not available: data does not have hourly timestamps.")
    else:
        st.info("Forecast data is not granular enough to produce day-of-week/hour patterns.")

    st.write("""In this section, you can observe how usage changes by month and time. 
    E-scooter demand often spikes in warmer months and typical commute hours.""")

#############################
# TAB 4: Forecast Analysis
#############################
with tab_analysis:
    st.subheader("Forecast Error & Diagnostic Analysis")

    df_eval = X_forecasting.copy()
    if 'y' in df_eval.columns and 'preds' in df_eval.columns:
        df_eval = df_eval.dropna(subset=["y", "preds"])
        df_eval["error"] = df_eval["y"] - df_eval["preds"]

        fig_scatter = px.scatter(
            df_eval,
            x="preds",
            y="y",
            title="Actual vs. Forecasted Trips",
            labels={"preds": "Forecasted Trips", "y": "Actual Trips"},
            trendline="ols",
            opacity=0.6
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        fig_resid = px.histogram(
            df_eval,
            x="error",
            nbins=50,
            title="Distribution of Forecast Errors (Actual - Forecast)"
        )
        fig_resid.update_layout(xaxis_title="Error", yaxis_title="Frequency")
        st.plotly_chart(fig_resid, use_container_width=True)

        threshold = 3 * df_eval["error"].abs().mean()
        big_errors = df_eval[df_eval["error"].abs() > threshold]
        if not big_errors.empty:
            st.warning(f"Large misses detected (|error| > {threshold:.1f}). Possible unmodeled events.")
            st.write(big_errors[["y", "preds", "error"]].head(10))
    else:
        st.info("Forecast data not fully available to compute errors.")

    st.write("""Here you can inspect how closely forecasts match actual data. Points far from the diagonal 
    in the scatter plot indicate big misses. The residual histogram shows whether errors are centered near zero 
    or skewed.""")

#############################
# FINAL NOTES
#############################
st.markdown("---")
st.markdown("**Tip**: Use the 'Monthly Hex Map' tab to select a month and highlight hexes. The controls only appear on that tab, so the rest of the dashboard stays uncluttered.")