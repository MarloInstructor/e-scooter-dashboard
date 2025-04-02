import streamlit as st


# --- PAGE SETUP ---
about_page = st.Page(
    "e-scooter.py",
    title="E-scooter",
    icon=":material/web:",
    default=True,
)
project_1_page = st.Page(
    "page_dashboard.py",
    title="Historical dashboard",
    icon=":material/history:",
)
project_2_page = st.Page(
    "page_temporal.py",
    title="Temporal Scenario Deck",
    icon=":material/trending_up:",
)
project_3_page = st.Page(
    "page_hex_customer.py",
    title="Spatial Trip Deck",
    icon=":material/hexagon:",
)
project_4_page = st.Page(
    "page_hex_operational.py",
    title="Spatial Demand Deck",
    icon=":material/monitoring:",
)
project_5_page = st.Page(
    "page_keplergl.py",
    title="Space-to-Space Deck",
    icon=":material/explore:",
)



# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [about_page],
        "Projects": [project_1_page, project_2_page, project_3_page, project_4_page, project_5_page],
    }
)

# --- RUN NAVIGATION ---
pg.run()