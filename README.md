# E-Scooter Demand Dashboard – Project Overview

**Goal:** Within **two weeks**, build a functional prototype that forecasts **E-Scooter usage and operational demand** both **temporally** (time-based) and **spatially** (location-based). We so aimed to visualize how external factors (weather, holidays, events) affect usage patterns and how many scooters may need to be moved into or out of certain areas.

---

## Core Models: Three “Decks” Explained

1. **Temporal Deck (Hourly Demand Model)**  
   - **Focus**: Predicts overall hourly scooter usage across the entire city.  
   - **Key Features**:  
     - Day of the week, month, holiday indicators  
     - Weather conditions (rain, snow, wind, humidity)  
     - Special events (e.g., football games)  
   - **Output**: An **hourly demand forecast** showing how many rides are expected citywide at each hour.

2. **Spatial Trip Deck (Trip Distribution Model)**  
   - **Focus**: Displays **where rides start** over time, highlighting regions with higher or lower trip volumes.  
   - **Key Features**:  
     - Similar to the Temporal Deck (day-of-week, weather, events)  
     - Spatial segmentation—pinpointing trip **start locations** across different time frames  
   - **Output**: A **spatiotemporal forecast** illustrating which regions see higher or lower numbers of **trip**, helping providers understand consumer demand.

3. **Demand Deck (Net Operational Demand Model)**  
   - **Focus**: Estimates how many scooters **accumulate** in or **vanish** from a specific area over a **6-hour window**—helping operators see where they must **add** or **remove** scooters.  
   - **Key Features**:  
     - Starts vs. ends in each region, aggregated over 6 hours  
     - External factors (again weather, events, holidays)  
   - **Output**: A **net demand metric** (ends - starts or vice versa), informing operational moves. This is not purely “consumer demand” but rather the **operational demand** for scooter placement/relocation.

### Why We Didn’t Finish a Full “Space-to-Space” Vector Model
- Modeling each origin–destination pair in detail (for about 70 spatial bins) leads to over 5000 possible connections.  
- Including a **temporal dimension** (e.g., hourly or 6-hour intervals) amplifies the data and computational requirements.  
- Within two weeks, we couldn’t thoroughly tackle such a high-dimensional challenge.  

---

## What We Actually Achieved

- **Historical Dashboard**: Displays past usage trends, revealing seasonality and general usage spikes.  
- **3D and Map Visualizations**:  
  - **KeplerGL Page**: Enables visual “scouting” of trip vectors in 3D (Arc layer), so you can see the high dimensionality of the problem but also a potential starting point for further analysis or modeling.  
  - **the thre Scenario Decks**: Show areas and times with high demand in scooter and scooter availability, potentially aiding operational decisions.  
- **Integration of External Factors**:  
  - **Weather** (rain, snow, wind, humidity)  
  - **Holidays** (impacting usage patterns)  
  - **Major Events** (e.g., football games)

Although data constraints (hourly intervals, wide spatial bins) limited precision, we demonstrated **how external factors correlate** with changing scooter usage or net demand. These methods are easily transferable to other industries (e.g., sales forecasts plus promotional events).

---
## Project Plan

- **Data Engineer (DE)**
   - Collects, cleans, and enriches raw scooter trip data.
   - Integrates external factors (weather, holidays, events).
   - Defers deeper spatial transformations to the ML Engineer.
- **Machine Learning Engineer (MLE)**
   - Builds, tests, and refines forecasting models.
   - Performs spatial binning/clustering to create region-level (or O–D) analyses.
   - Explores scenario simulations (discounts in certain regions).
- **Data Visualizer / Streamlit Developer (DV)**
   - Provides an interactive dashboard combining multiple “decks.”
   - Adds user-friendly controls to test hypothetical conditions (e.g., event day, weather extremes).

---
## What I Learned

- **Data Cleaning & Project Leadership**:  
  - Initially stepped into **Data Engineer duties** to rapidly prepare the scooter trip data.  
  - Served as **Project Lead**, defining goals, coordinating tasks, and maintaining focus.

- **AI Engineering**:  
  - Developed multiple **forecasting models** (hourly citywide usage, spatial trip distribution, and net operational demand).  
  - Ensured results were integrated into a **user-friendly dashboard** for quick insights.

- **Key Success Factors**:  
  - **Frequent communication**—daily updates.  
  - **Clear role assignments**, allowing concurrent development (data prep, modeling, visualization).  
  - **Successive feature integration**, letting the models evolve as new data arrive, as well as visualizing the models using the Scenario Decks in the Streamlit App, ensures relative independence of the three formulated roles.

- **Outcome**:  
  - A dynamic prototype showing **when, where, and how many scooters** are used—or needed—across Chicago.  
  - Despite the data gaps and the inability to finalize a full “vector” O–D model, we laid a strong foundation for more advanced mobility analytics.

---

## Key Skills & Technologies Acquired

- **Python**: Primary scripting and data manipulation language.  
- **Pandas & NumPy**: Efficient handling of large datasets, merging, and transformations.  
- **scikit-learn**: Training and validating ML models (XGBoost).  
- **Prophet**: Specialized time-series forecasting for seasonality and trend detection (open source by META).  
- **Streamlit**: Quick and easy development of interactive dashboards.  
- **Plotly & Matplotlib**: Graphical libraries for line plots, bar charts, and interactive data views.  
- **KeplerGL & pydeck**: Geospatial visualization, 3D mapping of trip data and net demand (open source by Uber).  
- **Spatial Binning / Clustering**: Techniques like h3-binning to group locations into meaningful regions.

---

## Project Strategy & Role Distribution

### Overall Project Flow

1. **Data Engineer (DE)**  
   - Collects, cleans, and enriches raw trip data.  
   - Integrates external factors like weather, holidays, and events.  
   - Defers deeper **spatial transformations** to the ML Engineer.

2. **Machine Learning Engineer (MLE)**  
   - Builds, tests, and refines forecasting models.  
   - Performs spatial binning/clustering to create region-level analyses.  
   - Explores scenario simulations (discounts in certain regions).

3. **Data Visualizer / Streamlit Developer (DV)**  
   - Provides an **interactive dashboard** combining multiple “decks.”  
   - Adds user-friendly controls (sliders, dropdowns) to explore hypothetical conditions (e.g., event day, weather extremes).

### Holding Out 3 Weeks
We set aside three weeks of data **unseen by the models** to measure “true future” performance, ensuring our metrics didn’t overfit.

---

## Making It Work Smoothly

- **Start Simple, Evolve Gradually**  
  - On Day 1, the DE delivered a basic daily demand dataset.  
  - The MLE immediately began baseline forecasting, then added complexity as new features arrived.

- **Frequent Incremental Updates**  
  - The MLE retrains/improves models whenever the DE releases new data or features.  
  - The DV updates dashboards to keep forecasts current.

- **Communication & Ownership**  
  - Daily or every-other-day stand-ups to highlight blockers and remain aligned.  
  - Clear responsibilities ensure minimal overlap and confusion.

---

## Next Steps & Future Possibilities

- **Comprehensive Vector O–D Modeling**  
  - Could require reducing temporal granularity (e.g., weekly) or using more advanced factorization methods to handle large state spaces.  
  - Ideal for deeper discount strategy insights or supply reallocation planning.

- **Deeper Feature Engineering**  
  - Incorporating additional data sources (e.g., real-time traffic, concurrency with other micro-mobility options) could improve accuracy.  
  - More precise event data might capture usage fluctuations more effectively.

- **Enhanced Visualization & UI**  
  - Although Streamlit was great for quick prototyping, a custom interface or specialized geospatial front-end could yield a more refined user experience.

---

**Thank you for your interest – I look forward to future projects and exciting collaborations!**
