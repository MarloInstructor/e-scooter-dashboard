import streamlit as st

# --- PAGE TITLE ---
st.title("E-Scooter Demand Dashboard")

# --- PROJECT DESCRIPTION ---
st.markdown(
    """
    Welcome to the **E-Scooter Demand Dashboard** – your one-stop solution for exploring,
    shared mobility operations of E-Scooter vendors in Chicago. This interactive platform consolidates 
    historical usage data, location-based consumer and operational demand patterns, and exploratory origin-destination analysis, using advanced modeling tools to facilitate 
    data-driven decisions on fleet distribution, infrastructure investments, and operational strategies.
    
    **Key Capabilities**:
    - Explore historical ridership trends and model accuracy
    - Visualize location-based demand patterns and operational hotspots
    - Forecast future usage based on weather and event inputs
    - Identify optimal spots for scooter deployment and rebalancing
    - Analyze origin-destination flows and identify high-traffic corridors
    """
)

# --- NAVIGATION & SIDEBAR INFO ---
st.subheader("Navigation & Usage")
st.markdown(
    """
    **Navigation**: Use the **sidebar** to move between different functions of the dashboard. 
    On mobile devices, tap the ☰ icon in the top-left to access the sidebar.

    Within each section, you may find filters (e.g., dates, regions, weather parameters) to 
    refine your view in the sidebar. Adjust these controls to explore specific scenarios or timeframes.
    """
)

# --- OVERVIEW OF SECTIONS ---
st.subheader("Dashboard Sections")

st.markdown(
    """
    **Historical Dashboard**  
    Explore past ridership data both temporally and spatially. View monthly usage trends and assess how well our models 
    performed by comparing historical predictions against actual data.

    **Temporal Scenario Deck**  
    Create custom forecasts based on calendar inputs (weekday, month, hour) and external conditions such as temperature, rain, 
    wind, or events. See how changing these variables affects hourly citywide demand.

    **Spatial Trip Deck**  
    Visualize e-scooter trip volumes across Chicago on an interactive hex map. Identify hotspots and usage patterns in 
    specific neighborhoods, and observe how demand shifts under different conditions.

    **Spatial Demand Deck**  
    Estimate the operational need for scooter relocation. This tool highlights areas with expected net accumulation or depletion 
    of scooters over a 6-hour window—useful for daily redistribution planning.

    **Space-to-Space Deck**  
    Examine directional trip flows between regions using interactive 2D and 3D KeplerGL maps. Reveal popular corridors, 
    under-utilized areas, and possible bottlenecks in rider movement.
    """
)

st.subheader("Technical Approach")

st.markdown(
    """
    The models were trained on a rich dataset combining publicly available e-scooter trip records from Chicago with weather data, 
    holidays, and event information scraped from the web. Spatial features were constructed using **H3 hexagonal binning**, and 
    time-based aggregations were created to reflect daily, hourly, and monthly trends.

    A key innovation in the modeling pipeline was the integration of **Prophet** (Meta’s open-source time series library) with 
    **XGBoost**. Prophet captured long-term seasonality and temporal patterns and generated forward-looking forecasts. These 
    forecasts were then passed into XGBoost as **lag-style features**, enabling the tree-based model to combine Prophet’s 
    extrapolative power with exogenous features like weather and events.

    This hybrid design eliminated the need for complex recurrent or sequential modeling and allowed forecasting across extended 
    horizons without manual time series splits.

    The dashboard interface was built in **Streamlit**, supporting real-time scenario simulations with sliders and selectors. 
    **Plotly** handled all temporal charts and pie breakdowns, while **Pydeck** rendered 3D hex maps for spatial insights. 
    **KeplerGL** was also used during prototyping for detailed exploration of trip vectors and flows across the city.
    """
)


# --- MOBILE FRIENDLINESS ---
st.subheader("Tips for Mobile Users")
st.markdown(
    """
    - Tap the ☰ icon in the top-left to open the sidebar and switch between pages.
    - Use pinch gestures or device orientation changes to navigate maps more easily.
    - If certain charts appear cut off, try rotating your phone horizontally.
    - You can scroll horizontally on wide data tables and charts.
    """
)

# --- FOOTER ---
st.markdown("---")
st.caption("Developed by Marlo Passler • Version 1.0")
