# E-Scooter Demand Forecasting Dashboard

This project was developed as a capstone for a data science bootcamp and explores e-scooter demand modeling in the city of Chicago. The inspiration came from an earlier team project, where we were tasked with designing a cloud-based data pipeline to collect weather and flight data. The scenario assumed an e-scooter company considering expansion, and needing reliable demand forecasts to make decisions around scooter relocation and pricing strategies.

The question was intriguing enough to pursue further, so I decided to build a comprehensive dashboard for my final project. The goal: leverage real-world public e-scooter trip data, enriched with weather, holiday, and event information, to forecast demand in both time and space. The result is a functional, interactive tool that can help operators understand how external conditions influence scooter usage and where resources are likely needed most.

## Project Overview

The dashboard brings together historical data visualizations and predictive models across several views. These views are accessible via tabs in the application and can also be explored on mobile (with the sidebar collapsed by default).

The **Historical Dashboard** provides an overview of past usage patterns. Users can analyze trends over time, explore usage by hour and day of the week, and review how trip volumes change across months. This section gives context to the data that powers the models.

The **Temporal Scenario Model** estimates total scooter usage by hour. It incorporates calendar effects such as weekday and month, as well as external influences like temperature, precipitation, and event schedules. The forecast is visualized as a time series, with sliders allowing users to simulate different scenarios and see how demand fluctuates in response.

The **Consumer Demand Model** extends the analysis into space. It predicts the number of trips originating in each hexagonal region of the city. These predictions are mapped dynamically and give a sense of where scooters are most likely to be needed based on conditions.

The **Operational Demand Model** goes one step further. Instead of just showing where scooters are picked up, it estimates the net operational demand—the difference between scooters arriving and departing in each area over a six-hour window. This can help vendors plan for relocation by highlighting areas of surplus and shortage. Regions with a strong surplus (excess scooters) are marked in red, while areas with a deficit (shortage of scooters) appear blue. This visual cue offers intuitive guidance for balancing fleet distribution.

While the foundation is strong, the two-week time frame limited what could be achieved in certain areas. For instance, a discounting strategy—where operators might offer incentives to rebalance supply—could only be partially addressed. A full origin–destination (O–D) model would be necessary to simulate the effects of discounting on trip flows between regions. However, this increases model complexity significantly, with over 5,000 spatial combinations, and was out of scope for the available time.

## Learning Notebooks
This repository includes three beginner-friendly Jupyter notebooks in the `notebooks` folder:
1. **Machine Learning Basics** – build a simple classifier with scikit-learn.
2. **Time-Series Forecasting** – explore Prophet for demand forecasting.
3. **Spatial Binning & Plotting** – visualize data with Folium hex maps.
Each notebook explains the theory, step by step code, and fun facts along the way.


## Technical Approach

The models were trained on a comprehensive dataset combining public e-scooter trip records from Chicago with web-scraped weather data, holiday calendars, and event schedules. Feature engineering included spatial binning via H3 hexagons, temporal aggregations (hourly, daily, and monthly), and the construction of features to reflect calendar effects, seasonality, and external shocks such as sports events.

A key component of the modeling pipeline was a hybrid forecasting strategy that combined Prophet, a time series model developed by Meta, with XGBoost, a powerful gradient boosting regressor. Prophet was first used to model the core temporal trends and seasonality in the scooter trip volumes. Its forecasts were then integrated into the XGBoost model as lag-style features—allowing the tree-based model to benefit from Prophet's strong temporal extrapolation without needing to design complex recurrent pipelines or manage rolling time-based validation schemes.

This setup provided the best of both worlds: Prophet handled long-horizon forecasting elegantly, while XGBoost brought in the flexibility and precision required to incorporate high-dimensional exogenous features like weather and event indicators. As a result, the models were able to deliver both accurate short-term predictions and scenario-based forecasts far beyond the range of historical data.

The final interactive dashboard was built in Streamlit, offering a lightweight but powerful front-end for scenario exploration. Users can manipulate weather, calendar, and event parameters to simulate hypothetical conditions and observe their impact in both the temporal and spatial domains. Visualizations were built using Plotly for interactivity, Pydeck for spatial rendering, and KeplerGL during early prototyping to explore trip trajectories and spatial flows.

## Challenges and Insights

A key insight was the difficulty of managing high-dimensional spatiotemporal forecasting. While trip starts and ends are relatively easy to model individually, combining them into a full matrix of flows poses significant challenges. Nonetheless, modeling starts and net demand separately already provides valuable operational insights.

Another learning was the importance of scenario simulation. Rather than focusing solely on predictive accuracy, the models are designed to explore "what-if" questions: What happens to demand if the weather worsens? How does a football game shift the flow of trips? This ability to experiment with assumptions is where the dashboard provides its current value given we don't have real-time trip data to play with.

## Final Thoughts

This project demonstrates that data-driven insights can inform real-world decision-making for mobility providers. Even with limited time and imperfect data, it's possible to extract actionable signals from patterns in usage, environment, and human behavior. The dashboard can serve as a foundation for more advanced analytics in the future, whether through discount modeling, live fleet optimization, or more granular origin–destination analysis.

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
