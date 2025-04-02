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
st.subheader("📍 Navigation & Usage")
st.markdown(
    """
    **Navigation**: Use the **sidebar** to move between different functions of the dashboard. 
    On mobile devices, tap the ☰ icon in the top-left to access the sidebar.

    Within each section, you may find filters (e.g., dates, regions, weather parameters) to 
    refine your view in the sidebar. Adjust these controls to explore specific scenarios or timeframes.
    """
)

# --- OVERVIEW OF SECTIONS ---
st.subheader("📊 Dashboard Sections")
st.markdown(
    """
    - **Historical Dashboard**  
      Explore past ridership data, both temporal and spatial, and look at the forecasting accuracy. 

    - **Temporal Scenario Deck**  
      Create custom forecasts based on calendar inputs (day of week, month, hour) 
      and weather conditions (temperature, rain, snow, wind). Visualize how changes 
      in these factors might affect hourly trip counts against a baseline.

    - **Spatial Trip Deck**  
      Explore E-Scooter demand on an interactive map. Identify hotspots, 
      visualize potential capacity constraints, and detect patterns across different neighborhoods in Chicago.

    - **Spatial Demand Deck**  
      Zoom into high-demand zones for rebalancing and resource planning. Discover 
      which areas consistently see peak usage and strategize daily scooter deployment.

    - **Space-to-Space Deck**  
      View origin-destination flows between hex regions in 3D or 2D KeplerGL maps. 
      A great tool for seeing how riders move throughout the city, highlighting 
      corridors of high traffic or under-served connections.
    """
)

# --- MOBILE FRIENDLINESS ---
st.subheader("📱 Tips for Mobile Users")
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
